# /// script
# requires-python = ">=3.12"
# dependencies = ["requests"]
# ///
"""Generate a LuaLS annotation library for WoW Classic Era and Forever.

Sources (`uv run generate.py sources` clones or updates them under sources/):
  ui-<flavor>    Gethe/wow-ui-source, Blizzard_APIDocumentationGenerated: typed functions,
                 structures, enums, callbacks and event payloads as Blizzard documents them
  bir-<flavor>   Ketho/BlizzardInterfaceResources: what each client really has (GlobalAPI,
                 WidgetAPI, Events, LuaEnum, CVars). This decides what goes into the library.
  ketho          Ketho/vscode-wow-api (MIT): hand-maintained Type/, Lua/ and Widget/ annotations
  ../dump        wiki_dump.py output: descriptions, restriction tags, and the signatures of
                 functions Blizzard does not document (UnitAura, GetSpellInfo, ...)

Output (WoW-API/library/):
  Security/Security.lua docs/Security.md (how secure execution, taint, protected frames and secret
                        values work, written from the wiki) followed by a generated summary, the
                        SecureTemplate type and every restricted function and widget method
                        (#protected, #hwevent, #nocombat, #secureframe, Blizzard's IsProtectedFunction,
                        HasRestrictions, Secret* flags, ...), moved here from the files below
  API/<System>.lua      functions from Blizzard's documentation, one file per Blizzard system
  API/Global.lua        global functions Blizzard's documentation does not cover (documented on the wiki)
  API/Deprecated.lua    Lua fallbacks from the Blizzard_Deprecated addons a client loads (UnitAura
                        on Era), as @deprecated with the C_ function to use instead
  API/Undocumented.lua  functions the clients have that nobody documents
  FrameXML/             Ketho's annotations of Blizzard's Lua utilities (ColorMixin, MenuUtil, ...),
                        only the files whose globals exist in Era or Forever
  Data/                 Enum.lua (Enum, Constants, LE_*), Event.lua (FrameEvent), CVar.lua
  Widget/<Class>.lua    widget classes and methods as the clients define them
  Type/                 Ketho's types, plus generated Structure, Callback, Namespace and
                        Undefined (types referenced somewhere but defined nowhere) files
  Lua/                  Lua 5.1 environment (Ketho)

Alongside the library, reference/ gets one markdown file per function, widget method and event for AI
tools and reading: facts in front matter, the LuaLS annotation, the files of Blizzard's UI source that
use it (from the --usage-branch checkout) and the converted wiki page (details, examples, patch
changes). See reference.py.

Both are written to the gitignored WoW-API/ folder (WoW-API/library, WoW-API/reference), so it can be
copied or linked into an addon workspace as one unit.

Flavors: the library covers everything either client has. Anything only one client has is
tagged in its doc comment with `---**Era only**` or `---**Forever only**`; where both have it
with different Blizzard signatures, Era's is the main one and Forever's an @overload.

Run:
  uv run generate.py sources                 clone/update the sources (sparse, shallow)
  uv run generate.py                         build WoW-API/library and WoW-API/reference
  uv run generate.py --usage-branch classic_era   'Used in wow-ui-source' from another branch
                                             (run `sources --usage-branch <branch>` first for
                                             branches other than classic_era and forever)
  uv run generate.py --usage-limit 100       list more files per reference entry
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path

from reference import Entry, UsageIndex, scan_usage, write_reference
from wiki_dump import (
  LuaTableParser,
  clean,
  closing_braces,
  parse_lua_module,
  split_params,
  strip_noncontent,
  template_calls,
)

ROOT = Path(__file__).parent
SOURCES = ROOT / "sources"
DUMP = ROOT / "dump"
EXPORT = ROOT / "WoW-API"  # everything generated, in one portable (gitignored) folder
OUT = EXPORT / "library"  # LuaLS annotations, for the language server
REFERENCE = EXPORT / "reference"  # markdown per function/method/event, for AI and reading (reference.py)
# Which Gethe/wow-ui-source branch the reference's "Used in wow-ui-source" lists are built from.
# Override with --usage-branch (classic_era, classic, live, ...); `sources` clones branches it lacks.
USAGE_BRANCH = "forever"
USAGE_LIMIT = 50  # files listed per entry, most uses first
GUIDE_TITLES = [
  "Secure Execution and Tainting", "SecureTemplates", "SecureStateDriver", "Object security", "Secret Values",
  "SecureHandlers", "SecureActionButtonTemplate", "SecureUnitButtonTemplate", "SecureHandlerStateTemplate",
  "RestrictedEnvironment",
]
WIKI_URL = "https://warcraft.wiki.gg/wiki/"
GLOBAL_FILE = "API/Global.lua"  # global functions Blizzard's documentation does not cover

FLAVORS = {"era": "classic_era", "forever": "forever"}  # our name -> branch in both repos
FLAVOR_LABEL = {"era": "Era", "forever": "Forever"}
# Game types a client matches in TOC [AllowLoadGameType ...] / [ExcludeLoadGameType ...] gates. Forever
# was developed as 'camelot' and belongs to the mainline family: its TOCs say
# '[AllowLoadGameType mainline] [ExcludeLoadGameType camelot]'. Era is vanilla in the classic family.
GAME_TYPES = {"era": {"vanilla", "classic"}, "forever": {"camelot", "mainline"}}
# TOC path tokens: '[Game]\Blizzard_CollectionsConstants.lua' loads Camelot/..., '[Family]\...' Mainline/...
TOC_TOKENS = {"era": {"Game": "Vanilla", "Family": "Classic"}, "forever": {"Game": "Camelot", "Family": "Mainline"}}
BLIZZARD_DOCS = "Interface/AddOns/Blizzard_APIDocumentationGenerated"
SOURCE_REPOS = [
  # (directory, repo, branch, sparse paths); the UI source is checked out whole (~50 MB per branch):
  # API docs, deprecation fallbacks, TOCs, and the Lua/XML scanned for "Used in wow-ui-source"
  *((f"ui-{f}", "Gethe/wow-ui-source", b, ["/Interface/*"]) for f, b in FLAVORS.items()),
  *((f"bir-{f}", "Ketho/BlizzardInterfaceResources", b, ["/Resources/*.lua"]) for f, b in FLAVORS.items()),
  ("ketho", "Ketho/vscode-wow-api", "master", ["/Annotations/Core/*", "/LICENSE"]),
]

LUA_BUILTIN_TYPES = {
  "nil", "any", "boolean", "string", "number", "integer", "function", "table", "thread", "userdata",
  "lightuserdata", "unknown", "true", "false", "self",
}
LUA_KEYWORDS = {
  "and", "break", "do", "else", "elseif", "end", "false", "for", "function", "if", "in", "local", "nil",
  "not", "or", "repeat", "return", "then", "true", "until", "while",
}
# Blizzard documentation and wiki type spellings -> Lua types; everything else is kept as a type name.
TYPE_ALIASES = {
  "bool": "boolean", "Boolean": "boolean", "cstring": "string", "stringView": "string", "String": "string",
  "func": "function", "Function": "function", "Number": "number", "Integer": "integer", "Table": "table",
  "luaIndex": "integer", "Variable": "any",
}


# --- Model -----------------------------------------------------------------------------------


@dataclass
class Param:
  name: str
  type: str = "any"
  optional: bool = False
  desc: str = ""


@dataclass
class Func:
  name: str  # 'UnitAura', 'C_Item.GetItemInfo', 'Frame:SetPoint'
  params: list[Param] = field(default_factory=list)
  returns: list[Param] = field(default_factory=list)
  doc: list[str] = field(default_factory=list)  # comment lines, without the leading '---'
  overloads: list[str] = field(default_factory=list)  # 'fun(...)' strings


def flavor_tag(present: set[str]) -> str:
  """'**Era only**' when one client lacks it, else ''."""
  if len(present) == 1:
    return f"**{FLAVOR_LABEL[next(iter(present))]} only**"
  return ""


def lua_name(name: str, taken: set[str]) -> str:
  """A legal, unique Lua parameter name."""
  if name == "...":
    return name
  words = re.findall(r"[A-Za-z_]\w*", name)
  name = "_or_".join(words) if words else "arg"
  if name in LUA_KEYWORDS:
    name += "_"
  base, n = name, 2
  while name in taken:
    name, n = f"{base}{n}", n + 1
  taken.add(name)
  return name


def clean_type(raw: str) -> tuple[str, bool]:
  """Wiki/Blizzard type text -> (LuaLS type, nilable). 'number,string' -> 'number|string', 'X?' -> nilable."""
  raw = raw.strip()
  nilable = raw.endswith("?")
  parts = []
  for part in re.split(r"[,|/]| or ", raw.rstrip("?")):
    part = part.strip()
    array = part.endswith("[]")
    part = TYPE_ALIASES.get(part.removesuffix("[]"), part.removesuffix("[]"))
    if re.fullmatch(r"[A-Za-z_][\w.]*", part):
      parts.append(part + ("[]" if array else ""))
  return ("|".join(parts) or "any", nilable)


# --- Rendering -------------------------------------------------------------------------------


def one_line(text: str) -> str:
  r"""Doc text must stay on its comment line: show control characters as escapes (\n, \t)."""
  return re.sub(r"[\x00-\x1f]", lambda m: CONTROL_ESCAPES.get(m.group(0), f"\\{ord(m.group(0))}"), text)


CONTROL_ESCAPES = {"\n": "\\n", "\r": "\\r", "\t": "\\t"}


def doc_lines(doc: list[str]) -> list[str]:
  """Comment lines, without repeating a line (Blizzard and the wiki often say the same thing)."""
  seen, out = set(), []
  for line in map(one_line, doc):
    key = re.sub(r"\W+", "", line.lower())
    if key and key in seen:
      continue
    seen.add(key)
    out.append(f"---{line}" if line else "---")
  return out


def lua_literal(value) -> str:
  if isinstance(value, bool):
    return "true" if value else "false"
  if isinstance(value, str):
    return json.dumps(value)
  return repr(value)


def render_func(f: Func) -> str:
  lines = doc_lines(f.doc)
  for p in f.params:
    opt = "?" if p.optional and p.name != "..." else ""
    lines.append(f"---@param {p.name}{opt} {p.type}" + (f" {one_line(p.desc)}" if p.desc else ""))
  for r in f.returns:
    opt = "?" if r.optional else ""
    name = "..." if r.name == "..." else r.name
    lines.append(f"---@return {r.type}{opt} {name}" + (f" # {one_line(r.desc)}" if r.desc else ""))
  lines += [f"---@overload {o}" for o in f.overloads]
  args = ", ".join(p.name for p in f.params)
  lines.append(f"function {f.name}({args}) end")
  return "\n".join(lines)


def fun_type(f: Func) -> str:
  args = ", ".join(f"{p.name}{'?' if p.optional and p.name != '...' else ''}: {p.type}" for p in f.params)
  rets = ", ".join(f"{r.type}{'?' if r.optional else ''}" for r in f.returns)
  return f"fun({args})" + (f": {rets}" if rets else "")


def write(path: Path, chunks: list[str], header: str = "") -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  body = "\n\n".join(c for c in chunks if c)
  path.write_text("---@meta _\n" + (header + "\n" if header else "") + "\n" + body + "\n", encoding="utf-8")


# --- Sources ---------------------------------------------------------------------------------


def ui_source_dir(branch: str) -> Path:
  """The wow-ui-source checkout for a branch: one of the flavors' (ui-era, ui-forever) or ui-<branch>."""
  flavor = next((f for f, b in FLAVORS.items() if b == branch), None)
  return SOURCES / (f"ui-{flavor}" if flavor else f"ui-{branch}")


