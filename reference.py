"""Markdown reference for AI and reading: one file per function, widget method and event.

generate.py builds the LuaLS library (for the language server) and hands this module one Entry per
API item; this module writes reference/ (for AI tools, search and reading):

  README.md                     what is here and how files are laid out
  index.md                      one line per entry: name, clients, tags, summary, file
  functions/<Name>.md           global and namespaced functions (C_Item.GetItemInfo.md)
  methods/<Class>/<Method>.md   widget methods
  events/<EVENT_NAME>.md        events
  guides/*.md                   docs/Security.md and the wiki's Secure Execution guide pages

Each entry file has YAML front matter with the facts (clients, restrictions, Blizzard flags,
deprecation, library file, wiki page), the LuaLS annotation from the library, and the wiki page
converted to markdown: details, examples, patch changes, see also. With a UsageIndex (scan_usage)
each entry also lists the files of Blizzard's UI source (Gethe/wow-ui-source) that use it.
"""

from __future__ import annotations

import json
import re
import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from wiki_dump import split_params

WIKI_URL = "https://warcraft.wiki.gg/wiki/"
KIND_DIRS = {"function": "functions", "method": "methods", "event": "events"}


@dataclass
class Entry:
  """One API item as the library describes it, plus the wiki page it is documented on."""

  name: str  # 'UnitAura', 'C_Item.GetItemInfo', 'Frame:SetPoint', 'ADDON_LOADED'
  kind: str  # function | method | event
  clients: list[str]  # ['Era', 'Forever']
  annotation: str  # the LuaLS block from the library
  library_file: str  # 'API/Global.lua', 'Security/Security.lua', ...
  summary: str = ""  # one line for the index
  notes: list[str] = field(default_factory=list)  # deprecation, 'Era only', 'documented on ...'
  tags: list[str] = field(default_factory=list)  # wiki restriction tags: protected, hwevent, ...
  flags: dict[str, list[str]] = field(default_factory=dict)  # Blizzard flag -> clients
  deprecated: str = ""  # replacement to use, or 'yes'
  page_title: str = ""  # the wiki page it is documented on
  page_text: str = ""  # that page's wikitext
  aliases: list[str] = field(default_factory=list)  # wiki titles redirecting to the page
  ui_source_files: int = 0  # how many wow-ui-source files reference it (set when rendered)


# --- Wikitext to markdown --------------------------------------------------------------------

INLINE_FLAVORS = {
  "wow": "Classic", "classic": "Classic", "tbc": "TBC", "wotlk": "Wrath", "cata": "Cata", "mop": "Mists",
  "mists": "Mists", "wod": "WoD", "legion": "Legion", "bfa": "BfA", "sl": "Shadowlands", "df": "Dragonflight",
  "tww": "The War Within", "mn": "Midnight",
}
PREFORMATTED = "\x01"  # marks wiki lines that start with a space (preformatted text)
DROP_TEMPLATES = {
  "wowapi", "wowapievent", "widgetmethod", "intrinsicmethod", "wowapitype", "widget", "widgethandler",
  "wowsystem", "luaapi", "framexmlfunc", "apinav", "apinavbox", "tocright", "toc", "reflist", "uitech",
  "stub/api", "wikify", "elinks-api", "api trail secure", "documentation", "notoc", "clear", "-",
}


