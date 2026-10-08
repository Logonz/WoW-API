# /// script
# requires-python = ">=3.12"
# dependencies = ["requests"]
# ///
"""Dump everything warcraft.wiki.gg knows about the WoW API, then index every name in it.

Two stages, so parsing can be iterated on without hitting the wiki again:

  fetch  Walk the wiki and cache raw pages under <out>/raw/. Seeds are the API and Event
         namespaces, every page using an API page template (functions, widget methods,
         UIOBJECT/UIHANDLER/CVar/MACRO/Structure pages, ...), the index pages and the
         Module:Wowapi data tables. It then keeps following redirects (both directions),
         transclusions and API links until nothing new turns up. Links that lead nowhere
         are recorded as missing.
  build  Parse the cache offline into:
           entries.jsonl  one record per page AND per redirect page: kind, API name, facts
                          (signatures, restrictions, deprecation, ...), categories, redirect
                          target with #section and how the names relate
           listings.jsonl rows from index pages and UIOBJECT method lists (args, returns,
                          tags like protected/secureframe, flavor bits, description)
           data/*.json    Module:Wowapi data tables as JSON (flavors, patches, groups of
                          renamed functions, secret-value predicates, systems, CVars).
                          system/* hold system -> names; the wiki inverts them at runtime.
           names.tsv      one row per name/title: name, status, kind, title, target, relation,
                          flavors, tags, detail. Status:
                            page      has its own page
                            redirect  title redirects to another page
                            section   redirect into a #section of another page
                            no-page   known from data tables or index lists, but no page
                            red-link  linked on the wiki, nothing exists
                          Relation (how the name relates to the target page):
                            same-name    same API, old/new title style ('API X' -> 'API:X')
                            case         differs only in case
                            unqualified  bare name -> qualified ('ClearAllPoints' -> 'Region:...')
                            moved        same function, other namespace/class ('Frame:X' -> 'ScriptRegion:X')
                            renamed      different name ('GetUnitName' -> 'UnitName')
                            dead link    red link whose name still resolves to a page
                            same-method  no page; the method is documented on another class
           manifest.json  counts and build info

Network: requests go through the scraper-questie proxies by default (PROXY_* from --env-file),
rotating across ports, throttled by --delay.

Run:
  uv run wiki_dump.py             fetch + build
  uv run wiki_dump.py build       rebuild from the cache only
  uv run wiki_dump.py --network-mode local
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import shutil
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

API_URL = "https://warcraft.wiki.gg/api.php"
USER_AGENT = "wow-api-wiki-dump/0.2 (personal project)"
BATCH = 50  # anonymous API limit for titles and page content per request
DEFAULT_ENV_FILE = Path("~/projects/scraper-questie/wh_parser/.env").expanduser()
DEFAULT_PROXY_PORTS = "8001-8010"  # scraper-questie DE_PORTS

NS_NAMES = {
  0: "Main", 2: "User", 4: "Project", 10: "Template", 14: "Category", 828: "Module", 3000: "API", 3004: "Event",
}

# Template -> page kind, in priority order (a function page may also use Restrictedapi etc.).
KIND_TEMPLATES = [
  ("Widgetmethod", "widget-method"),
  ("Intrinsicmethod", "intrinsic-method"),
  ("Luaapi", "lua-function"),
  ("Framexmlfunc", "framexml-function"),
  ("Wowapievent", "event"),
  ("Wowapitype", "type"),
  ("Widget", "widget"),
  ("Widgethandler", "widget-handler"),
  ("Wowsystem", "system"),
  ("Intrinsic", "intrinsic"),
  ("Framexmltype", "framexml-type"),
  ("Cvar", "cvar"),
  ("Removedcvar", "cvar"),
  ("Macro API", "macro"),
  ("Removedapi", "removed-function"),
  ("Wowapi", "function"),
]
SEED_TEMPLATES = [t for t, _ in KIND_TEMPLATES] + ["Restrictedapi", "Deprecatedapi", "Apicompat"]

# Overview pages whose lists carry tags and flavor bits that single pages may not.
INDEX_PAGES = [
  "World of Warcraft API",
  "World of Warcraft API/Classic",
  "Widget API",
  "ScriptObject API",
  "Events",
  "Events/Classic",
  "Global functions",
  "Global functions/Classic",
  "Lua functions",
  "FrameXML functions",
  "Console variables",
  "Console variables/Classic",
  "API types",
  "Widget script handlers",
  "Secure Execution and Tainting",
  "World of Warcraft Non-Public API",
  "Category:API functions/restricted",
]
EXTRA_MODULES = ["Module:API info/cvar/data", "Module:API info/restricted"]
# Guide pages docs/Security.md is written from (the wiki's Secure Execution trail), kept for reference.
GUIDE_PAGES = [
  "Object security", "Secret Values", "SecureHandlers", "SecureActionButtonTemplate", "SecureUnitButtonTemplate",
  "SecureHandlerStateTemplate", "RestrictedEnvironment", "Secure code", "Template:API Trail Secure",
]

# Link targets worth following (and reporting when they lead nowhere).
SCOPE_PREFIXES = (
  "API:", "API ", "Event:", "UIOBJECT ", "UIHANDLER ", "ScriptObject ", "INTRINSIC ",
  "CVar ", "Structure ", "Struct ", "Enum.", "API types/", "XML/", "FrameXML types/",
)
NAME_PREFIXES = ("UIOBJECT ", "UIHANDLER ", "ScriptObject ", "INTRINSIC ", "CVar ", "MACRO ")
KEEP_TITLE_PREFIXES = ("API types/", "Structure ", "Struct ", "Enum.", "XML/", "FrameXML types/")
TITLE_KINDS = [
  ("CVar ", "cvar"), ("MACRO ", "macro"), ("UIOBJECT ", "widget"), ("UIHANDLER ", "widget-handler"),
  ("INTRINSIC ", "intrinsic"), ("ScriptObject ", "widget"), ("XML/", "widget"),
  ("API types/", "type"), ("Structure ", "type"), ("Struct ", "type"), ("Enum.", "type"), ("API ", "function"),
]
# listing {{apilink|t=...}} / data module -> kind for names that have no page
LISTING_KINDS = {"w": "widget-method", "h": "widget-handler", "e": "event", "a": "function", "Function": "function"}
DATA_KINDS = {
  "gametype/function": "function", "gametype/event": "event",
  "gametype/widget": "widget-method", "gametype/scriptobject": "widget-method",
}
NON_API_KINDS = {"type", "framexml-type", "system", "index", "module", "other"}
API_KINDS = {
  "function", "widget-method", "intrinsic-method", "lua-function", "framexml-function",
  "removed-function", "event",
}
NAMED_KINDS = API_KINDS | {"widget", "widget-handler", "intrinsic", "cvar", "macro", "type"}
FLAVOR_BITS = [(0x1, "standard"), (0x2, "forever"), (0x4, "mists"), (0x8, "tbc"), (0x10, "vanilla")]
PATCH_FLAVORS = {"standard": "standard", "camelot": "forever", "mists": "mists", "tbc": "tbc", "vanilla": "vanilla"}

REDIRECT_RE = re.compile(r"^\s*#REDIRECT\s*\[\[([^\]|]+)", re.IGNORECASE)
LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
TRANSCLUDE_RE = re.compile(r"\{\{\s*:([^|}]+)")
TEMPLATE_RE = re.compile(r"\{\{\s*([A-Za-z][^{}|#:<>\n]*?)\s*(?:\||\}\})")
MAGIC_WORDS = {"PAGENAME", "FULLPAGENAME", "BASEPAGENAME", "SUBPAGENAME", "NAMESPACE", "DISPLAYTITLE", "DEFAULTSORT"}
NONCONTENT_RE = re.compile(
  r"<!--.*?-->|<(nowiki|pre|syntaxhighlight|source)\b[^>]*>.*?</\1\s*>", re.DOTALL | re.IGNORECASE
)
# {{api|t=...|Name}} link types -> page title (Module:Api.link)
API_LINK_TITLES = {
  "a": "API:{}", "w": "API:{}", "e": "Event:{}", "c": "CVar {}", "wh": "UIHANDLER {}",
  "o": "UIOBJECT {}", "sc": "ScriptObject {}", "x": "XML/{}", "i": "INTRINSIC {}",
}


def log(msg: str) -> None:
  print(msg, file=sys.stderr, flush=True)


def clean(title: str) -> tuple[str, str]:
  """Normalize a link target like MediaWiki does; returns (title, fragment). Keeps '(...)':
  some titles really end in '()', e.g. 'API FramerateFrame:Toggle()'."""
  title, _, fragment = title.partition("#")
  title = re.sub(r"\s+", " ", title.strip().lstrip(":").replace("_", " "))
  return (title[:1].upper() + title[1:], fragment.strip())


def in_scope(title: str) -> bool:
  return title.startswith(SCOPE_PREFIXES)


def strip_noncontent(text: str) -> str:
  """Drop comments and code blocks, whose [[links]] and {{templates}} are not real (editor
  boilerplate like '<!-- or {{wowapievent}}, {{widgetmethod}} -->', Lua examples)."""
  return NONCONTENT_RE.sub("", text)


def api_template_targets(text: str):
  """Titles linked by {{api|...}}, mapped the way Module:Api.link does it."""
  for call in template_calls(text, "api"):
    link_type, name = call.get("t", "a"), call.get("1", "").strip()
    if link_type in API_LINK_TITLES and name:
      if link_type in ("a", "w"):
        name = name.split("(")[0].replace(":", "_")
      yield clean(API_LINK_TITLES[link_type].format(name))[0]


def chunks(items: list, size: int):
  for i in range(0, len(items), size):
    yield items[i : i + size]


# --- Network ---------------------------------------------------------------------------------


def load_env_file(path: Path) -> None:
  """KEY=VALUE lines into os.environ; values already in the environment win."""
  if not path.is_file():
    return
  for line in path.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
      key, value = line.split("=", 1)
      os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def proxy_urls(ports: str) -> list[str]:
  host, user, password = (os.environ.get(k) for k in ("PROXY_HOST", "PROXY_USERNAME", "PROXY_PASSWORD"))
  if not all((host, user, password)):
    raise SystemExit("proxy mode needs PROXY_HOST, PROXY_USERNAME and PROXY_PASSWORD (see --env-file)")
  first, _, last = ports.partition("-")
  auth = f"{quote(user, safe='')}:{quote(password, safe='')}"
  return [f"http://{auth}@{host}:{port}" for port in range(int(first), int(last or first) + 1)]


class WikiClient:
  """Polite, sequential MediaWiki client: throttled, honours maxlag/429, rotates proxies."""

  def __init__(self, delay: float, proxies: list[str]):
    self.delay = delay
    self.last_request = 0.0
    self.proxies = itertools.cycle(proxies) if proxies else None
    self.session = requests.Session()
    self.session.headers["User-Agent"] = USER_AGENT
    self.requests = 0
    self.normalized: dict[str, str] = {}  # title as we asked -> title as MediaWiki spells it

  def get(self, **params) -> dict:
    query = {"action": "query", "format": "json", "formatversion": 2, "maxlag": 5, **params}
    for attempt in range(8):
      pause = self.delay - (time.monotonic() - self.last_request)
      if pause > 0:
        time.sleep(pause)
      self.last_request = time.monotonic()
      proxy = next(self.proxies) if self.proxies else None
      self.requests += 1
      try:
        resp = self.session.get(
          API_URL, params=query, timeout=90, proxies={"http": proxy, "https": proxy} if proxy else None
        )
      except requests.RequestException as e:
        retry_after = 2**attempt
        log(f"  network error ({type(e).__name__}), retrying in {retry_after}s")
        time.sleep(retry_after)
        continue
      if resp.status_code == 200:
        data = resp.json()
        error = data.get("error")
        if error is None:
          return data
        if error.get("code") != "maxlag":
          raise RuntimeError(f"API error: {error}")
        retry_after = int(resp.headers.get("Retry-After", 5))
      elif resp.status_code in (429, 500, 502, 503, 504):
        retry_after = int(resp.headers.get("Retry-After") or 2 ** (attempt + 1))
      else:
        resp.raise_for_status()
      log(f"  HTTP {resp.status_code}, retrying in {retry_after}s ({attempt + 1}/8)")
      time.sleep(retry_after)
    raise RuntimeError(f"gave up after retries: {params}")

  def query_all(self, key: str, **params) -> list[dict]:
    """A list= query, following continue tokens."""
    cont: dict = {}
    out: list[dict] = []
    while True:
      data = self.get(**params, **cont)
      out += data.get("query", {}).get(key, [])
      if "continue" not in data:
        return out
      cont = data["continue"]

  def pages(self, **params):
    """Page objects from a prop= query, following continue tokens (a page may repeat)."""
    cont: dict = {}
    while True:
      data = self.get(**params, **cont)
      query = data.get("query", {})
      self.normalized.update({n["from"]: n["to"] for n in query.get("normalized", [])})
      yield from query.get("pages", [])
      if "continue" not in data:
        return
      cont = data["continue"]


# --- Fetch stage -----------------------------------------------------------------------------


def file_for(title: str, ns: int) -> str:
  """Reversible, Windows-safe relative path for a page: <Namespace>/<Title_without_prefix>.wiki."""
  name = title.split(":", 1)[1] if ns != 0 and ":" in title else title
  ext = ".lua" if ns == 828 else ".wiki"
  return f"{NS_NAMES.get(ns, f'ns{ns}')}/{quote(name.replace(' ', '_'), safe='_.,-()!')}{ext}"


class RawStore:
  """The fetch cache: page files plus pages.jsonl (metadata) and missing.json."""

  def __init__(self, root: Path):
    self.root = root
    self.meta: dict[str, dict] = {}  # title -> metadata
    self.queried: set[str] = set()  # titles already asked for (input spelling)
    self.missing: dict[str, set[str]] = defaultdict(set)  # nonexistent title -> referencing pages
    self.refs: dict[str, set[str]] = defaultdict(set)  # title -> pages that link/transclude it
    self.unresolved: set[str] = set()  # asked for, but MediaWiki returned neither content nor 'missing'

  def text(self, title: str) -> str:
    return (self.root / "pages" / self.meta[title]["file"]).read_text(encoding="utf-8")

  def save(self, normalized: dict[str, str]) -> None:
    for asked, spelled in normalized.items():
      self.refs[spelled] |= self.refs.get(asked, set())
    with (self.root / "pages.jsonl").open("w", encoding="utf-8") as f:
      for title in sorted(self.meta):
        f.write(json.dumps(self.meta[title], ensure_ascii=False) + "\n")
    missing = {t: sorted(self.refs.get(t, ())) for t in sorted(self.missing)}
    (self.root / "missing.json").write_text(json.dumps(missing, indent=1, ensure_ascii=False), encoding="utf-8")


def seed_titles(wiki: WikiClient) -> set[str]:
  titles: set[str] = set()
  for ns in (3000, 3004):
    found = wiki.query_all("allpages", list="allpages", apnamespace=ns, aplimit=500)
    log(f"  namespace {NS_NAMES[ns]}: {len(found)} titles")
    titles.update(p["title"] for p in found)
  for template in SEED_TEMPLATES:
    found = wiki.query_all("embeddedin", list="embeddedin", eititle=f"Template:{template}", eilimit=500)
    log(f"  Template:{template}: {len(found)} pages")
    titles.update(p["title"] for p in found)
  old_style = wiki.query_all(
    "allpages", list="allpages", apnamespace=0, apprefix="API ", apfilterredir="nonredirects", aplimit=500
  )
  log(f"  main-namespace 'API ' pages: {len(old_style)}")
  titles.update(p["title"] for p in old_style)
  modules = wiki.query_all("allpages", list="allpages", apnamespace=828, apprefix="Wowapi/data/", aplimit=500)
  log(f"  Module:Wowapi/data: {len(modules)} modules")
  titles.update(p["title"] for p in modules)
  titles.update(INDEX_PAGES)
  titles.update(EXTRA_MODULES)
  titles.update(GUIDE_PAGES)
  return titles


def fetch_content(wiki: WikiClient, titles: list[str], store: RawStore, retry: bool = True) -> list[str]:
  """Fetch wikitext + revision info; returns the titles that now exist in the store."""
  fetched: list[str] = []
  without_content: set[str] = set()
  for batch in chunks(titles, BATCH):
    store.queried.update(batch)
    params = {"prop": "info|revisions", "rvprop": "content|ids|timestamp", "rvslots": "main"}
    for page in wiki.pages(titles="|".join(batch), **params):
      title = page["title"]
      if page.get("missing") or page.get("invalid"):
        store.missing.setdefault(title, set())
        continue
      if not page.get("revisions"):
        without_content.add(title)  # content may arrive in a later continue chunk
        continue
      rev = page["revisions"][0]
      text = rev["slots"]["main"].get("content", "")
      meta = {
        "title": title,
        "ns": page["ns"],
        "pageid": page["pageid"],
        "revid": rev["revid"],
        "timestamp": rev["timestamp"],
        "redirect": bool(page.get("redirect") or REDIRECT_RE.match(text)),
        "file": file_for(title, page["ns"]),
        "categories": [],
        "redirects": [],
      }
      path = store.root / "pages" / meta["file"]
      path.parent.mkdir(parents=True, exist_ok=True)
      path.write_text(text, encoding="utf-8")
      store.meta[title] = meta
      fetched.append(title)
  leftover = sorted(without_content - store.meta.keys())
  if leftover and retry:
    log(f"  retrying {len(leftover)} pages that came back without content")
    fetched += fetch_content(wiki, leftover, store, retry=False)
  elif leftover:
    log(f"  WARNING: no content for {len(leftover)} pages: {leftover[:5]}")
    store.unresolved.update(leftover)
  return fetched


def fetch_categories(wiki: WikiClient, titles: list[str], store: RawStore) -> None:
  for batch in chunks(titles, BATCH):
    for page in wiki.pages(titles="|".join(batch), prop="categories", clprop="hidden", cllimit="max"):
      if page["title"] in store.meta:
        store.meta[page["title"]]["categories"] += [
          {"title": c["title"], "hidden": bool(c.get("hidden"))} for c in page.get("categories", [])
        ]


def fetch_redirects(wiki: WikiClient, titles: list[str], store: RawStore) -> set[str]:
  """Record which pages redirect to each title; returns the redirect titles."""
  found: set[str] = set()
  for batch in chunks(titles, BATCH):
    for page in wiki.pages(titles="|".join(batch), prop="redirects", rdprop="title|fragment", rdlimit="max"):
      for r in page.get("redirects", []):
        found.add(r["title"])
        if page["title"] in store.meta:
          store.meta[page["title"]]["redirects"].append({"title": r["title"], "fragment": r.get("fragment", "")})
  return found


def follow_ups(store: RawStore, titles: list[str]) -> set[str]:
  """Titles reachable from freshly fetched pages: redirect targets, transclusions, API links."""
  found: set[str] = set()
  for title in titles:
    meta = store.meta[title]
    if meta["ns"] == 828:
      continue  # Lua modules: [[...]] inside them is code, not links
    text = store.text(title)
    if meta["redirect"]:
      if m := REDIRECT_RE.match(text):
        target = clean(m.group(1))[0]
        store.refs[target].add(title)
        found.add(target)
      continue
    if meta["ns"] == 10:
      continue  # templates are fetched for their content; their own links are not API pages
    text = strip_noncontent(text)
    targets = [clean(m.group(1))[0] for m in TRANSCLUDE_RE.finditer(text)]
    targets += [t for m in LINK_RE.finditer(text) if in_scope(t := clean(m.group(1))[0])]
    targets += [t for t in api_template_targets(text) if in_scope(t)]
    for target in targets:
      store.refs[target].add(title)
      found.add(target)
    # Content templates such as {{AuraType|aura}} hold the returns of UnitAura & co.
    templates = {m.group(1) for m in TEMPLATE_RE.finditer(text)} - MAGIC_WORDS
    found.update(f"Template:{clean(name)[0]}" for name in templates)
  return found


def fetch(wiki: WikiClient, raw: Path) -> None:
  shutil.rmtree(raw, ignore_errors=True)
  raw.mkdir(parents=True)
  store = RawStore(raw)

  log("seeding titles")
  queue = seed_titles(wiki)
  for round_no in itertools.count(1):
    todo = sorted(t for t in queue if t not in store.meta and t not in store.queried and t not in store.missing)
    if not todo:
      break
    log(f"round {round_no}: fetching {len(todo)} titles")
    fetched = fetch_content(wiki, todo, store)
    fetch_categories(wiki, fetched, store)
    targets = [t for t in fetched if not store.meta[t]["redirect"]]
    queue = fetch_redirects(wiki, targets, store) | follow_ups(store, fetched)
    log(f"  {len(fetched)} pages stored, {len(store.missing)} missing so far, {wiki.requests} requests")

  store.save(wiki.normalized)
  info = {
    "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "source": API_URL,
    "pages": len(store.meta),
    "redirect_pages": sum(1 for m in store.meta.values() if m["redirect"]),
    "unresolved": sorted(store.unresolved),
    "missing": len(store.missing),
    "requests": wiki.requests,
  }
  (raw / "fetch.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
  log(f"fetch done: {info}")


# --- Lua data modules ------------------------------------------------------------------------


class LuaTableParser:
  """Reads Lua table constructors from Scribunto data modules. Parses only; never executes."""

  NUMBER = re.compile(r"-?(0[xX][0-9a-fA-F]+|\d+(\.\d+)?([eE][-+]?\d+)?)")
  IDENT = re.compile(r"[A-Za-z_]\w*")

  def __init__(self, src: str):
    self.s = src
    self.i = 0

  def skip(self) -> None:
    while self.i < len(self.s):
      if self.s[self.i].isspace():
        self.i += 1
      elif self.s.startswith("--", self.i):
        long = re.match(r"--\[(=*)\[", self.s[self.i :])
        if long:
          end = self.s.find(f"]{long.group(1)}]", self.i)
          self.i = len(self.s) if end < 0 else end + len(long.group(1)) + 2
        else:
          end = self.s.find("\n", self.i)
          self.i = len(self.s) if end < 0 else end + 1
      else:
        return

  def value(self):
    self.skip()
    c = self.s[self.i]
    if c == "{":
      return self.table()
    if c in "\"'":
      return self.string(c)
    long = re.match(r"\[(=*)\[", self.s[self.i :])
    if long:
      start = self.i + len(long.group(0))
      end = self.s.find(f"]{long.group(1)}]", start)
      if end < 0:
        raise ValueError(f"unterminated long string at {start}")
      self.i = end + len(long.group(1)) + 2
      return self.s[start:end]
    if m := self.NUMBER.match(self.s, self.i):
      self.i = m.end()
      text = m.group(0)
      if "x" in text.lower():
        return int(text, 16)
      return float(text) if any(ch in text for ch in ".eE") else int(text)
    if m := self.IDENT.match(self.s, self.i):
      word = m.group(0)
      if word in ("true", "false", "nil"):
        self.i = m.end()
        return {"true": True, "false": False, "nil": None}[word]
    return self.expression()

  def expression(self) -> dict:
    """Anything that is not a literal (a variable, a call): keep its source text."""
    start, depth = self.i, 0
    while self.i < len(self.s):
      c = self.s[self.i]
      if c in "({[":
        depth += 1
      elif c in ")}]":
        if depth == 0:
          break
        depth -= 1
      elif c in ",;" and depth == 0:
        break
      self.i += 1
    return {"$expr": self.s[start : self.i].strip()}

  def string(self, quote_char: str) -> str:
    self.i += 1
    out = []
    escapes = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'"}
    while self.s[self.i] != quote_char:
      c = self.s[self.i]
      if c == "\\":
        nxt = self.s[self.i + 1]
        if nxt.isdigit():
          digits = re.match(r"\d{1,3}", self.s[self.i + 1 :]).group(0)
          out.append(chr(int(digits)))
          self.i += 1 + len(digits)
          continue
        out.append(escapes.get(nxt, nxt))
        self.i += 2
        continue
      out.append(c)
      self.i += 1
    self.i += 1
    return "".join(out)

  def table(self):
    self.i += 1
    items: dict = {}
    position = 0
    while True:
      self.skip()
      if self.s[self.i] == "}":
        self.i += 1
        break
      if self.s[self.i] == "[" and not re.match(r"\[=*\[", self.s[self.i :]):
        self.i += 1
        key = self.value()
        self.skip()
        self.i += 1  # ]
        self.skip()
        self.i += 1  # =
        items[key] = self.value()
      elif (m := self.IDENT.match(self.s, self.i)) and re.match(r"\s*=(?!=)", self.s[m.end() :]):
        self.i = m.end()
        self.skip()
        self.i += 1  # =
        items[m.group(0)] = self.value()
      else:
        position += 1
        items[position] = self.value()
      self.skip()
      if self.i < len(self.s) and self.s[self.i] in ",;":
        self.i += 1
    if items and list(items) == list(range(1, len(items) + 1)):
      return list(items.values())
    return {str(k): v for k, v in items.items()}


MERGE_RE = re.compile(r"^for\s+(\w+),\s*(\w+)\s+in\s+pairs\((\w+)\)\s+do\s+(\w+)\[\1\]\s*=\s*\2\s+end", re.MULTILINE)


def parse_lua_module(src: str):
  """The data a module returns, read statically: its top-level `name = {...}` tables, with
  `for k, v in pairs(a) do b[k] = v end` merges applied. Returns the `return`ed table when it
  holds data, else the only non-empty table, else all tables by name."""
  tables = {}
  for m in re.finditer(r"^(?:local\s+)?([A-Za-z_][\w.]*)\s*=\s*(?=\{)", src, re.MULTILINE):
    parser = LuaTableParser(src)
    parser.i = m.end()
    tables[m.group(1)] = parser.value()
  for _, _, source, dest in MERGE_RE.findall(src):
    if isinstance(tables.get(source), dict) and isinstance(tables.get(dest), dict):
      tables[dest] = {**tables[dest], **tables[source]}
  returned = re.search(r"^return\s+([\w.]+)\s*$", src, re.MULTILINE)
  if returned and tables.get(returned.group(1)):
    return tables[returned.group(1)]
  non_empty = {k: v for k, v in tables.items() if v}
  if len(non_empty) == 1:
    return next(iter(non_empty.values()))
  return tables


# --- Build stage -----------------------------------------------------------------------------


def closing_braces(text: str, i: int) -> int:
  """Index of the '}}' that closes a template whose body starts at i, or -1."""
  depth = 0
  while i < len(text) - 1:
    if text.startswith("{{", i):
      depth, i = depth + 1, i + 2
    elif text.startswith("}}", i):
      if depth == 0:
        return i
      depth, i = depth - 1, i + 2
    else:
      i += 1
  return -1


def split_params(body: str) -> list[str]:
  """Split a template body on '|' that is not inside a nested {{...}} or [[...]]."""
  parts, depth, start, i = [], 0, 0, 0
  while i < len(body):
    pair = body[i : i + 2]
    if pair in ("{{", "[["):
      depth, i = depth + 1, i + 2
    elif pair in ("}}", "]]") and depth:
      depth, i = depth - 1, i + 2
    else:
      if body[i] == "|" and depth == 0:
        parts.append(body[start:i])
        start = i + 1
      i += 1
  parts.append(body[start:])
  return parts


def template_calls(text: str, name: str) -> list[dict]:
  """Parameters of every {{name|...}} call (positional as "1", "2", ...), nested templates included.
  {{=}} and {{!}} are the wiki's escaped '=' and '|' and stay part of the value."""
  text = text.replace("{{=}}", "\x01").replace("{{!}}", "\x02")
  first = f"[{name[0].upper()}{name[0].lower()}]{re.escape(name[1:])}"
  calls = []
  for m in re.finditer(rf"\{{\{{\s*{first}\s*(?=[|}}])", text):
    end = closing_braces(text, m.end())
    if end < 0:
      continue
    params: dict[str, str] = {}
    position = 0
    for part in split_params(text[m.end() : end])[1:]:
      key, eq, value = part.partition("=")
      if eq and re.fullmatch(r"\s*\w+\s*", key):
        key, value = key.strip(), value.strip()
      else:
        position += 1
        key, value = str(position), part.strip()
      params[key] = value.replace("\x01", "=").replace("\x02", "|")
    calls.append(params)
  return calls