def update_sources(usage_branch: str) -> None:
  SOURCES.mkdir(exist_ok=True)
  repos = list(SOURCE_REPOS)
  if not any(directory == ui_source_dir(usage_branch).name for directory, *_ in repos):
    repos.append((ui_source_dir(usage_branch).name, "Gethe/wow-ui-source", usage_branch, ["/Interface/*"]))
  for directory, repo, branch, paths in repos:
    dest = SOURCES / directory
    if not dest.exists():
      subprocess.run(
        ["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse", "--branch", branch,
         f"https://github.com/{repo}.git", dest],
        check=True,
      )
    subprocess.run(["git", "-C", dest, "sparse-checkout", "set", "--no-cone", *paths], check=True)
    subprocess.run(["git", "-C", dest, "pull", "-q", "--depth", "1"], check=True)
    print(f"{directory}: {commit(dest)}", file=sys.stderr)


def commit(path: Path) -> str:
  return subprocess.run(
    ["git", "-C", path, "log", "-1", "--format=%h %cs"], capture_output=True, text=True, check=True
  ).stdout.strip()


def read_lua(path: Path):
  return parse_lua_module(path.read_text(encoding="utf-8"))


@dataclass
class Client:
  """What one client (flavor) has, from BlizzardInterfaceResources and Blizzard's docs."""

  flavor: str
  globals: set[str]
  lua_api: set[str]
  widgets: dict  # class -> {inherits, methods, handlers}
  events: dict[str, list[str]]  # system -> event names
  enums: dict  # Enum table
  constants: dict
  le: dict[str, int]  # LE_* globals
  cvars: dict  # name -> [default, category, account, character, (secure,) help]
  systems: list[dict]  # Blizzard documentation tables
  lua_globals: set[str]  # functions and mixins Blizzard's Lua UI defines (FrameXML)
  deprecated: dict[str, "Deprecated"]  # Lua fallbacks from the Blizzard_Deprecated* addons this client loads
  frames: set[str]  # named global frames (GameTooltip, Minimap, UIParent, ...)
  templates: dict  # virtual XML template -> {type = widget type}


@dataclass
class Deprecated:
  file: str  # 'Blizzard_Deprecated/Deprecated_1_15_8.lua'
  args: list[str] | None  # None for an alias ('X = C_Ns.Fn'), which takes the replacement's signature
  replacement: str  # the C_ function the fallback calls or aliases, if any


def loads_for(allow: str | None, exclude: str | None, game_types: set[str]) -> bool:
  """Whether 'AllowLoadGameType <allow>' / 'ExcludeLoadGameType <exclude>' lets a client load something."""
  def types(spec: str) -> set[str]:
    return {t.strip() for t in spec.split(",")}

  return (allow is None or bool(types(allow) & game_types)) and (exclude is None or not types(exclude) & game_types)


def toc_files(addon: Path, game_types: set[str], tokens: dict[str, str]) -> list[Path]:
  """Lua files an addon's .toc loads for a client, honouring Allow/ExcludeLoadGameType gates and
  filling path tokens like 'Deprecated_Specialization_[Game].lua'."""
  toc = next(addon.glob("*.toc"), None)
  if toc is None:
    return []
  text = toc.read_text(encoding="utf-8")
  header = {k: v for k, v in re.findall(r"^## (AllowLoadGameType|ExcludeLoadGameType):\s*(.+)$", text, re.MULTILINE)}
  if not loads_for(header.get("AllowLoadGameType"), header.get("ExcludeLoadGameType"), game_types):
    return []
  files = []
  for m in re.finditer(r"^([^#\s].*?\.lua)((?:\s*\[[^\]]+\])*)\s*$", text, re.MULTILINE):
    gates = dict(re.findall(r"\[(AllowLoadGameType|ExcludeLoadGameType) ([^\]]+)\]", m.group(2)))
    if loads_for(gates.get("AllowLoadGameType"), gates.get("ExcludeLoadGameType"), game_types):
      path = re.sub(r"\[(\w+)\]", lambda t: tokens.get(t.group(1), t.group(0)), m.group(1))
      files.append(addon / path.replace("\\", "/"))
  return files


SHIM_RE = re.compile(
  r"^([ \t]*)(?:function\s+([\w.:]+)\s*\(([^)]*)\)|([\w.]+)\s*=\s*function\s*\(([^)]*)\))", re.MULTILINE
)
ALIAS_RE = re.compile(r"^[ \t]*([\w.]+)\s*=\s*([A-Za-z_][\w.]*)\s*;?\s*$", re.MULTILINE)


def load_deprecated(flavor: str, c_functions: set[str]) -> dict[str, Deprecated]:
  """Fallbacks the Blizzard_Deprecated* addons define for this client: 'X = function(...)' wrappers
  and 'X = C_Ns.Fn' aliases of C functions the client has."""
  out: dict[str, Deprecated] = {}
  addons = SOURCES / f"ui-{flavor}" / "Interface/AddOns"
  for addon in sorted(addons.glob("Blizzard_Deprecated*")):
    for path in toc_files(addon, GAME_TYPES[flavor], TOC_TOKENS[flavor]):
      if not path.is_file():
        print(f"{flavor}: {addon.name} lists {path.name}, which is not in the source", file=sys.stderr)
        continue
      text = path.read_text(encoding="utf-8")
      file = path.relative_to(addons).as_posix()
      for m in SHIM_RE.finditer(text):
        name, args = (m.group(2), m.group(3)) if m.group(2) else (m.group(4), m.group(5))
        end = re.search(rf"^{re.escape(m.group(1))}end\b", text[m.end() :], re.MULTILINE)  # same indentation
        body = text[m.end() : m.end() + end.start()] if end else ""
        call = re.search(r"\b(C_\w+\.\w+)\s*\(", body)
        out[name] = Deprecated(file, [a.strip() for a in args.split(",") if a.strip()], call.group(1) if call else "")
      for m in ALIAS_RE.finditer(text):
        if m.group(2) in c_functions:
          out.setdefault(m.group(1), Deprecated(file, None, m.group(2)))
  return out


def load_client(flavor: str) -> Client:
  res = SOURCES / f"bir-{flavor}" / "Resources"
  global_api = read_lua(res / "GlobalAPI.lua")
  framexml = read_lua(res / "FrameXML.lua")
  enum_src = (res / "LuaEnum.lua").read_text(encoding="utf-8")
  enum_tables = parse_lua_module(enum_src)
  systems = []
  for path in sorted((SOURCES / f"ui-{flavor}" / BLIZZARD_DOCS).glob("*.lua")):
    text = path.read_text(encoding="utf-8")
    if m := re.search(r"^local \w+ =\s*(\{)", text, re.MULTILINE):
      parser = LuaTableParser(text)
      parser.i = m.start(1)
      doc = parser.value()
      doc["_file"] = path.stem.removesuffix("Documentation")
      systems.append(doc)
  return Client(
    flavor=flavor,
    globals=set(global_api["GlobalAPI"]),
    lua_api=set(global_api["LuaAPI"]),
    widgets=read_lua(res / "WidgetAPI.lua"),
    events=read_lua(res / "Events.lua"),
    enums=enum_tables.get("Enum", {}),
    constants=enum_tables.get("Constants", {}),
    le={m.group(1): int(m.group(2)) for m in re.finditer(r"^(\w+)\s*=\s*(-?\d+)\s*$", enum_src, re.MULTILINE)},
    cvars=read_lua(res / "CVars.lua")["CVars"]["var"],
    systems=systems,
    lua_globals=set(framexml["FrameXML"]) | set(framexml["LoadOnDemand"]) | set(read_lua(res / "Mixins.lua")),
    deprecated=load_deprecated(flavor, set(global_api["GlobalAPI"])),
    frames=set().union(*read_lua(res / "Frames.lua").values()),  # {Frames, LoadOnDemand}
    templates=read_lua(res / "Templates.lua"),
  )


# --- Blizzard documentation ------------------------------------------------------------------


class BlizzardTypes:
  """Turns Blizzard documentation types into LuaLS types."""

  def __init__(self, clients: list[Client]):
    self.enums = {n for c in clients for n in c.enums}
    self.structures: dict[str, tuple[dict, set[str]]] = {}  # name -> (table, flavors)
    self.callbacks: dict[str, tuple[dict, set[str]]] = {}
    for c in clients:
      for system in c.systems:
        for table in system.get("Tables", []) or []:
          kind = {"Structure": self.structures, "CallbackType": self.callbacks}.get(table.get("Type"))
          if kind is not None:
            kind.setdefault(table["Name"], (table, set()))[1].add(c.flavor)

  def lua(self, f: dict) -> str:
    t = f.get("Type", "any")
    if t == "table" and f.get("InnerType"):
      return self.lua({"Type": f["InnerType"]}) + "[]"
    if f.get("Mixin"):
      return f["Mixin"]
    if t in self.enums:
      return f"Enum.{t}"
    return TYPE_ALIASES.get(t, t)

  def param(self, f: dict, taken: set[str]) -> Param:
    desc = " ".join(f.get("Documentation", []) or [])
    if "Default" in f:
      desc = (desc + f" (default: {lua_literal(f['Default'])})").strip()
    return Param(lua_name(f["Name"], taken), self.lua(f), bool(f.get("Nilable")) or "Default" in f, desc)

  def func(self, fn: dict, owner: str, sep: str = ".") -> Func:
    taken: set[str] = set()
    return Func(
      name=f"{owner}{sep}{fn['Name']}" if owner else fn["Name"],
      params=[self.param(a, taken) for a in fn.get("Arguments", []) or []],
      returns=[self.param(r, set()) for r in fn.get("Returns", []) or []],
      doc=[d for d in fn.get("Documentation", []) or [] if d],
    )