def wiki_to_markdown(text: str, expand: Callable[[str], str] = lambda t: t) -> str:
  """Convert a wiki page body to markdown: headings, lists, definition lists, tables, code
  blocks (syntaxhighlight, pre, space-indented), links and the API templates."""
  markers = r"<!--.*?-->|__NOTOC__|__TOC__|</?(?:onlyinclude|includeonly|noinclude)>"
  text = re.sub(markers, "", expand(re.sub(markers, "", text, flags=re.S)), flags=re.S)  # again: from transclusions
  code: list[str] = []

  def stash(lang: str, body: str) -> str:
    code.append(f"```{lang}\n{body.strip(chr(10))}\n```")
    return f"\x00{len(code) - 1}\x00"

  text = re.sub(r"<syntaxhighlight[^>]*\binline\b[^>]*>(.*?)</syntaxhighlight\s*>", r"`\1`", text, flags=re.S | re.I)
  text = re.sub(
    r"<(syntaxhighlight|source)[^>]*?(?:lang=\"?(\w+)\"?)?[^>]*>(.*?)</\1\s*>",
    lambda m: "\n" + stash(m.group(2) or "lua", m.group(3)) + "\n",
    text,
    flags=re.S | re.I,
  )
  text = re.sub(r"<pre[^>]*>(.*?)</pre\s*>", lambda m: "\n" + stash("", m.group(1)) + "\n", text, flags=re.S | re.I)
  text = re.sub(r"<ref[^>/]*/>|<ref[^>]*>.*?</ref\s*>", "", text, flags=re.S | re.I)
  text = re.sub(r"^ ", PREFORMATTED, text, flags=re.M)  # mark before templates vanish and leave spaces behind
  text = render_templates(text)
  # categories and images; image captions may hold links of their own
  text = re.sub(r"\[\[(?:Category|File|Image):(?:[^\[\]]|\[[^\]]*\])*\]\]", "", text, flags=re.I)
  text = re.sub(r"\[\[:?([^\]|]*)\|([^\]]*)\]\]", r"\2", text)
  text = re.sub(r"\[\[:?([^\]]*)\]\]", r"\1", text)
  text = re.sub(r"\[(https?://[^\s\]]+)\s+([^\]]+)\]", r"[\2](\1)", text)
  text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.S)
  text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
  text = re.sub(r"</?(?:span|font|small|big|div|center|u|s|sup|sub|nowiki|blockquote)[^>]*>", "", text, flags=re.I)
  text = text.replace("'''", "**").replace("''", "*")

  lines, out, preformatted = text.split("\n"), [], []
  i = 0
  while i < len(lines):
    line = lines[i]
    if line.startswith("{|"):  # wiki table
      end = next((j for j in range(i, len(lines)) if lines[j].startswith("|}")), len(lines) - 1)
      out += table_to_markdown(lines[i : end + 1])
      i = end + 1
      continue
    if line.startswith(PREFORMATTED) and line[1:].strip() and "\x00" not in line:  # ' code' on the wiki
      preformatted.append(line[1:])
      i += 1
      continue
    if preformatted:
      out.append(stash("", "\n".join(preformatted)))
      preformatted = []
    out.append(markdown_line(line.replace(PREFORMATTED, " ").lstrip()))
    i += 1
  if preformatted:
    out.append(stash("", "\n".join(preformatted)))

  text = "\n".join(out)
  text = re.sub(r"\x00(\d+)\x00", lambda m: code[int(m.group(1))], text)
  text = re.sub(r"[ \t]+\n", "\n", text)
  return re.sub(r"\n{3,}", "\n\n", text).strip()


def markdown_line(line: str) -> str:
  if m := re.match(r"^(={2,6})\s*(.*?)\s*\1\s*$", line):
    return "\n" + "#" * len(m.group(1)) + " " + m.group(2) + "\n"
  if m := re.match(r"^([*#:;]+)\s*(.*)$", line):
    marks, body = m.group(1), m.group(2)
    depth = "  " * (len(marks) - 1)
    if marks.endswith(";"):  # ';term : definition', ':;term:definition' (the ':' only indents)
      depth = "  " * max(len(marks) - 2, 0) if marks.startswith(":") else depth
      term, sep, definition = body.partition(":")
      return f"{depth}- **{term.strip()}**" + (f": {definition.strip()}" if sep else "")
    if marks.endswith("*"):
      return f"{depth}- {body}"
    if marks.endswith("#"):
      return f"{depth}1. {body}"
    return f"{depth}{body}" if len(marks) == 1 else f"{depth}- {body}"  # ':' indents
  return line