def page_kind(title: str, ns: int, text: str) -> str:
  """Kind from the page's API template (outside comments); else from its title prefix.
  Only the main, API, Event and Category (systems) namespaces hold API pages."""
  if title in INDEX_PAGES:
    return "index"
  if ns == 828:
    return "module"
  if ns not in (0, 14, 3000, 3004):
    return "other"
  text = strip_noncontent(text)
  for template, kind in KIND_TEMPLATES:
    if re.search(rf"\{{\{{\s*[{template[0]}{template[0].lower()}]{re.escape(template[1:])}\s*[|}}]", text):
      return kind if ns != 14 or kind == "system" else "other"
  if ns == 14:
    return "other"
  for prefix, kind in TITLE_KINDS:
    if title.startswith(prefix):
      return kind
  return {3000: "function", 3004: "event"}.get(ns, "other")


def title_body(title: str) -> str:
  """'API:Foo Bar', 'API Foo Bar' and 'Event:FOO' -> the part after the API/Event prefix."""
  for prefix in ("API:", "API ", "Event:"):
    if title.startswith(prefix) and not title.startswith("API types/"):
      return title[len(prefix) :]
  return title


def api_name(title: str, kind: str = "", classes: frozenset[str] | set[str] = frozenset()) -> str:
  """The name addons use, following Module:Wowapi/src/page: spaces become '_' for functions and
  events; 'Class Method' becomes 'Class:Method' for method pages, or when Class is a known widget,
  ScriptObject or mixin (so 'API EJ GetCurrentInstance' stays EJ_GetCurrentInstance). Type and
  overview pages keep their title."""
  if kind in NON_API_KINDS or title.startswith(KEEP_TITLE_PREFIXES):
    return title
  for prefix in NAME_PREFIXES:
    if title.startswith(prefix):
      rest = title[len(prefix) :]
      return f"/{rest}" if prefix == "MACRO " else rest
  body = re.sub(r"\(.*\)$", "", title_body(title)).strip()
  owner = body.split(" ", 1)[0]
  is_method = kind in ("widget-method", "intrinsic-method") or (
    kind not in ("function", "lua-function", "event")
    and re.fullmatch(r"[A-Za-z0-9]+ [A-Za-z0-9]+", body) is not None
    and (owner in classes or owner.endswith("Mixin"))
  )
  return body.replace(" ", ":", 1) if is_method else body.replace(" ", "_")