# --- Wiki ------------------------------------------------------------------------------------


@dataclass
class WikiPage:
  title: str
  text: str
  facts: dict
  tags: set[str]
  aliases: list[str] = field(default_factory=list)  # titles redirecting here


def load_wiki() -> tuple[dict[str, WikiPage], dict[str, str], dict[str, set[str]]]:
  """(page by API name, redirect name -> target page title, tags by name)."""
  tags: dict[str, set[str]] = defaultdict(set)
  for line in (DUMP / "listings.jsonl").open(encoding="utf-8"):
    row = json.loads(line)
    tags[row["name"]].update(row.get("tags", []))
  pages: dict[str, WikiPage] = {}
  redirects: dict[str, str] = {}
  by_title: dict[str, WikiPage] = {}
  for line in (DUMP / "entries.jsonl").open(encoding="utf-8"):
    e = json.loads(line)
    if "redirect" in e:
      if e["redirect"]["target_exists"]:
        redirects.setdefault(e["name"], e["redirect"]["target"])
      continue
    if e["kind"] in ("function", "removed-function", "framexml-function", "lua-function", "widget-method", "event"):
      page = WikiPage(e["title"], (DUMP / e["file"]).read_text(encoding="utf-8"), e.get("facts", {}), set())
      page.tags = set(page.facts.get("restricted", [])) | tags.get(e["name"], set())
      page.aliases = [r["title"] for r in e.get("redirects", [])]
      pages.setdefault(e["name"], page)
      by_title[e["title"]] = page
  return pages, redirects, tags


def wiki_url(title: str) -> str:
  return WIKI_URL + title.replace(" ", "_")


def plain(text: str) -> str:
  """Wiki markup -> readable one-line text."""
  text = re.sub(r"\{\{(?:api|apiname|apitype)\|(?:t=\w+\|)?([^|}]+)[^}]*\}\}", r"\1", text)
  text = re.sub(r"\{\{[^{}]*\}\}", "", text)
  text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)
  text = re.sub(r"\[https?://\S+ ([^\]]+)\]", r"\1", text)
  text = re.sub(r"<code>(.*?)</code>", r"`\1`", text)
  text = re.sub(r"<[^>]+>|'''?", "", text)
  return re.sub(r"\s+", " ", text).strip()


def drop_templates(text: str) -> str:
  """Remove every {{...}} (nested, multi-line) after turning link templates into their text."""
  text = re.sub(r"\{\{(?:api|apiname|apitype)\|(?:t=\w+\|)?([^|{}]+)[^{}]*\}\}", r"\1", text)
  while (start := text.find("{{")) >= 0:
    end = closing_braces(text, start + 2)
    text = text[:start] + (text[end + 2 :] if end >= 0 else "")
  return text


def description(text: str) -> list[str]:
  """The opening paragraph of a page, before the first heading."""
  lines = []
  for line in drop_templates(strip_noncontent(text).split("\n==")[0]).splitlines():
    stripped = line.strip()
    if re.fullmatch(r"(\{\{[^{}]*\}\}\s*)*", stripped) or stripped.startswith(("{{apisig", "{|", "|", "!")):
      if lines:
        break
      continue
    if text_line := plain(stripped.lstrip(":*# ")):
      lines.append(text_line)
  return lines[:3]


BRACKET_DEPTH = {"(": 1, "[": 1, ")": -1, "]": -1}


@dataclass
class SigArg:
  """One argument of a wiki signature."""

  names: list[str]  # the name and its alternatives: 'itemId or itemName or itemLink'
  optional: bool = False  # may be nil or left off the end: 'a [, b]', 'a{, b}', 'b?'
  omittable: bool = False  # may be left out, shifting the rest: 'hooksecurefunc([tbl,] functionName, hook)'
  vararg: bool = False  # '...', '...buttons'


def signature_args(args: str) -> list[SigArg]:
  """Parse the many ways the wiki marks optional arguments:
  'unit, index [, filter]', 'a [, b [, c]]', 'point [, relativeTo] [, x, y]', '[name [, template]]',
  '[tbl,] functionName, hook', 'slot, onOff{, exclusive}', 'guid?', 'itemID or itemLink [, slot]',
  '"spellName" or spellId', 'text, ...', '...buttons'. Unbalanced brackets are tolerated."""
  args = args.replace("{", "[").replace("}", "]")
  omittable = {label.strip() for label in re.findall(r"\[\s*([^\[\],]+?)\s*,\s*\]", args)}  # '[tbl,]'
  out, depth, current, optional = [], 0, "", False
  for ch in args + ",":
    if ch == "[":
      depth += 1
    elif ch == "]":
      depth = max(depth - 1, 0)
    elif ch == ",":
      if label := current.strip():
        out.append(sig_arg(label, optional, label in omittable))
      current = ""
    else:
      if not current.strip() and not ch.isspace():
        optional = depth > 0
      current += ch
  return out


def sig_arg(label: str, optional: bool, omittable: bool) -> SigArg:
  label = label.strip().strip("\"'")
  if label.endswith("?"):
    label, optional = label[:-1], True
  if label.startswith("..."):
    return SigArg([label[3:].strip() or "..."], optional, omittable, vararg=True)
  names = [n.strip().strip("\"'") for n in re.split(r"\s+or\s+|\s*\|\s*", label) if n.strip().strip("\"'")]
  return SigArg(names or [label], optional, omittable)


def sig_params(
  args: list[SigArg], info: dict[str, tuple[str, bool, str]] | None = None
) -> tuple[list[Param], list[bool]]:
  """Lua parameters for parsed signature arguments, typed from the Arguments section where it
  names them; alternatives get the union of their types. Also returns which ones are omittable."""
  info = info or {}
  taken: set[str] = set()
  params = []
  for arg in args:
    found = [info[n] for n in (*arg.names, "...") if n in info and (n != "..." or arg.vararg)]
    types = list(dict.fromkeys(part for typ, _, _ in found for part in typ.split("|") if part != "any"))
    desc = found[0][2] if found else ""
    if len(arg.names) > 1:
      desc = f"{' or '.join(arg.names)}." + (f" {desc}" if desc else "")
    optional = (arg.optional and not arg.omittable) or any(nilable for _, nilable, _ in found)
    name = "..." if arg.vararg else lua_name(arg.names[0], taken)
    params.append(Param(name, "|".join(types) or "any", optional, desc))
  return params, [arg.omittable for arg in args]


def without_omitted(f: Func, omittable: list[bool]) -> str:
  """The @overload for calling f with its omittable leading arguments left out."""
  return fun_type(Func(f.name, [p for p, o in zip(f.params, omittable, strict=True) if not o], f.returns))


def split_signature(sig: str) -> tuple[list[tuple[str, list[SigArg]]], list[str]]:
  """An {{apisig}} -> ([(function name, args)], returns). One signature may list several calls
  sharing the returns: 'name, ... = GetSpellInfo(spell) = GetSpellInfo(index, bookType)'."""
  sig = plain(sig)
  depth, split_at = 0, -1
  for i, ch in enumerate(sig):
    depth += BRACKET_DEPTH.get(ch, 0)
    if ch == "=" and depth == 0:
      split_at = i
      break
  rets, rest = (sig[:split_at], sig[split_at + 1 :]) if split_at >= 0 else ("", sig)
  calls, i = [], 0
  while m := re.compile(r"([A-Za-z_][\w.:]*)\s*\(").search(rest, i):
    depth, j = 1, m.end()
    while j < len(rest) and depth:
      depth += {"(": 1, ")": -1}.get(rest[j], 0)
      j += 1
    calls.append((m.group(1), signature_args(rest[m.end() : j - 1])))
    i = j
  return calls, [r.strip() for r in rets.split(",") if r.strip()]


class Transcluder:
  """Expands {{:Page|args}}, and {{Template|args}} whose body is a definition list (returns
  shared by several pages, like {{AuraType|aura}}), with the cached page. Handles what those
  pages use: <onlyinclude>/<noinclude>, {{{param|default}}} and {{#if:...}}."""

  def __init__(self) -> None:
    self.files: dict[str, str] = {}
    self.bodies: dict[str, str | None] = {}
    for line in (DUMP / "raw/pages.jsonl").open(encoding="utf-8"):
      m = json.loads(line)
      self.files[m["title"]] = m["file"]

  def body(self, title: str, depth: int = 3) -> str | None:
    """What transcluding the page inserts, following redirects; None when it isn't cached."""
    if title not in self.bodies:
      self.bodies[title] = self._read(title, depth)
    return self.bodies[title]

  def _read(self, title: str, depth: int) -> str | None:
    if title not in self.files or depth == 0:
      return None
    text = (DUMP / "raw/pages" / self.files[title]).read_text(encoding="utf-8")
    if m := re.match(r"\s*#REDIRECT\s*\[\[([^\]|#]+)", text, re.IGNORECASE):
      return self._read(clean(m.group(1))[0], depth - 1)
    if "<onlyinclude>" in text:
      return "".join(re.findall(r"<onlyinclude>(.*?)</onlyinclude>", text, re.DOTALL))
    return re.sub(r"<noinclude>.*?</noinclude>|</?includeonly>", "", text, flags=re.DOTALL)

  def expand(self, text: str, depth: int = 2) -> str:
    out, i = [], 0
    while depth and (m := TEMPLATE_START.search(text, i)):
      end = closing_braces(text, m.end())
      if end < 0:
        break
      parts = split_params(text[m.end() : end])
      is_page = m.group(1) == ":"
      title = clean(parts[0])[0] if is_page else f"Template:{clean(parts[0])[0]}"
      body = self.body(title)
      out.append(text[i : m.start()])
      if is_page or (body is not None and re.search(r"^:;", body, re.MULTILINE)):
        args: dict[str, str] = {}
        for n, part in enumerate(parts[1:], 1):
          key, eq, value = part.partition("=")
          args[key.strip() if eq else str(n)] = value.strip() if eq else part.strip()
        out.append(self.expand(evaluate(body, args), depth - 1) if body is not None else "")
      else:
        out.append(text[m.start() : end + 2])  # an ordinary template ({{apitype|...}}): keep it
      i = end + 2
    out.append(text[i:])
    return "".join(out)