def table_to_markdown(rows: list[str]) -> list[str]:
  """A {| ... |} wiki table as a markdown table (attributes, spans and captions dropped)."""
  table: list[list[str]] = []
  header = False
  current: list[str] = []
  nested: list[str] = []  # a table inside a cell: flattened into that cell as 'a — b; c — d'
  for raw in rows[1:]:
    line = raw.replace(PREFORMATTED, " ").strip()
    if nested or line.startswith("{|"):
      nested.append(line)
      if line.startswith("|}"):
        inner = [r.strip("| ").replace(" || ", " — ") for r in nested[1:-1] if r.strip("| -")]
        if current:
          current[-1] = (current[-1] + " " + "; ".join(inner)).strip()
        nested = []
      continue
    if line.startswith("|}"):
      break
    if line.startswith("|+"):
      continue
    if line.startswith("|-"):
      if current:
        table.append(current)
      current = []
      continue
    if line.startswith(("!", "|")):
      is_header = line.startswith("!")
      header = header or (is_header and not table)
      body = line[2:] if line.startswith(("||", "!!")) else line[1:]  # continuation lines start with '||'
      for cell in re.split(r"!!|\|\|", body):
        if re.match(r"^\s*[\w-]+=\"[^\"]*\"[^|]*\|(?!\|)", cell):  # style="..." | content
          cell = cell.split("|", 1)[1]
        current.append(cell.strip())
    elif current:
      current[-1] += " " + line
  if current:
    table.append(current)
  if not table:
    return []
  width = max(len(r) for r in table)
  table = [r + [""] * (width - len(r)) for r in table]
  keep = [c for c in range(width) if any(r[c] for r in table)]  # drop columns empty in every row
  table, width = [[r[c] for c in keep] for r in table], len(keep)
  head, body = (table[0], table[1:]) if header else ([""] * width, table)

  def row(cells: list[str]) -> str:
    return "| " + " | ".join(c.replace("\n", " ").replace("|", "\\|") for c in cells) + " |"

  return ["", row(head), "|" + "---|" * width, *map(row, body), ""]


INNERMOST_TEMPLATE = re.compile(r"\{\{((?:(?!\{\{|\}\}).)*)\}\}", re.DOTALL)


def render_templates(text: str) -> str:
  """Replace templates with their markdown, innermost first (one pass per nesting level)."""
  text = text.replace("{{=}}", "=").replace("{{!}}", "\\|")
  for _ in range(20):
    rendered = INNERMOST_TEMPLATE.sub(lambda m: render_template(m.group(1)), text)
    if rendered == text:
      break
    text = rendered
  return text


def render_template(body: str) -> str:
  parts = split_params(body)
  name = parts[0].strip()
  key = name.lower()
  args: dict[str, str] = {}
  for n, part in enumerate(parts[1:], 1):
    k, eq, v = part.partition("=")
    if eq and re.fullmatch(r"\s*\w+\s*", k):
      args[k.strip()] = v.strip()
    else:
      args[str(n)] = part.strip()
  first = args.get("1", "")
  if key in DROP_TEMPLATES or key.startswith(("#", "displaytitle", "defaultsort")):
    return ""
  if key in ("api", "apilink", "api.inline") or key.startswith("apilink"):
    return f"`{(args.get('2') if key == 'api' and '2' in args else first) or args.get('framexml', '')}`"
  if key in ("apitype", "apiname", "apiname.added"):
    return f"`{first}`" if first else ""
  if key == "apisig":
    return "\n```lua\n" + first + "\n```\n"
  if key == "restrictedapi":
    return f"\n> **Restricted:** {first}" + (f". {args['note']}" if args.get("note") else "") + "\n"
  if key == "deprecatedapi":
    removed = f", removed in {args['removed']}" if args.get("removed") else ""
    return f"\n> **Deprecated** in patch {args.get('patch', '?')}{removed}.\n"
  if key == "removedapi":
    return "\n> **Removed** from the game" + (f" in patch {first}" if first else "") + ".\n"
  if m := re.match(r"patch (\S+)", key):
    note = args.get("note") or first
    return f"**Patch {m.group(1)}**" + (f": {note}" if note else "")
  if key.endswith("-inline"):
    return f"({INLINE_FLAVORS.get(key.removesuffix('-inline'), name.removesuffix('-inline'))})"
  if key in ("ref web", "elink"):
    title = args.get("title") or args.get("site") or args.get("url", "")
    return f"[{title}]({args.get('url') or args.get('link', '')})"
  if key == "apirow":  # a row of a {| {{apitable}} ... |} table
    return f"|-\n| {first} || {args.get('2', '')}"
  if key in ("apitable", "apitable.style", "apitable.captionstyle"):
    return ""
  if key == "blizz":
    return "Blizzard"
  if key == "bluepost":
    return f"\n> **{args.get('poster', 'Blizzard')}** ({args.get('date', '')}): {args.get('body', '')}\n"
  if key in ("tooltip", "color", "colour"):
    return args.get("2", first)
  return first if len(parts) == 2 and len(first) < 80 else ""  # unknown simple wrappers keep their text


# --- Usage in Blizzard's UI source ------------------------------------------------------------

CHAIN_RE = re.compile(r"(?<![\w.:])([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)")  # UnitAura, C_Item.GetItemInfo, "UNIT_AURA"
METHOD_CALL_RE = re.compile(r":\s*([A-Za-z_]\w*)\s*\(")  # frame:SetPoint(
# Blizzard's API documentation declares names rather than using them; not counted as usage.
DECLARATION_DIRS = ("Blizzard_APIDocumentationGenerated", "Blizzard_APIDocumentation")