def is_api_shaped(title: str) -> bool:
  """Could this redirect title be an API name? ('RegisterUnitWatch', 'SPELL AURA APPLIED', 'API X')
  as opposed to guide titles like 'HOWTO: Use OnUpdate Correctly'."""
  return in_scope(title) or bool(
    re.fullmatch(r"[A-Za-z_]\w*(?:[.:][A-Za-z_]\w*)*", title) or re.fullmatch(r"[A-Z0-9_]+(?: [A-Z0-9_]+)+", title)
  )


def relation(name: str, target: str) -> str:
  """How a redirect's own name relates to the page it lands on."""
  if name == target:
    return "same-name"
  if name.lower() == target.lower():
    return "case"
  tail = re.split(r"[.:]", name)[-1]
  target_tail = re.split(r"[.:]", target)[-1]
  if tail.lower() == target_tail.lower():
    return "unqualified" if tail == name else "moved"
  return "renamed"


FACT_TEMPLATES = (
  "wowapi", "widgetmethod", "intrinsicmethod", "wowapievent", "wowapitype", "deprecatedapi", "removedapi",
)


def page_facts(text: str, kind: str) -> dict:
  facts: dict = {}
  sigs = [c.get("1", "") for c in template_calls(text, "apisig")]
  if sigs:
    facts["signatures"] = sigs
  for template in FACT_TEMPLATES:
    calls = [c for c in template_calls(text, template) if c]
    if calls:
      facts[template] = calls[0]
  restricted = template_calls(text, "restrictedapi")
  if restricted:
    flags = {flag.strip() for c in restricted for flag in c.get("1", "").split(",")}
    facts["restricted"] = sorted(flags - {""})
    notes = [c["note"] for c in restricted if c.get("note")]
    if notes:
      facts["restricted_note"] = notes
  compat = [c.get("1") for c in template_calls(text, "apicompat") if kind != "index"]
  if compat:
    facts["apicompat"] = compat[0]
  return facts