TEMPLATE_START = re.compile(r"\{\{\s*(:?)(?=[A-Za-z])")


def evaluate(text: str, args: dict[str, str]) -> str:
  """Fill {{{param|default}}} and resolve {{#if:cond|then|else}}."""
  text = re.sub(r"\{\{\{([^{}|]+)(?:\|([^{}]*))?\}\}\}", lambda m: args.get(m.group(1).strip(), m.group(2) or ""), text)
  while (start := text.find("{{#if:")) >= 0:
    end = closing_braces(text, start + 2)
    if end < 0:
      break
    cond, *branches = split_params(text[start + 6 : end]) + ["", ""]
    text = text[:start] + (branches[0] if cond.strip() else branches[1]) + text[end + 2 :]
  return text


DEF_RE = re.compile(r"^[:*]*;\s*([^:]+?)\s*:\s*(.*)$")
SPAN_TYPE_RE = re.compile(r'<span class="apitype">([^<]+)</span>\s*(\?)?')


def definitions(text: str, headings: tuple[str, ...]) -> dict[str, dict[str, tuple[str, bool, str]]]:
  """Name -> (type, nilable, desc) from definition lists under the given headings, keyed by the
  function a '===Name===' subsection is about ('' when the section has no subsections)."""
  out: dict[str, dict[str, tuple[str, bool, str]]] = defaultdict(dict)
  for m in re.finditer(rf"^==\s*(?:{'|'.join(headings)})\s*==\s*$(.*?)(?=^==[^=]|\Z)", text, re.MULTILINE | re.DOTALL):
    owner = ""
    for line in m.group(1).splitlines():
      if sub := re.match(r"^===+\s*(.+?)\s*===+\s*$", line):
        owner = plain(sub.group(1)).split("(")[0].strip()
        continue
      if not (d := DEF_RE.match(line)):
        continue
      name, rest = re.sub(r"^\d+\.\s*", "", plain(d.group(1)).strip()), d.group(2)  # ':;1. name : ...'
      calls = template_calls(rest, "apitype")
      if calls:
        union = "|".join(v for k, v in sorted(calls[0].items()) if k.isdigit())  # {{apitype|number|string}}
        typ, nilable = clean_type(union)
        nilable = nilable or "default" in calls[0]
        desc = rest.split("}}", 1)[-1]
      elif span := SPAN_TYPE_RE.search(rest):  # <span class="apitype">string</span>? in older templates
        typ, nilable = clean_type(span.group(1))
        nilable = nilable or bool(span.group(2))
        desc = rest[span.end() :]
      else:  # old style ';buttonID : Number - desc', ';rank : String (Optional) - desc'
        first, _, desc = rest.partition(" - ")
        word = re.fullmatch(r"\s*([A-Za-z]+\??)\s*(\([^)]*\))?\s*", first)
        typ, nilable = clean_type(word.group(1)) if word else ("any", False)
        desc = desc if _ else rest
      desc = re.sub(r"^[-:]\s*", "", plain(desc))
      # prose: '(optional, default = false)', 'Optional, will return ...'
      nilable = nilable or bool(re.search(r"\(optional\b", rest, re.IGNORECASE) or re.match(r"optional\b", desc, re.I))
      out[owner][name] = (typ, nilable, desc)
  return out


def wiki_funcs(page: WikiPage, transcluder: Transcluder, want: str = "") -> dict[str, Func]:
  """Every function a wiki page has a signature for. A name with several call forms
  (GetSpellInfo(spell) / GetSpellInfo(index, bookType)) gets the first as its signature and
  the others as @overload; other names on the same page become functions of their own. Old
  pages without {{apisig}} still show the call in the text (' a, b = UnitDefense(unit);'); that
  is used for `want` when nothing else names it."""
  own_text = re.sub(r"</?(?:onlyinclude|includeonly|noinclude)>", "", page.text)  # markers only matter when transcluded
  text = strip_noncontent(transcluder.expand(strip_noncontent(own_text)))
  args_by_owner = definitions(text, ("Arguments", "Parameters"))
  rets_by_owner = definitions(text, ("Returns",))
  signatures = [sig.get("1", "") for sig in template_calls(text, "apisig")]
  if want and not any(want in s for s in signatures):
    if m := re.search(rf"^[ :]*((?:[\w, .\[\]]+=\s*)?{re.escape(want)}\s*\([^)\n]*\))", own_text, re.MULTILINE):
      signatures.append(m.group(1))
  funcs: dict[str, Func] = {}
  for sig in signatures:
    calls, returns = split_signature(sig)
    for name, args in calls:
      short = re.split(r"[.:]", name)[-1]  # '===GetItemInfoByID===' documents C_BlackMarket.GetItemInfoByID
      arg_info = {**args_by_owner.get("", {}), **args_by_owner.get(short, {}), **args_by_owner.get(name, {})}
      ret_info = {**rets_by_owner.get("", {}), **rets_by_owner.get(short, {}), **rets_by_owner.get(name, {})}
      params, omittable = sig_params(args, arg_info)
      rets = []
      for raw in returns:
        typ, nilable, desc = ret_info.get(raw, ("any", False, ""))
        rets.append(Param("..." if raw == "..." else lua_name(raw, set()), typ, nilable, desc))
      f = Func(name.replace(":", "."), params, rets)
      if any(omittable):  # 'hooksecurefunc([tbl,] functionName, hook)': also callable without them
        f.overloads.append(without_omitted(f, omittable))
      if f.name in funcs:
        funcs[f.name].overloads += [fun_type(f), *f.overloads]
      else:
        funcs[f.name] = f
  return funcs


def wiki_doc(page: WikiPage) -> list[str]:
  doc = description(page.text)
  if page.tags:
    doc.append(" ".join(f"#{t}" for t in sorted(page.tags)))
  doc.append(f"[Documentation]({wiki_url(page.title)})")
  return doc


# --- Security --------------------------------------------------------------------------------
#
# Everything restricted goes into one file, Security/Security.lua: the hand-written document
# docs/Security.md on top, a generated summary, then the restricted functions and widget methods,
# moved there from their usual files. A function lands in the first section it matches.

SECURITY_FILE = "Security/Security.lua"
SECURITY_DOC = ROOT / "docs/Security.md"
SECURITY_SECTIONS = [
  ("tools", "Security API: taint, secure calls, combat lockdown, secret values"),
  ("protected", "Protected: secure code only (#protected, IsProtectedFunction)"),
  ("hwevent", "Hardware event required (#hwevent)"),
  ("restricted", "Usage restrictions: combat, instance, /script, group, permission, trial (HasRestrictions)"),
  ("secret", "May return secret values to tainted code (Forever)"),
  ("widget", "Widget methods restricted on protected, forbidden or anchor-restricted frames"),
]
USAGE_TAGS = {"nocombat", "noscript", "noinstance", "grouponly", "nopermission", "nofreetrial"}
WIDGET_TAGS = {"protected", "hwevent", "secureframe", "restrictedframe", "anchorfamily"} | USAGE_TAGS
SECURITY_TOOLS = re.compile(
  r"^(?:issecure\w*|forceinsecure|hooksecurefunc|securecall\w*|secureexecuterange|securecopy|InCombatLockdown"
  r"|SecureCmdOptionParse|issecret\w*|canaccess\w*|hasanysecretvalues|scrubsecretvalues|dropsecretaccess"
  r"|secretwrap|secretunwrap|GetRestrictedActionStatus|C_RestrictedActions\.\w+|C_Secrets\.\w+)$"
)
# Blizzard documentation flags shown on items; SecureHooksAllowed is information, the rest restrict.
SECURITY_FLAG_RE = re.compile(
  r"^(IsProtectedFunction|HasRestrictions|SecureHooksAllowed|RestrictedFor\w+|SecretReturns|SecretWhen\w+"
  r"|SecretIn\w+|SecretPayloads|ChecksForbiddenAspects)$"
)


def blizzard_security_flags(clients: list[Client]) -> dict[str, dict[str, set[str]]]:
  """'UnitName' / 'Frame:SetPoint' / 'ADDON_ACTION_BLOCKED' -> {flag: clients whose docs set it}."""
  object_of = script_object_classes()
  flags: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
  for c in clients:
    for system in c.systems:
      owner, sep = system_owner(system, object_of)
      for fn in system.get("Functions", []) or []:
        name = f"{owner}{sep}{fn['Name']}" if owner else fn["Name"]
        for key, value in fn.items():
          if value and SECURITY_FLAG_RE.match(key):
            flags[name][key].add(c.flavor)
      for event in system.get("Events", []) or []:
        for key, value in event.items():
          if value and SECURITY_FLAG_RE.match(key):
            flags[event["LiteralName"]][key].add(c.flavor)
  return flags


def flag_note(flags: dict[str, set[str]], everyone: int) -> str:
  """'Blizzard: HasRestrictions, IsProtectedFunction (Forever only)'."""
  parts = [
    flag + (f" ({FLAVOR_LABEL[next(iter(fl))]} only)" if len(fl) < everyone else "")
    for flag, fl in sorted(flags.items())
  ]
  return "Blizzard: " + ", ".join(parts) if parts else ""


def security_section(name: str, tags: set[str], flags: set[str]) -> str | None:
  """Which Security.lua section a global function belongs in, if any."""
  if SECURITY_TOOLS.match(name):
    return "tools"
  if "protected" in tags or "IsProtectedFunction" in flags:
    return "protected"
  if "hwevent" in tags:
    return "hwevent"
  if tags & USAGE_TAGS or "HasRestrictions" in flags or any(f.startswith("RestrictedFor") for f in flags):
    return "restricted"
  if any(f.startswith(("SecretReturns", "SecretWhen", "SecretIn")) for f in flags):
    return "secret"
  return None