@dataclass
class UsageIndex:
  """Where names occur in a wow-ui-source checkout: name -> repository path -> [uses, first line]."""

  label: str  # 'forever @ 15666a6 1.60.1 (70245)'
  names: dict[str, dict[str, list[int]]]  # global/namespaced functions and events
  methods: dict[str, dict[str, list[int]]]  # ':Method(' calls, whatever the receiver


def scan_usage(checkout: Path, label: str, names: set[str], methods: set[str]) -> UsageIndex:
  """One pass over Interface/**/*.lua|xml, recording only the wanted names. A dotted chain counts
  for each of its prefixes (C_Item.GetItemInfo in C_Item.GetItemInfo(...)); events match inside
  strings ("UNIT_AURA"); methods match ':Name(' calls."""
  found: dict[str, dict[str, list[int]]] = {}
  found_methods: dict[str, dict[str, list[int]]] = {}

  def record(index: dict, name: str, path: str, line: int) -> None:
    hit = index.setdefault(name, {}).setdefault(path, [0, line])
    hit[0] += 1

  for path in sorted((checkout / "Interface").rglob("*")):
    rel = path.relative_to(checkout).as_posix()
    if path.suffix not in (".lua", ".xml") or any(f"/{d}/" in rel for d in DECLARATION_DIRS):
      continue
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
      for m in CHAIN_RE.finditer(line):
        parts = m.group(1).split(".")
        for k in range(1, len(parts) + 1):
          if (name := ".".join(parts[:k])) in names:
            record(found, name, rel, line_no)
      for m in METHOD_CALL_RE.finditer(line):
        if m.group(1) in methods:
          record(found_methods, m.group(1), rel, line_no)
  return UsageIndex(label, found, found_methods)


def usage_section(entry: Entry, usage: UsageIndex, limit: int) -> tuple[str, int]:
  """The '## Used in wow-ui-source' section for an entry, and how many files use it."""
  if entry.kind == "method":
    method = entry.name.split(":", 1)[1]
    hits = usage.methods.get(method, {})
    verb, what = "call", f"`:{method}(` on some object (the receiver's type is not checked)"
  else:
    hits = usage.names.get(entry.name, {})
    verb, what = "use", f"`{entry.name}`"
  heading = f"## Used in wow-ui-source ({usage.label})"
  if not hits:
    return f"{heading}\n\nNo file of Blizzard's UI source uses {what.split(' (')[0]}.", 0
  ranked = sorted(hits.items(), key=lambda item: (-item[1][0], item[0]))
  shown = ranked[:limit]
  lines = [f"- wow-ui-source/{path}:{line} ({count} use{'s' if count != 1 else ''})" for path, (count, line) in shown]
  more = f"; the {len(shown)} with the most uses" if len(ranked) > len(shown) else ""
  files = f"{len(ranked)} files {verb}" if len(ranked) != 1 else f"1 file {verb}s"
  return f"{heading}\n\n{files} {what}{more}:\n\n" + "\n".join(lines), len(ranked)


# --- Files -----------------------------------------------------------------------------------


def entry_path(entry: Entry) -> str:
  if entry.kind == "method":
    cls, method = entry.name.split(":", 1)
    return f"methods/{cls}/{method}.md"
  return f"{KIND_DIRS[entry.kind]}/{entry.name}.md"


def front_matter(entry: Entry) -> str:
  def value(v) -> str:
    return json.dumps(v, ensure_ascii=False)

  fields = {
    "name": entry.name,
    "kind": entry.kind,
    "clients": entry.clients,
    "library": entry.library_file,
    "restrictions": entry.tags,
    "blizzard_flags": entry.flags,
    "deprecated": entry.deprecated,
    "wiki": WIKI_URL + entry.page_title.replace(" ", "_") if entry.page_title else "",
    "aliases": entry.aliases,
    "ui_source_files": entry.ui_source_files,
  }
  lines = [f"{k}: {value(v)}" for k, v in fields.items() if v not in ("", [], {}, 0)]
  return "---\n" + "\n".join(lines) + "\n---"