def listing_entry(line: str, classes: set[str]) -> dict | None:
  """The API a list line is about: {{apilink...}}, {{api|t=e|...}} or [[API:...]], whichever comes first."""
  for m in re.finditer(r"\{\{\s*(apilink(?:\.\w+)?|api)\s*\||\[\[(API:[^|\]#]+)", line):
    if m.group(2):
      return {"name": api_name(m.group(2).replace("_", " "), classes=classes)}
    calls = template_calls(line[m.start() :], m.group(1))
    params = calls[0] if calls else {}
    if m.group(1) == "api" and params.get("t") != "e":
      continue  # {{api|...}} is a generic link; only its event form starts an event list line
    # FrameXML entries name the function in framexml= instead of the first parameter
    if name := re.sub(r"\(.*\)$", "", params.get("1") or params.get("framexml") or "").strip():
      entry = {"name": name, "type": params.get("t", "")}
      for key, field in (("arg", "args"), ("ret", "returns")):
        if key in params:
          entry[field] = params[key]
      return entry
  return None


def span_text(line: str, css_class: str) -> str:
  m = re.search(rf'<span class="{css_class}">(.*?)</span>', line)
  return m.group(1) if m else ""


def parse_listings(title: str, text: str, classes: set[str]) -> list[dict]:
  """Rows from index-style lists: one row per API at the start of a list or table line."""
  rows = []
  section = ""
  for line in strip_noncontent(text).splitlines():
    if heading := re.match(r"^(=+)(.+?)\1\s*$", line):
      section = re.sub(r"\{\{[^}]*\|([^|}]+)\}\}", r"\1", heading.group(2)).strip(" '")
      continue
    if not line.startswith((":", "|", "*")) or not (entry := listing_entry(line, classes)):
      continue
    row = {"name": entry["name"], "page": title, "section": section}
    if entry.get("type"):
      row["type"] = entry["type"]
    for field, css in (("args", "apiarg"), ("returns", "apiret")):
      if value := entry.get(field) or span_text(line, css):
        row[field] = value
    if tags := [t.strip() for c in re.findall(r"\{\{apitag\|([^}]+)\}\}", line) for t in c.split(",")]:
      row["tags"] = tags
    if compat := re.search(r"\{\{apicompat\|(0x[0-9a-fA-F]+)", line):
      row["flavors"] = flavors(int(compat.group(1), 16))
    if desc := re.search(r"(?:\}\}|\]\]|\))\s+-\s+(.+)$", line):
      row["description"] = desc.group(1).strip()
    rows.append(row)
  return rows