def widget_restricted(tags: set[str], flags: set[str]) -> bool:
  return bool(tags & WIDGET_TAGS) or bool(flags - {"SecureHooksAllowed"})


def restricted_on(section: str, tags: set[str], flags: dict[str, set[str]], present: set[str]) -> set[str]:
  """Clients an item is restricted on. Wiki tags hold for every client that has the item; a
  Blizzard flag only for the clients whose documentation sets it (secret values: Forever)."""
  if section in ("tools", "hwevent") or tags & (WIDGET_TAGS if section == "widget" else {"protected"} | USAGE_TAGS):
    return set(present)
  wanted = {
    "protected": lambda f: f == "IsProtectedFunction",
    "restricted": lambda f: f == "HasRestrictions" or f.startswith("RestrictedFor"),
    "secret": lambda f: f.startswith(("SecretReturns", "SecretWhen", "SecretIn")),
    "widget": lambda f: f != "SecureHooksAllowed",
  }[section]
  return present & set().union(*(fl for f, fl in flags.items() if wanted(f)))


def build_security(
  clients: list[Client],
  sections: dict[str, list[tuple[str, set[str]]]],
  widget_methods: dict[str, list[tuple[str, set[str]]]],
  flags: dict[str, dict[str, set[str]]],
) -> list[str]:
  """Security/Security.lua: the document, a generated summary, the secure template type, then
  every restricted item by section. Items are (rendered chunk, clients that have it)."""
  doc = SECURITY_DOC.read_text(encoding="utf-8").rstrip()
  chunks = [f"--[==[\n{doc}\n]==]"]

  everyone = len(clients)
  per_section = {key: sections.get(key, []) for key, _ in SECURITY_SECTIONS}
  per_section["widget"] = [item for items in widget_methods.values() for item in items]
  summary = [
    "Generated summary (rebuilt on every run)",
    "",
    "Number of items below that are restricted on each client: wiki tags count for every client that",
    "has the item, Blizzard flags only for the client whose documentation sets them (secret values are",
    "Forever's; Era does not have them).",
    "",
    "| Section | Era | Forever |",
    "|---|---|---|",
  ]
  for key, title in SECURITY_SECTIONS:
    counts = [sum(1 for _, fl in per_section[key] if c.flavor in fl) for c in clients]
    summary.append(f"| {title} | {' | '.join(map(str, counts))} |")
  summary += ["", "Events: ADDON_ACTION_BLOCKED, ADDON_ACTION_FORBIDDEN, PLAYER_REGEN_DISABLED (combat starts),",
              "PLAYER_REGEN_ENABLED (combat ends: apply queued changes)."]
  events_by_flag: dict[str, list[str]] = defaultdict(list)
  for name, event_flags in sorted(flags.items()):
    if name.isupper() and "_" in name:
      events_by_flag[flag_note(event_flags, everyone).removeprefix("Blizzard: ")].append(name)
  if events_by_flag:
    summary += ["", "Events whose payload may be secret on tainted code paths, by Blizzard flag:"]
    for flag, names in sorted(events_by_flag.items()):
      summary += [f"- {flag}:", *textwrap.wrap(", ".join(names), 96, initial_indent="  ", subsequent_indent="  ")]
  chunks.append("--[==[\n" + "\n".join(summary) + "\n]==]")

  templates: dict[str, tuple[str, set[str]]] = {}
  for c in clients:
    for name, spec in c.templates.items():
      if re.fullmatch(r"(?:Secure|Insecure)\w*Template", name):
        templates.setdefault(name, (spec.get("type", "") if isinstance(spec, dict) else "", set()))[1].add(c.flavor)
  lines = [
    "---Secure (and their insecure counterpart) XML templates the clients have.",
    "---@alias SecureTemplate string",
  ]
  for name, (kind, fl) in sorted(templates.items()):
    notes = " ".join(x for x in (kind, flavor_tag(fl)) if x)
    lines.append(f'---|"{name}"' + (f" # {notes}" if notes else ""))
  chunks.append("\n".join(lines))

  for key, title in SECURITY_SECTIONS:
    if key == "widget":
      chunks.append(f"-- {title} " + "-" * max(4, 96 - len(title)))
      for cls, items in sorted(widget_methods.items()):
        chunks.append(f"---@class {cls}\nlocal {cls} = {{}}")
        chunks += [chunk for chunk, _ in items]
    elif per_section[key]:
      chunks.append(f"-- {title} " + "-" * max(4, 96 - len(title)))
      chunks += [chunk for chunk, _ in per_section[key]]
  return chunks


# --- Library sections ------------------------------------------------------------------------


def build_functions(
  clients: list[Client],
  types: BlizzardTypes,
  wiki,
  transcluder: Transcluder,
  predefined: set[str],
  flags: dict[str, dict[str, set[str]]],
  entries: list[Entry],
) -> tuple[dict[str, list[str]], dict[str, list[tuple[str, set[str]]]]]:
  """Global and namespaced functions -> ({output file: rendered chunks}, {security section: items}),
  plus a reference/ entry per function appended to `entries`.
  A function exists when a client has it in C (GlobalAPI, LuaAPI) or as a Lua fallback from
  Blizzard_Deprecated (UnitAura on Era). Names a copied Ketho file already annotates (`predefined`)
  are left to that file. Restricted functions go to the security sections instead of their file."""
  pages, redirects, _ = wiki
  present: dict[str, set[str]] = defaultdict(set)  # name -> clients that have it
  in_c: dict[str, set[str]] = defaultdict(set)  # name -> clients that have it as a C function
  shims: dict[str, dict[str, Deprecated]] = defaultdict(dict)  # name -> {client: its Lua fallback}
  for c in clients:
    for name in c.globals | c.lua_api:
      present[name].add(c.flavor)
      in_c[name].add(c.flavor)
    tables = {n.split(".")[0] for n in c.globals | c.lua_globals if "." in n}
    for name, shim in c.deprecated.items():
      owner = re.split(r"[.:]", name)[0]
      if name not in c.globals and (owner == name or owner in tables):  # not 'searcher.Foo' on a local
        present[name].add(c.flavor)
        shims[name][c.flavor] = shim

  # Blizzard documentation, per flavor; Era's signature wins, a differing Forever one becomes an overload.
  # ScriptObject systems document widget methods (SimpleButtonAPI: GetText); they belong to build_widgets.
  documented: dict[str, tuple[str, Func]] = {}  # name -> (system file, func)
  for c in clients:
    for system in c.systems:
      if system.get("Type") == "ScriptObject":
        continue
      for fn in system.get("Functions", []) or []:
        f = types.func(fn, system.get("Namespace") or "")
        if f.name not in present:
          continue
        if f.name in documented:
          first = documented[f.name][1]
          if fun_type(first) != fun_type(f) and fun_type(f) not in first.overloads:
            first.overloads.append(fun_type(f))
        else:
          documented[f.name] = (system["_file"], f)

  # Pages whose {{apisig}} names a function: UnitBuff and UnitDebuff are documented on UnitAura's page.
  signed: dict[str, WikiPage] = {}
  for page in pages.values():
    for sig in page.facts.get("signatures", []):
      for call, _ in split_signature(sig)[0]:
        signed.setdefault(call.replace(":", "."), page)
  page_by_title = {p.title: p for p in pages.values()}

  curated = ketho_functions()
  files: dict[str, list[str]] = defaultdict(list)
  security: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)
  for name in sorted(present, key=str.lower):
    if name in predefined:
      continue
    own = pages.get(name) or signed.get(name)
    if (classic := pages.get(f"{name}/Classic")) and present[name] == {"era"}:
      own = classic  # an Era-only function: the wiki's Classic page has its signature
    see = None if own else page_by_title.get(redirects.get(name, ""))  # a redirect: a pointer, not a signature
    shim = next(iter(shims[name].values()), None) if name in shims else None
    block = ""  # a curated annotation from Ketho, used as is under our notes
    if name in documented:
      file, f = documented[name]
      f.doc = (wiki_doc(own or see) if own or see else []) + f.doc
      out = f"API/{file}.lua"
    elif own and name in curated and own is not classic:
      f = Func(name, doc=[d for d in wiki_doc(own) if not d.startswith("[Documentation]")])
      block = curated[name]
      out = GLOBAL_FILE
    elif own:
      f = wiki_funcs(own, transcluder, want=name).get(name) or Func(name, [Param("...")])
      f.doc = wiki_doc(own) + f.doc
      if own is not pages.get(name):
        f.doc.append(f"Documented on {own.title}.")
      if shim and shim.args is not None and not in_c[name] and len(f.params) != len(shim.args):
        taken: set[str] = set()  # the wiki describes another version; the fallback's arguments are what runs
        f.params = [Param(lua_name(a, taken), optional=True) for a in shim.args]
      out = GLOBAL_FILE
    elif shim and shim.args is None and shim.replacement in documented:  # 'X = C_Ns.Fn'
      replacement = documented[shim.replacement][1]
      f = Func(name, replacement.params, replacement.returns, overloads=list(replacement.overloads))
      out = GLOBAL_FILE
    elif shim and shim.args is not None:
      taken: set[str] = set()
      f = Func(name, [Param(lua_name(a, taken)) for a in shim.args])
      out = GLOBAL_FILE
    elif see:
      f = Func(name, [Param("...")], doc=wiki_doc(see) + [f"The wiki redirects {name} to {see.title}."])
      out = GLOBAL_FILE
    else:
      f = Func(name, [Param("...")], doc=["Undocumented: the client has it; Blizzard and the wiki do not document it."])
      out = "API/Undocumented.lua"
    if shim:
      use = f" Use {shim.replacement} instead." if shim.replacement else ""
      note = f"Lua fallback from {shim.file}, only loaded while the CVar loadDeprecationFallbacks is on.{use}"
      if in_c[name]:  # a C function on one client, only a fallback on the other: not deprecated everywhere
        f.doc.append(f"Deprecated on {', '.join(FLAVOR_LABEL[fl] for fl in sorted(shims[name]))}: {note}")
      else:
        f.doc += ["@deprecated", note]
        out = "API/Deprecated.lua"
    if tag := flavor_tag(present[name]):
      f.doc.insert(0, tag)
    if note := flag_note(flags.get(name, {}), len(clients)):
      f.doc.append(note)
    rendered = "\n".join([*doc_lines(f.doc), block]) if block else render_func(f)
    page_tags = (own or see).tags if own or see else set()
    if section := security_section(name, page_tags, set(flags.get(name, {}))):
      security[section].append((rendered, restricted_on(section, page_tags, flags.get(name, {}), present[name])))
      out = SECURITY_FILE
    else:
      files[out].append(rendered)
    entry = reference_entry(name, "function", present[name], rendered, out, f.doc, own or see, flags.get(name, {}))
    if shim and not in_c[name]:
      entry.deprecated = shim.replacement or "yes"
    entries.append(entry)
  return files, security