def render_entry(entry: Entry, expand: Callable[[str], str], usage: UsageIndex | None = None, limit: int = 50) -> str:
  usage_text = ""
  if usage:
    usage_text, entry.ui_source_files = usage_section(entry, usage, limit)
  parts = [front_matter(entry), f"# {entry.name}"]
  if entry.notes:
    parts.append("\n".join(f"> {note}" for note in entry.notes))
  parts.append("## LuaLS annotation\n\n```lua\n" + entry.annotation.strip() + "\n```")
  if usage_text:
    parts.append(usage_text)
  if entry.page_text:
    parts.append(f"## Wiki: {entry.page_title}\n\n" + demote(wiki_to_markdown(entry.page_text, expand)))
  else:
    parts.append("No wiki page documents this; the annotation above is everything known.")
  return "\n\n".join(parts) + "\n"


def demote(markdown: str) -> str:
  """Wiki '==' headings render as '##'; nest them under the '## Wiki' heading."""
  return re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", markdown, flags=re.M)


def write_reference(
  out: Path,
  entries: list[Entry],
  guides: dict[str, str],
  expand: Callable[[str], str],
  usage: UsageIndex | None = None,
  usage_limit: int = 50,
) -> None:
  """Write reference/: entry files, index.md, README.md and guides/ (title -> markdown or wikitext).
  With a UsageIndex each entry lists the wow-ui-source files that use it (at most usage_limit)."""
  shutil.rmtree(out, ignore_errors=True)
  for entry in entries:
    path = out / entry_path(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_entry(entry, expand, usage, usage_limit), encoding="utf-8")

  (out / "guides").mkdir(parents=True, exist_ok=True)
  for title, body in guides.items():
    if title.endswith(".md"):  # already markdown (docs/Security.md)
      text = body
    else:
      text = f"# {title}\n\nFrom {WIKI_URL}{title.replace(' ', '_')}\n\n" + wiki_to_markdown(body, expand)
    name = title.removesuffix(".md").replace("/", "_").replace(":", "_")
    (out / "guides" / f"{name}.md").write_text(text + "\n", encoding="utf-8")

  index = ["# Index", "", "One line per entry: name, clients, restrictions, summary, file.", ""]
  for kind, title in (("function", "Functions"), ("method", "Widget methods"), ("event", "Events")):
    index += [f"## {title}", ""]
    for entry in sorted((e for e in entries if e.kind == kind), key=lambda e: e.name.lower()):
      labels = ("/".join(entry.clients), *(f"#{t}" for t in entry.tags), "deprecated" if entry.deprecated else "")
      meta = ", ".join(x for x in labels if x)
      summary = f" — {entry.summary}" if entry.summary else ""
      index.append(f"- `{entry.name}` ({meta}){summary} → {entry_path(entry)}")
    index.append("")
  (out / "index.md").write_text("\n".join(index), encoding="utf-8")
  usage_label = usage.label if usage else "not generated"
  readme = README.format(count=len(entries), guides=", ".join(sorted(guides)), usage=usage_label)
  (out / "README.md").write_text(readme, encoding="utf-8")


README = """# WoW API reference: Classic Era + Forever

{count} entries, one markdown file per function, widget method and event, for AI tools, search and
reading. The LuaLS annotations for the language server are in `library/`, generated alongside.

- `index.md`: one line per entry (name, clients, restrictions, summary, file). Start here.
- `functions/<Name>.md`, `methods/<Class>/<Method>.md`, `events/<EVENT>.md`
- `guides/`: {guides}

Each entry file:

1. YAML front matter: `name`, `kind`, `clients` (which of Era/Forever have it), `library` (the
   annotation file), `restrictions` (wiki tags: protected, hwevent, nocombat, secureframe, ...),
   `blizzard_flags` (Blizzard documentation flags and the clients that set them), `deprecated`
   (the replacement to use), `wiki` (source page), `aliases` (other names that redirect to it),
   `ui_source_files` (how many files of Blizzard's UI source use it).
2. Notes such as "Era only" or how a deprecated fallback is loaded.
3. The LuaLS annotation exactly as in `library/`: typed parameters, returns and overloads.
4. Used in wow-ui-source: the files of Blizzard's own UI (https://github.com/Gethe/wow-ui-source,
   {usage}) that use it, as `wow-ui-source/<path>:<first line> (uses)`, most uses first.
   Open them to see real usage. Methods are matched by `:Name(` calls on any object.
5. The wiki page as markdown: description, arguments, returns, details, examples, patch changes.
   Wiki pages describe retail first; where the annotation and the page differ, trust the
   annotation and `clients` for Era and Forever.
"""