def flavors(mask: int) -> list[str]:
  return [label for bit, label in FLAVOR_BITS if mask & bit]


def build(out: Path) -> None:
  raw = out / "raw"
  metas = [json.loads(line) for line in (raw / "pages.jsonl").read_text(encoding="utf-8").splitlines()]
  meta = {m["title"]: m for m in metas}
  missing = json.loads((raw / "missing.json").read_text(encoding="utf-8"))
  text_of = {t: (raw / "pages" / m["file"]).read_text(encoding="utf-8") for t, m in meta.items()}
  log(f"building from {len(meta)} cached pages")

  # Data modules -> JSON.
  data_dir = out / "data"
  shutil.rmtree(data_dir, ignore_errors=True)
  modules: dict[str, object] = {}
  for title, m in meta.items():
    if m["ns"] == 828 and not m["redirect"]:
      try:
        modules[title] = parse_lua_module(text_of[title])
      except (IndexError, ValueError) as e:
        log(f"  could not parse {title}: {e}")
        continue
      path = data_dir / f"{title.split(':', 1)[1]}.json"
      path.parent.mkdir(parents=True, exist_ok=True)
      path.write_text(json.dumps(modules[title], indent=1, ensure_ascii=False), encoding="utf-8")

  def module(name: str) -> dict:
    value = modules.get(f"Module:Wowapi/data/{name}")
    return value if isinstance(value, dict) else {}

  gametype: dict[str, int] = {}
  for part in ("function", "event", "widget", "scriptobject"):
    gametype.update({k: v for k, v in module(f"gametype/{part}").items() if isinstance(v, int)})
  patches: dict[str, list[str]] = defaultdict(list)
  for title, value in modules.items():
    if m := re.match(r"Module:Wowapi/data/patch/(\w+)/", title):
      for name, versions in (value if isinstance(value, dict) else {}).items():
        patches[name].append(f"{PATCH_FLAVORS.get(m.group(1), m.group(1))} {'-'.join(map(str, versions))}")
  group_of: dict[str, list[str]] = {}
  for group in modules.get("Module:Wowapi/data/group") or []:
    if isinstance(group, list):
      for name in group:
        group_of[name] = [n for n in group if n != name]

  # Pages and redirect pages -> entries.
  def resolve(title: str) -> tuple[str, str]:
    """Final (title, fragment) after following redirect chains inside the cache."""
    fragment = ""
    for _ in range(10):
      if title not in meta or not meta[title]["redirect"]:
        break
      m = REDIRECT_RE.match(text_of[title])
      if not m:
        break
      title, frag = clean(m.group(1))
      fragment = frag or fragment
    return title, fragment

  kind_of = {t: ("redirect" if m["redirect"] else page_kind(t, m["ns"], text_of[t])) for t, m in meta.items()}

  # Owners whose 'Owner Method' titles are methods (widgets, ScriptObjects, intrinsics), as opposed
  # to functions whose name merely contains a space-turned-underscore like EJ_GetCurrentInstance.
  classes = {k.split(":")[0] for part in ("gametype/widget", "gametype/scriptobject") for k in module(part)}
  classes |= {v for v in module("scriptobject").values() if isinstance(v, str)}
  classes |= {title_body(t).split(" ")[0] for t, k in kind_of.items() if k in ("widget-method", "intrinsic-method")}
  classes |= {t.split(" ", 1)[1] for t in meta if t.startswith(("UIOBJECT ", "ScriptObject ", "INTRINSIC "))}
  name_of = {t: api_name(t, kind_of[t], classes) for t in meta}

  entries = []
  for title in sorted(meta):
    m = meta[title]
    entry = {
      "title": title,
      "ns": m["ns"],
      "kind": kind_of[title],
      "name": name_of[title],
      "file": f"raw/pages/{m['file']}",
      "pageid": m["pageid"],
      "revid": m["revid"],
      "timestamp": m["timestamp"],
      "categories": [c["title"].removeprefix("Category:") for c in m["categories"] if not c["hidden"]],
    }
    if m["redirect"]:
      target, fragment = resolve(title)
      target_kind = kind_of.get(target, "")
      target_name = api_name(target, target_kind, classes)
      if title_body(title) == title_body(target):
        entry["name"] = name_of[title] = target_name  # same title in old/new form: same API
      entry["redirect"] = {
        "target": target,
        "fragment": fragment,
        "target_exists": target in meta,
        "target_name": target_name,
        "relation": relation(entry["name"], target_name),
      }
    else:
      entry["redirects"] = m["redirects"]
      facts = page_facts(strip_noncontent(text_of[title]), entry["kind"])
      if facts:
        entry["facts"] = facts
    entries.append(entry)

  # Index lists and UIOBJECT method lists.
  listings = []
  for title in sorted(meta):
    if kind_of[title] in ("index", "widget", "intrinsic") and meta[title]["ns"] != 828:
      listings += parse_listings(title, text_of[title], classes)

  # Names. One name can belong to pages of different kinds (UpdateWindow is a function and a
  # CVar), so lookups prefer the asked-for kind, then API kinds.
  pages_by_name: dict[str, list[tuple[str, str]]] = defaultdict(list)  # name -> [(kind, title)]
  for e in sorted(entries, key=lambda e: e["kind"] not in API_KINDS):
    if e["kind"] in NAMED_KINDS:
      pages_by_name[e["name"]].append((e["kind"], e["title"]))
  for e in entries:
    if "redirect" in e and kind_of.get(e["redirect"]["target"]) in NAMED_KINDS:
      pages_by_name[e["name"]].append((kind_of[e["redirect"]["target"]], e["redirect"]["target"]))

  def find_page(name: str, kind: str = "") -> str:
    found = pages_by_name.get(name, [])
    return next((t for k, t in found if k == kind), found[0][1] if found else "")

  tags_of: dict[str, set[str]] = defaultdict(set)
  for row in listings:
    tags_of[row["name"]].update(row.get("tags", []))
  for e in entries:
    tags_of[e["name"]].update(e.get("facts", {}).get("restricted", []))

  def name_columns(name: str, kind: str) -> tuple[str, str]:
    """Flavors and tags; both describe API functions/events/methods only."""
    if kind not in API_KINDS:
      return "", ""
    mask = gametype.get(name)
    return (",".join(flavors(mask)) if mask is not None else "", ",".join(sorted(tags_of.get(name, ()))))

  rows = []
  named = set()
  for e in entries:
    if e["kind"] in ("module", "index", "other", "system"):
      continue
    if "redirect" in e and (e["ns"] not in (0, 3000, 3004) or not is_api_shaped(e["title"])):
      continue  # guide redirects like 'HOWTO: Use OnUpdate Correctly' are not API names
    named.add(e["name"])
    if "redirect" in e:
      r = e["redirect"]
      status = "section" if r["fragment"] else "redirect"
      target = r["target"] + (f"#{r['fragment']}" if r["fragment"] else "")
      target_kind = kind_of.get(r["target"], "")
      flavor, tags = name_columns(e["name"] if e["name"] in gametype else r["target_name"], target_kind)
      detail = f"lands on {r['target_name']}" + ("" if r["target_exists"] else " (target not on wiki)")
      rows.append((e["name"], status, e["kind"], e["title"], target, r["relation"], flavor, tags, detail))
    else:
      flavor, tags = name_columns(e["name"], e["kind"])
      detail = "; ".join(f"aka {n}" for n in group_of.get(e["name"], []))
      rows.append((e["name"], "page", e["kind"], e["title"], "", "", flavor, tags, detail))

  # A method with no page of its own is often documented on another class, e.g. the wiki's data
  # says ScriptRegion:ClearAllPoints while the page is ScriptRegionResizing:ClearAllPoints.
  method_pages: dict[str, list[str]] = defaultdict(list)
  for e in entries:
    if e["kind"] in ("widget-method", "intrinsic-method") and ":" in e["name"]:
      method_pages[e["name"].split(":", 1)[1]].append(e["name"])

  def documented_elsewhere(name: str, kind: str) -> tuple[str, str, str]:
    """(target page, relation, detail) for a name without its own page; empty when unknown."""
    if page := find_page(name, kind):
      return page, "dead link", ""
    cls, sep, method = name.partition(":")
    others = sorted(
      (n for n in method_pages.get(method, []) if n != name), key=lambda n: (not n.startswith(cls), n)
    ) if sep else []
    if not others:
      return "", "", ""
    return find_page(others[0], "widget-method"), "same-method", "same method documented as " + ", ".join(others)

  def kind_from_title(title: str, name: str) -> str:
    if title.startswith("Event:"):
      return "event"
    if title.startswith(("API:", "API ")) and ":" in name:
      return "widget-method"
    return next((kind for prefix, kind in TITLE_KINDS if title.startswith(prefix)), "function")

  red_names = set()
  for title, refs in missing.items():
    if not in_scope(title):
      continue
    name = api_name(title, classes=classes)
    kind = kind_from_title(title, name)
    target, rel, detail = documented_elsewhere(name, kind)
    flavor, tags = name_columns(name, kind)
    detail = "; ".join(d for d in (detail, "referenced from " + ", ".join(refs) if refs else "") if d)
    rows.append((name, "red-link", kind, title, target, rel, flavor, tags, detail))
    red_names.add(name)

  sources: dict[str, set[str]] = defaultdict(set)
  source_kind: dict[str, str] = {}
  for part, kind in DATA_KINDS.items():
    for name in module(part):
      sources[name].add(part)
      source_kind.setdefault(name, kind)
  for row in listings:
    sources[row["name"]].add(f"listed on {row['page']}")
    source_kind.setdefault(row["name"], LISTING_KINDS.get(row.get("type", ""), ""))
  for name in sorted(sources):
    if name in named or name in red_names or name in pages_by_name:
      continue
    kind = source_kind.get(name) or ("widget-method" if ":" in name else "")
    target, rel, detail = documented_elsewhere(name, kind)
    flavor, tags = name_columns(name, kind)
    detail = "; ".join(d for d in (detail, "; ".join(sorted(sources[name]))) if d)
    rows.append((name, "no-page", kind, "", target, rel, flavor, tags, detail))

  for name in list(patches):
    patches[name].sort()
  rows.sort(key=lambda r: (r[0].lower(), r[1], r[3]))

  # Write outputs.
  with (out / "entries.jsonl").open("w", encoding="utf-8") as f:
    for e in entries:
      if e["name"] in patches:
        e["patches"] = patches[e["name"]]
      if e["name"] in gametype:
        e["flavors"] = flavors(gametype[e["name"]])
      f.write(json.dumps(e, ensure_ascii=False) + "\n")
  with (out / "listings.jsonl").open("w", encoding="utf-8") as f:
    for row in listings:
      f.write(json.dumps(row, ensure_ascii=False) + "\n")
  with (out / "names.tsv").open("w", encoding="utf-8") as f:
    f.write("name\tstatus\tkind\ttitle\ttarget\trelation\tflavors\ttags\tdetail\n")
    for row in rows:
      f.write("\t".join(str(c).replace("\t", " ").replace("\n", " ") for c in row) + "\n")

  status_counts: dict[str, int] = defaultdict(int)
  for row in rows:
    status_counts[row[1]] += 1
  kind_counts: dict[str, int] = defaultdict(int)
  for e in entries:
    kind_counts[e["kind"]] += 1
  manifest = {
    "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "fetch": json.loads((raw / "fetch.json").read_text(encoding="utf-8")),
    "builds": module("cfg").get("build", {}),
    "entries_by_kind": dict(sorted(kind_counts.items())),
    "names_by_status": dict(sorted(status_counts.items())),
    "listings": len(listings),
    "data_modules": sorted(t.split(":", 1)[1] for t in modules),
  }
  (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
  log(f"build done: {manifest['entries_by_kind']} {manifest['names_by_status']}")


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("stage", nargs="?", choices=("all", "fetch", "build"), default="all")
  parser.add_argument("--out", type=Path, default=Path(__file__).parent / "dump")
  parser.add_argument("--delay", type=float, default=0.5, help="seconds between API requests")
  parser.add_argument("--network-mode", choices=("proxy", "local"), default="proxy")
  parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE, help="where PROXY_* come from")
  parser.add_argument("--proxy-ports", default=DEFAULT_PROXY_PORTS, help="port or range, e.g. 8001-8010")
  args = parser.parse_args()

  if args.stage in ("all", "fetch"):
    proxies: list[str] = []
    if args.network_mode == "proxy":
      load_env_file(args.env_file)
      proxies = proxy_urls(args.proxy_ports)
      log(f"network: {len(proxies)} proxy ports")
    else:
      log("network: direct")
    fetch(WikiClient(args.delay, proxies), args.out / "raw")
  if args.stage in ("all", "build"):
    build(args.out)


if __name__ == "__main__":
  main()