REFERENCE_NOTES = ("**", "Lua fallback", "Deprecated on", "Documented on", "The wiki redirects", "Undocumented")


def reference_entry(
  name: str, kind: str, present: set[str], annotation: str, library_file: str, doc: list[str],
  page: WikiPage | None, flags: dict[str, set[str]],
) -> Entry:
  """The reference/ entry for an item, from what the library says about it and its wiki page."""
  notes = [d.strip("*") for d in doc if d.startswith(REFERENCE_NOTES)]
  summary = next(iter(description(page.text)), "") if page else ""
  not_summary = (*REFERENCE_NOTES, "[", "#", "@", "Blizzard:")
  summary = summary or next((d for d in doc if d and not d.startswith(not_summary)), "")
  return Entry(
    name=name,
    kind=kind,
    clients=[FLAVOR_LABEL[fl] for fl in FLAVORS if fl in present],
    annotation=annotation,
    library_file=library_file,
    summary=one_line(summary),
    notes=notes,
    tags=sorted(page.tags) if page else [],
    flags={flag: [FLAVOR_LABEL[fl] for fl in FLAVORS if fl in fls] for flag, fls in sorted(flags.items())},
    page_title=page.title if page else "",
    page_text=page.text if page else "",
    aliases=page.aliases if page else [],
  )


def build_namespaces(clients: list[Client]) -> list[str]:
  present: dict[str, set[str]] = defaultdict(set)
  for c in clients:
    for name in c.globals:
      if "." in name:
        present[name.split(".")[0]].add(c.flavor)
  return [
    (f"---{tag}\n" if (tag := flavor_tag(fl)) else "") + f"{ns} = {{}}" for ns, fl in sorted(present.items())
  ]


def build_structures(types: BlizzardTypes, skip: set[str]) -> tuple[list[str], list[str]]:
  """Blizzard's Structure and CallbackType tables, except those a copied Ketho file already defines."""
  structures, callbacks = [], []
  for name, (table, fl) in sorted(types.structures.items()):
    if name in skip:
      continue
    lines = [f"---{tag}"] if (tag := flavor_tag(fl)) else []
    lines.append(f"---@class {name}")
    for f in table.get("Fields", []) or []:
      desc = one_line(" ".join(f.get("Documentation", []) or []))
      nilable = "?" if f.get("Nilable") else ""
      lines.append(f"---@field {f['Name']} {types.lua(f)}{nilable}" + (f" {desc}" if desc else ""))
    structures.append("\n".join(lines))
  for name, (table, fl) in sorted(types.callbacks.items()):
    if name in skip:
      continue
    taken: set[str] = set()
    f = Func(name, [types.param(a, taken) for a in table.get("Arguments", []) or []])
    f.returns = [types.param(r, set()) for r in table.get("Returns", []) or []]
    callbacks.append((f"---{tag}\n" if (tag := flavor_tag(fl)) else "") + f"---@alias {name} {fun_type(f)}")
  return structures, callbacks


def per_client(values: dict[str, object], everyone: int) -> tuple[object, str]:
  """{client: value} -> (value to write, comment). The first client's value is written; a
  different value elsewhere ('Forever: -1') or a missing client ('Era only') goes in the comment."""
  first = next(iter(values.values()))
  notes = [f"{FLAVOR_LABEL[fl]}: {lua_literal(v)}" for fl, v in values.items() if v != first]
  if len(values) < everyone:
    notes.insert(0, flavor_tag(set(values)))
  return first, "; ".join(notes)


def value_lines(values_by_key: dict[str, dict[str, object]], everyone: int, indent: str) -> list[str]:
  def order(item):
    first = next(iter(item[1].values()))
    return (first if isinstance(first, (int, float)) and not isinstance(first, bool) else 0, item[0])

  lines = []
  for key, values in sorted(values_by_key.items(), key=order):
    value, note = per_client(values, everyone)
    lines.append(f"{indent}{key} = {lua_literal(value)}," + (f" -- {note}" if note else ""))
  return lines


def build_enums(clients: list[Client]) -> list[str]:
  chunks = ["Enum = {}"]
  for name in sorted({n for c in clients for n in c.enums}):
    have = [c for c in clients if name in c.enums]
    values: dict[str, dict[str, object]] = defaultdict(dict)
    for c in have:
      for k, v in c.enums[name].items():
        values[k][c.flavor] = v
    lines = [f"---{tag}"] if (tag := flavor_tag({c.flavor for c in have})) else []
    lines += [f"---@enum Enum.{name}", f"Enum.{name} = {{", *value_lines(values, len(have), "\t"), "}"]
    chunks.append("\n".join(lines))

  groups: dict[str, dict[str, dict[str, object]]] = defaultdict(lambda: defaultdict(dict))
  for c in clients:
    for group, values in c.constants.items():
      for k, v in values.items():
        groups[group][k][c.flavor] = v
  chunks.append("Constants = {\n" + "\n".join(
    f"\t{group} = {{\n" + "\n".join(value_lines(values, len(clients), "\t\t")) + "\n\t},"
    for group, values in sorted(groups.items())
  ) + "\n}")

  le: dict[str, dict[str, object]] = defaultdict(dict)
  for c in clients:
    for n, v in c.le.items():
      le[n][c.flavor] = v
  le_lines = []
  for n in sorted(le):
    value, note = per_client(le[n], len(clients))
    le_lines.append(f"{n} = {lua_literal(value)}" + (f" -- {note}" if note else ""))
  chunks.append("\n".join(le_lines))
  return chunks


def build_events(
  clients: list[Client], types: BlizzardTypes, wiki, flags: dict[str, dict[str, set[str]]], entries: list[Entry]
) -> list[str]:
  """Data/Event.lua's FrameEvent alias, plus a reference/ entry per event with its typed payload."""
  pages, _, _ = wiki
  present: dict[str, set[str]] = defaultdict(set)
  payloads: dict[str, dict[str, str]] = defaultdict(dict)  # event -> {client: 'a, b'}
  typed: dict[str, dict[str, str]] = defaultdict(dict)  # event -> {client: 'a: string, b: number?'}
  for c in clients:
    for names in c.events.values():
      for n in names:
        present[n].add(c.flavor)
    for system in c.systems:
      for ev in system.get("Events", []) or []:
        payload = ev.get("Payload", []) or []
        payloads[ev["LiteralName"]][c.flavor] = ", ".join(p["Name"] for p in payload)
        typed[ev["LiteralName"]][c.flavor] = ", ".join(
          f"{p['Name']}: {types.lua(p)}{'?' if p.get('Nilable') else ''}" for p in payload
        )
  lines = ["---@alias FrameEvent string"]
  for name in sorted(present):
    by_client = {fl: p for fl, p in payloads.get(name, {}).items() if fl in present[name]}
    first = next(iter(by_client.values()), "")
    notes = [f"`{first}`"] if first else []
    notes += [f"({FLAVOR_LABEL[fl]}: `{p}`)" for fl, p in by_client.items() if p != first]
    if tag := flavor_tag(present[name]):
      notes.append(tag)
    line = f'---|"{name}"' + (f" # {' '.join(notes)}" if notes else "")
    lines.append(line)

    by_client_typed = {fl: p for fl, p in typed.get(name, {}).items() if fl in present[name]}
    first_typed = next(iter(by_client_typed.items()), None)
    annotation = [line]
    if first_typed:
      annotation.append(f"-- Payload (Blizzard documentation): {first_typed[1] or 'none'}")
      annotation += [
        f"-- Payload on {FLAVOR_LABEL[fl]}: {p or 'none'}" for fl, p in by_client_typed.items() if p != first_typed[1]
      ]
    entries.append(reference_entry(
      name, "event", present[name], "\n".join(annotation), "Data/Event.lua", [tag] if tag else [], pages.get(name),
      flags.get(name, {}),
    ))
  return ["\n".join(lines)]


def build_cvars(clients: list[Client]) -> list[str]:
  present: dict[str, set[str]] = defaultdict(set)
  info: dict[str, list] = {}
  for c in clients:
    for name, values in c.cvars.items():
      present[name].add(c.flavor)
      info.setdefault(name, values)
  lines = ["---@alias CVar string"]
  for name in sorted(present, key=str.lower):
    default, help_text = info[name][0], plain(str(info[name][-1]))
    default_note = f"default `{default}`" if default != "" else ""
    notes = " ".join(x for x in (default_note, help_text, flavor_tag(present[name])) if x)
    lines.append(f'---|"{name}"' + (f" # {notes}" if notes else ""))
  return ["\n".join(lines)]


KETHO_METHOD_RE = re.compile(r"((?:^---.*\n)*)^function (\w+):(\w+)\((.*)\) end", re.MULTILINE)


def ketho_methods() -> dict[str, dict[str, str]]:
  """Method name -> {class: doc block + function line} from Ketho's widget annotations."""
  methods: dict[str, dict[str, str]] = defaultdict(dict)
  for path in (SOURCES / "ketho/Annotations/Core/Widget").rglob("*.lua"):
    for m in KETHO_METHOD_RE.finditer(path.read_text(encoding="utf-8")):
      doc = "\n".join(line for line in m.group(1).splitlines() if not line.startswith(("---@meta", "---@class")))
      methods[m.group(3)][m.group(2)] = (doc + "\n" if doc else "") + f"function {{cls}}:{m.group(3)}({m.group(4)}) end"
  return methods


def ketho_parents() -> dict[str, list[str]]:
  parents = {}
  for path in (SOURCES / "ketho/Annotations/Core/Widget").rglob("*.lua"):
    for m in re.finditer(r"^---@class (\w+)\s*:\s*(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE):
      parents.setdefault(m.group(1), [p.strip() for p in m.group(2).split(",")])
  return parents


def script_object_classes() -> dict[str, str]:
  """Blizzard ScriptObject system -> widget class ('SimpleButtonAPI' -> 'Button'), from the wiki's data."""
  return json.loads((DUMP / "data/Wowapi/data/scriptobject.json").read_text(encoding="utf-8"))


def system_owner(system: dict, object_of: dict[str, str]) -> tuple[str, str]:
  """('C_Item', '.') for a namespaced system, ('Button', ':') for widget methods, ('', '') for globals."""
  if system.get("Type") == "ScriptObject":
    return object_of.get(system["Name"]) or system["Name"].removeprefix("Simple").removesuffix("API"), ":"
  return system.get("Namespace") or "", "."


def blizzard_methods(clients: list[Client], types: BlizzardTypes) -> dict[str, Func]:
  """'Button:GetText' -> Func from Blizzard's ScriptObject docs (SimpleButtonAPI); Era's
  signature first, a differing Forever one as an overload."""
  object_of = script_object_classes()
  methods: dict[str, Func] = {}
  for c in clients:
    for system in c.systems:
      if system.get("Type") != "ScriptObject":
        continue
      cls, _ = system_owner(system, object_of)
      for fn in system.get("Functions", []) or []:
        f = types.func(fn, cls, ":")
        if f.name not in methods:
          methods[f.name] = f
        elif fun_type(f) != fun_type(methods[f.name]) and fun_type(f) not in methods[f.name].overloads:
          methods[f.name].overloads.append(fun_type(f))
  return methods


def build_widgets(
  clients: list[Client], types: BlizzardTypes, wiki, flags: dict[str, dict[str, set[str]]], entries: list[Entry]
) -> tuple[dict[str, list[str]], dict[str, list[tuple[str, set[str]]]]]:
  """Widget classes as the clients define them (BlizzardInterfaceResources WidgetAPI). Method
  signatures come from Blizzard's docs for that class, else Ketho's block for the class or an
  ancestor, else the wiki's method lists. Returns ({file: chunks}, {class: restricted methods});
  restricted methods (#secureframe, ...) go to Security.lua instead of the class file. A
  reference/ entry per method is appended to `entries`."""
  pages, _, tags = wiki
  pages_by_method: dict[str, dict[str, WikiPage]] = defaultdict(dict)  # method -> class -> wiki page
  for name, page in pages.items():
    if ":" in name:
      owner, method = name.split(":", 1)
      pages_by_method[method][owner] = page
  flags_by_method: dict[str, dict[str, dict[str, set[str]]]] = defaultdict(dict)  # method -> class -> flags
  for name, method_flags in flags.items():
    if ":" in name:
      owner, method = name.split(":", 1)
      flags_by_method[method][owner] = method_flags
  tags_by_method: dict[str, dict[str, set[str]]] = defaultdict(dict)  # method -> class -> wiki tags
  for name, method_tags in tags.items():
    if ":" in name and method_tags:
      owner, method = name.split(":", 1)
      tags_by_method[method][owner] = method_tags
  restricted: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)
  fallback_parents = ketho_parents()
  documented = blizzard_methods(clients, types)
  listing_args: dict[str, tuple[str, str]] = {}
  for line in (DUMP / "listings.jsonl").open(encoding="utf-8"):
    row = json.loads(line)
    if row.get("type") in ("w", "Function") and ":" in row["name"]:
      listing_args.setdefault(row["name"], (row.get("args", ""), row.get("returns", "")))
  ketho = ketho_methods()
  classes: dict[str, dict] = {}
  for c in clients:
    for cls, spec in c.widgets.items():
      entry = classes.setdefault(cls, {"inherits": [], "flavors": set(), "methods": defaultdict(set)})
      entry["flavors"].add(c.flavor)
      entry["inherits"] = entry["inherits"] or list(spec.get("inherits", []))
      for method in spec.get("methods", []):
        entry["methods"][method].add(c.flavor)
  for cls, entry in classes.items():
    if cls in entry["inherits"]:  # the dumps list Region as inheriting Region; use Ketho's parents the clients have
      entry["inherits"] = [p for p in fallback_parents.get(cls, []) if p in classes and p != cls]

  def ancestors(cls: str) -> list[str]:
    out, queue = [], list(classes.get(cls, {}).get("inherits", []))
    while queue:
      parent = queue.pop(0)
      if parent not in out:
        out.append(parent)
        queue += classes.get(parent, {}).get("inherits", [])
    return out

  def donor(cls: str, by_class: dict):
    """The definition for this class, an ancestor, or a split-off relative (the dumps keep
    SetPoint on ScriptRegion; Blizzard and Ketho document it on ScriptRegionResizing)."""
    for candidate in (cls, *ancestors(cls)):
      if candidate in by_class:
        return by_class[candidate]
    related = sorted(k for k in by_class for a in (cls, *ancestors(cls)) if k.startswith(a) or a.startswith(k))
    return by_class[related[0]] if related else None

  documented_by_method: dict[str, dict[str, Func]] = defaultdict(dict)
  for name, f in documented.items():
    owner, method = name.split(":", 1)
    documented_by_method[method][owner] = f

  files: dict[str, list[str]] = {}
  for cls, entry in sorted(classes.items()):
    header = [f"---{tag}"] if (tag := flavor_tag(entry["flavors"])) else []
    header += [f"---[Documentation]({wiki_url('UIOBJECT ' + cls)})"]
    header.append(f"---@class {cls}" + (f" : {', '.join(entry['inherits'])}" if entry["inherits"] else ""))
    header.append(f"local {cls} = {{}}")
    # CreateFrame("frame") / ("FRAME") resolve to these, as in Ketho's annotations
    header += [f"---@class {variant} : {cls}" for variant in sorted({cls.lower(), cls.upper()} - {cls})]
    chunks = ["\n".join(header)]
    for method in sorted(entry["methods"]):
      notes = [t for t in (flavor_tag(entry["methods"][method]),) if t]
      if method_tags := donor(cls, tags_by_method.get(method, {})):  # wiki lists ScriptRegionResizing:SetPoint
        notes.append(" ".join(f"#{t}" for t in sorted(method_tags)))
      blizzard, curated = donor(cls, documented_by_method.get(method, {})), donor(cls, ketho.get(method, {}))
      # Ketho marks optional arguments (SetPoint("CENTER")); Blizzard's docs often don't. Prefer his
      # block unless Blizzard documents more parameters (SetRotation(radians, animate)).
      if curated and not (blizzard and len(blizzard.params) > curated.count("---@param ")):
        block = curated.replace("{cls}", cls)
      elif blizzard:
        f = replace(blizzard, name=f"{cls}:{method}")
        f.doc = [f"[Documentation]({wiki_url(f'API {cls} {method}')})"] + f.doc
        block = render_func(f)
      else:
        args, rets = listing_args.get(f"{cls}:{method}", ("", ""))
        calls, returns = split_signature(f"{rets} = X({args})" if rets else f"X({args})")
        params, omittable = sig_params(calls[0][1]) if calls else ([], [])
        f = Func(f"{cls}:{method}", params)
        f.returns = [Param("..." if r == "..." else lua_name(r, set())) for r in returns]
        if any(omittable):
          f.overloads.append(without_omitted(f, omittable))
        f.doc = [f"[Documentation]({wiki_url(f'API {cls} {method}')})"]
        block = render_func(f)
      method_flags = donor(cls, flags_by_method.get(method, {})) or {}
      if note := flag_note(method_flags, len(clients)):
        notes.append(note)
      chunk = "\n".join(f"---{n}" for n in notes) + ("\n" if notes else "") + block
      clients_with = entry["methods"][method]
      if widget_restricted(method_tags or set(), set(method_flags)):
        restricted[cls].append((chunk, restricted_on("widget", method_tags or set(), method_flags, clients_with)))
        library_file = SECURITY_FILE
      else:
        chunks.append(chunk)
        library_file = f"Widget/{cls}.lua"
      page = donor(cls, pages_by_method.get(method, {}))
      entries.append(
        reference_entry(f"{cls}:{method}", "method", clients_with, chunk, library_file, notes, page, method_flags)
      )
    files[f"Widget/{cls}.lua"] = chunks
  return files, restricted


def copy_framexml(clients: list[Client]) -> None:
  """Ketho's FrameXML annotations (ColorMixin, CreateColor, ItemLocationMixin, MenuUtil, ...) follow
  mainline; keep a file only when most globals it defines exist in at least one of our clients."""
  known = set().union(*(c.lua_globals | c.globals for c in clients))  # 'CreateColor', 'AuraUtil.ForEachAura'
  known |= {name.split(".")[0] for name in known if "." in name}  # tables: 'AuraUtil'
  source = SOURCES / "ketho/Annotations/Core/FrameXML"
  dropped = []
  for path in sorted(source.rglob("*.lua")):
    text = path.read_text(encoding="utf-8")
    names = set(re.findall(r"^(?:function ([A-Za-z_][\w.]*)\(|([A-Za-z_]\w*) = \{)", text, re.MULTILINE))
    names = {a or b for a, b in names}
    if names and len(names & known) * 2 < len(names):
      dropped.append(path.relative_to(source).as_posix())
      continue
    dest = OUT / "FrameXML" / path.relative_to(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(path, dest)
  if dropped:
    print(f"FrameXML files not in Era/Forever, skipped: {', '.join(dropped)}", file=sys.stderr)


def defined_globals(root: Path) -> set[str]:
  """Functions and aliases already annotated under root: 'function Mixin(', 'format = string.format'."""
  names: set[str] = set()
  for path in root.rglob("*.lua"):
    text = path.read_text(encoding="utf-8")
    names.update(re.findall(r"^function ([A-Za-z_][\w.:]*)\s*\(", text, re.MULTILINE))
    names.update(re.findall(r"^([A-Za-z_][\w.]*)\s*=", text, re.MULTILINE))  # EventRegistry = CreateFromMixins(...)
  return names


KETHO_FUNCTION_RE = re.compile(r"((?:^---.*\n)*)^function ([\w.:]+)\((.*)\) end$", re.MULTILINE)


def ketho_functions() -> dict[str, str]:
  """Name -> annotation block from Ketho's Data/Wiki.lua, only where he adds what a wiki parse can't
  express: generic signatures such as CreateFrame's `T` (other blocks may mark optional args required)."""
  text = (SOURCES / "ketho/Annotations/Core/Data/Wiki.lua").read_text(encoding="utf-8")
  text = re.sub(r"^---@meta.*\n", "", text, flags=re.MULTILINE)
  return {m.group(2): m.group(0).strip() for m in KETHO_FUNCTION_RE.finditer(text) if "---@generic" in m.group(1)}


def build_frames(clients: list[Client], predefined: set[str]) -> list[str]:
  """Named global frames. Their widget type is only known when the name is a widget class
  (GameTooltip, Minimap); the rest are typed Frame."""
  classes = {cls for c in clients for cls in c.widgets}
  present: dict[str, set[str]] = defaultdict(set)
  for c in clients:
    for name in c.frames:
      present[name].add(c.flavor)
  chunks = []
  for name, fl in sorted(present.items()):
    if name not in predefined:
      tag = f"---{flavor_tag(fl)}\n" if flavor_tag(fl) else ""
      chunks.append(f"{tag}---@type {name if name in classes else 'Frame'}\n{name} = {{}}")
  return chunks


TYPE_TAG_RE = re.compile(
  r"^---@(param\s+\S+|return|field\s+\S+|alias\s+\S+|overload|type|class\s+[^\s:]+)\s*(.*)$", re.MULTILINE
)


def type_names(tag: str, rest: str) -> set[str]:
  """Type names an annotation refers to. '@overload'/'@alias' are all type; '@param x T desc',
  '@return T name' and '@field x T desc' start with one; '@class X : A, B' names parents."""
  if tag.startswith("class"):
    return {p.strip() for p in rest.removeprefix(":").split(",") if p.strip()} if rest.startswith(":") else set()
  rest = re.sub(r"\"[^\"]*\"|'[^']*'|`[^`]*`", "", rest.split(" # ")[0])  # comments, string literal types
  if not tag.startswith(("overload", "alias")):  # the type is the first token; spaces inside (...) belong to it
    depth, end = 0, 0
    while end < len(rest) and (depth or not rest[end].isspace()):
      depth += {"(": 1, ")": -1}.get(rest[end], 0)
      end += 1
    if rest[:end].endswith(":"):  # 'fun(x: T): R' -> include the return type
      end += len(re.match(r"\s*\S*", rest[end:]).group(0))
    rest = rest[:end]

  def typed_args(m: re.Match) -> str:  # fun(t, k: K) -> only the types: 'K'
    return ",".join(seg.split(":", 1)[1] for seg in m.group(1).split(",") if ":" in seg)

  rest = re.sub(r"fun\(([^()]*)\)", typed_args, rest)
  return set(re.findall(r"[A-Za-z_][\w.]*", rest)) - {"fun", "async"}


def type_usage(root: Path) -> tuple[set[str], set[str], set[str]]:
  """(defined, referenced, used as class parent) type names across the library's annotation files."""
  defined, referenced, parents = set(LUA_BUILTIN_TYPES), set(), set()
  for path in root.rglob("*.lua"):
    text = path.read_text(encoding="utf-8")
    defined.update(re.findall(r"^---@(?:class|alias|enum)\s+([\w.]+)", text, re.MULTILINE))
    for generic in re.findall(r"^---@generic\s+(.+)$", text, re.MULTILINE):  # '---@generic K, V: table'
      defined.update(p.split(":")[0].strip() for p in generic.split(","))
    for m in TYPE_TAG_RE.finditer(text):
      names = type_names(m.group(1), m.group(2).strip())
      referenced |= names
      if m.group(1).startswith("class"):
        parents |= names
  return defined, referenced, parents


def scan_ui_source(branch: str, entries: list[Entry]) -> UsageIndex | None:
  """Where Blizzard's UI source on `branch` uses each entry; None (with a hint) when not checked out."""
  checkout = ui_source_dir(branch)
  if not (checkout / "Interface").is_dir():
    print(f"no wow-ui-source checkout for {branch}; run: uv run generate.py sources --usage-branch {branch}",
          file=sys.stderr)
    return None
  subject = subprocess.run(
    ["git", "-C", checkout, "log", "-1", "--format=%h %s"], capture_output=True, text=True, check=True
  ).stdout.strip()
  names = {e.name for e in entries if e.kind != "method"}
  methods = {e.name.split(":", 1)[1] for e in entries if e.kind == "method"}
  return scan_usage(checkout, f"{branch} @ {subject}", names, methods)


def generate(usage_branch: str = USAGE_BRANCH, usage_limit: int = USAGE_LIMIT) -> None:
  clients = [load_client(f) for f in FLAVORS]
  wiki = load_wiki()
  types = BlizzardTypes(clients)

  shutil.rmtree(OUT, ignore_errors=True)
  ketho = SOURCES / "ketho/Annotations/Core"
  for part in ("Type", "Lua", "ScriptObject", "Widget/UIType", "Widget/Intrinsic"):
    shutil.copytree(ketho / part, OUT / part, dirs_exist_ok=True)
  (OUT / "Type/Namespace.lua").unlink(missing_ok=True)  # generated below for these clients
  shutil.copy(SOURCES / "ketho/LICENSE", OUT / "LICENSE-vscode-wow-api")

  copy_framexml(clients)
  predefined = defined_globals(OUT)  # Mixin, CreateFromMixins, string.format, ... from Ketho's files
  flags = blizzard_security_flags(clients)
  transcluder = Transcluder()
  entries: list[Entry] = []
  function_files, restricted_functions = build_functions(
    clients, types, wiki, transcluder, predefined, flags, entries
  )
  widget_files, restricted_methods = build_widgets(clients, types, wiki, flags, entries)
  for path, chunks in {**function_files, **widget_files}.items():
    write(OUT / path, chunks)
  write(OUT / SECURITY_FILE, build_security(clients, restricted_functions, restricted_methods, flags))
  write(OUT / "Type/Frames.lua", build_frames(clients, predefined))
  structures, callbacks = build_structures(types, skip=type_usage(OUT)[0])  # Ketho's copies win
  write(OUT / "Type/Structure.generated.lua", structures)
  write(OUT / "Type/Callback.lua", callbacks)
  write(OUT / "Type/Namespace.lua", build_namespaces(clients))
  write(OUT / "Data/Enum.lua", build_enums(clients))
  write(OUT / "Data/Event.lua", build_events(clients, types, wiki, flags, entries))
  write(OUT / "Data/CVar.lua", build_cvars(clients))
  guides = {"Security.md": SECURITY_DOC.read_text(encoding="utf-8")}
  for title in GUIDE_TITLES:  # the wiki's Secure Execution trail, where the dump has it
    if file := transcluder.files.get(title):
      guides[title] = (DUMP / "raw/pages" / file).read_text(encoding="utf-8")
  write_reference(REFERENCE, entries, guides, transcluder.expand, scan_ui_source(usage_branch, entries), usage_limit)

  defined, referenced, parents = type_usage(OUT)
  missing = sorted(referenced - defined)
  write(
    OUT / "Type/Undefined.lua",
    [f"---@class {t}" if t in parents else f"---@alias {t} any" for t in missing],
    "-- Types referenced somewhere in this library but defined nowhere; kept loose on purpose.",
  )

  stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
  sources = "\n".join(f"- `{d}` {repo}@{b}: {commit(SOURCES / d)}" for d, repo, b, _ in SOURCE_REPOS)
  wiki_info = json.loads((DUMP / "raw/fetch.json").read_text(encoding="utf-8"))
  (OUT / "README.md").write_text(
    f"# WoW API annotations: Classic Era + Forever\n\nGenerated {stamp} by `generate.py`.\n\n"
    "Anything only one client has is tagged `**Era only**` or `**Forever only**` in its doc comment;\n"
    "values that differ (enums, constants, event payloads) note the other client's value.\n"
    "`#protected`, `#secureframe`, ... come from the wiki. Functions that only exist as a\n"
    "Blizzard_Deprecated fallback are `@deprecated` and name the C_ function to use.\n\n"
    "Everything restricted (protected, hardware event, combat/instance limits, secret values, widget\n"
    "methods on protected frames) lives in `Security/Security.lua`, which opens with a guide to secure\n"
    "execution and taint. That guide is `docs/Security.md` in the generator repository.\n\n## Sources\n\n"
    f"{sources}\n- warcraft.wiki.gg dump fetched {wiki_info['fetched']}\n\n"
    "Type/, Lua/, ScriptObject/, Widget/UIType/, Widget/Intrinsic/ and FrameXML/ are copied from\n"
    "Ketho/vscode-wow-api (MIT, see LICENSE-vscode-wow-api); FrameXML/ only where its globals exist in\n"
    "these clients. Widget methods Blizzard does not document take Ketho's signatures.\n\n"
    "## Not covered yet\n\n"
    "- Lua globals of Blizzard's own UI without an annotation (StaticPopup_Show, Clamp, Round, ...)\n"
    "- the wiki's Classic-specific subpages (e.g. GetBattlefieldStatus returns differ on Classic)\n",
    encoding="utf-8",
  )
  counts = defaultdict(int)
  for path in OUT.rglob("*.lua"):
    counts[path.relative_to(OUT).parts[0]] += len(re.findall(r"^function ", path.read_text(encoding="utf-8"), re.M))
  print(f"wrote {OUT}: functions per folder {dict(counts)}, {len(missing)} undefined types", file=sys.stderr)


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("stage", nargs="?", choices=("library", "sources"), default="library")
  parser.add_argument(
    "--usage-branch", default=USAGE_BRANCH, help="wow-ui-source branch scanned for 'Used in wow-ui-source' lists"
  )
  parser.add_argument("--usage-limit", type=int, default=USAGE_LIMIT, help="files listed per reference entry")
  args = parser.parse_args()
  if args.stage == "sources":
    update_sources(args.usage_branch)
  else:
    generate(args.usage_branch, args.usage_limit)


if __name__ == "__main__":
  main()
