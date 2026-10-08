# WoW-API generator

This repo builds a World of Warcraft API library for **Classic Era** and **Forever** and nothing
else. Everything it produces lands in the gitignored `WoW-API/` folder:

- `WoW-API/library/` holds LuaLS annotations (`---@meta` files) for the language server. Addons
  point `Lua.workspace.library` at it.
- `WoW-API/reference/` holds one markdown file per function, widget method and event, meant for
  AI tools and for reading.

Read `docs/Findings.md` before changing how data is parsed or merged. It records how the wiki,
Blizzard's sources and Ketho's data behave, including the quirks that cost time to discover.

## Commands

Run Python only through `uv` (`uv run ...`), never `python` or `python3` directly.

```bash
uv run wiki_dump.py                      # fetch warcraft.wiki.gg into dump/ (~20 min, via proxies)
uv run wiki_dump.py build                # re-parse dump/raw offline (seconds)
uv run generate.py sources               # clone/update sources/ (Gethe, Ketho BIR, Ketho annotations)
uv run generate.py                       # build WoW-API/library and WoW-API/reference (~11 s)
uv run generate.py --usage-branch classic_era    # "Used in wow-ui-source" from another branch
uv run --with pytest --with requests pytest test_wiki_dump.py test_generate.py test_reference.py
uvx ruff check --select E,F,W,B --line-length 120 wiki_dump.py generate.py reference.py test_*.py
```

`wiki_dump.py` uses scraper-questie's proxies by default. It reads `PROXY_HOST`, `PROXY_USERNAME`
and `PROXY_PASSWORD` from `~/projects/scraper-questie/wh_parser/.env` and rotates ports 8001-8010.
Use `--network-mode local` to go direct. Never print the `.env` values.

## Layout

| Path | What it is |
|---|---|
| `wiki_dump.py` | Fetches the wiki (`fetch`) into `dump/raw/`, parses it (`build`) into `dump/entries.jsonl`, `listings.jsonl`, `names.tsv`, `data/*.json`. Also holds the shared parsing helpers (`LuaTableParser`, `template_calls`, `clean`, `api_name`, ...). |
| `generate.py` | Builds `WoW-API/library` from `sources/` + `dump/`, and hands one `Entry` per item to `reference.py`. |
| `reference.py` | Converts wikitext to markdown, scans wow-ui-source for usages, writes `WoW-API/reference`. Imports only from `wiki_dump.py`. |
| `docs/Security.md` | Hand-written guide to secure execution and taint. Copied verbatim to the top of `library/Security/Security.lua` and into `reference/guides/`. Edit it freely. |
| `docs/Findings.md` | What we learned about the sources. |
| `test_*.py` | Focused tests of the parsing rules, built from real wiki and Blizzard snippets. |
| `dump/` | Wiki cache (gitignored). `dump/raw/pages/<Namespace>/<Title>.wiki` is every page's wikitext. |
| `sources/` | Shallow sparse clones (gitignored): `ui-era`, `ui-forever` (Gethe/wow-ui-source, full `Interface/`), `bir-era`, `bir-forever` (Ketho/BlizzardInterfaceResources `Resources/`), `ketho` (Ketho/vscode-wow-api `Annotations/Core`). |

## How generate.py decides what goes where

1. `load_client` reads one client (flavor) from its BIR dumps, Blizzard's generated API docs and its
   `Blizzard_Deprecated*` addons. A function exists when a client's BIR dump lists it or one of
   the deprecation addons that client loads defines it. Anything else is not annotated, whatever
   the wiki says.
2. `build_functions` gives each existing function one definition. The first source that applies wins:
   - Blizzard's documentation for the client (typed). Era's signature is primary and a different
     Forever signature becomes an `@overload`.
   - The wiki page that documents it. That is its own page, a page whose `{{apisig}}` names it, or
     the `/Classic` subpage for Era-only functions.
   - Ketho's curated block, only when it has a `---@generic` signature (`CreateFrame`).
   - A `Blizzard_Deprecated` fallback's argument list.
   - `...` with "Undocumented".
3. Restricted items go to `library/Security/Security.lua` instead of their usual file
   (`security_section`, `restricted_on`). Wiki tags count for every client that has the item;
   Blizzard flags only for the client whose docs set them.
4. `build_widgets` builds classes from BIR `WidgetAPI`. Method signatures come from Ketho's block
   for the class, an ancestor or a related class. Blizzard's own method docs win when they list
   more parameters. The wiki's method lists are the last resort.
5. Each builder appends an `Entry` per item; `reference.write_reference` renders them.
6. `type_usage` scans the finished library and writes `Type/Undefined.lua` stubs for every type
   that is referenced but defined nowhere.

## Common changes

| To change | Edit |
|---|---|
| Which clients/branches | `FLAVORS`, `FLAVOR_LABEL`, `GAME_TYPES`, `TOC_TOKENS` in `generate.py` |
| The "Era only" tag text | `flavor_tag` |
| Output folder names | `EXPORT`, `OUT`, `REFERENCE`, `GLOBAL_FILE`, `SECURITY_FILE` |
| Which file a function lands in | the `out = ...` branches in `build_functions` |
| Security sections and their rules | `SECURITY_SECTIONS`, `USAGE_TAGS`, `WIDGET_TAGS`, `SECURITY_TOOLS`, `SECURITY_FLAG_RE`, `security_section` |
| The security guide text | `docs/Security.md` |
| How the wiki's optional args are read | `signature_args`, `sig_arg`, `sig_params` |
| How Arguments/Returns sections are read | `definitions` (and `Transcluder`, `evaluate` for transclusions) |
| Wikitext to markdown | `wiki_to_markdown`, `render_template`, `table_to_markdown` in `reference.py` |
| Reference file layout and front matter | `entry_path`, `front_matter`, `render_entry`, `README` in `reference.py` |
| "Used in wow-ui-source" | `USAGE_BRANCH`, `USAGE_LIMIT`, `scan_usage`, `usage_section`, `DECLARATION_DIRS` |
| Which Ketho folders are copied | the copy loop at the top of `generate()` and `copy_framexml` |
| What the wiki fetch includes | `SEED_TEMPLATES`, `INDEX_PAGES`, `GUIDE_PAGES`, `SCOPE_PREFIXES` in `wiki_dump.py` |

## Validating a change

Run these in order of cost:

1. The tests and ruff (commands above). Add a test with a real snippet when you fix a parsing case.
2. `uv run generate.py`, then spot-check the items you touched in `WoW-API/library` and
   `WoW-API/reference`. Read the output itself. A clean run proves little.
3. Syntax: `for f in $(find WoW-API/library -name '*.lua'); do luac -p "$f"; done` must print nothing.
4. LuaLS. Put `{"runtime.version": "Lua 5.1", "workspace.checkThirdParty": false}` in a temporary
   `.luarc.json` inside `WoW-API/library`, run
   `~/LuaLS/bin/lua-language-server --check "$PWD" --checklevel=Warning --logpath <tmpdir>`, then
   delete the `.luarc.json`. The expected result is 8 warnings, all in Ketho's
   `FrameXML/Blizzard_SharedXML/GlobalCallbackRegistry.lua` and `TableUtil.lua` (upstream).
   Anything else is new.
5. For behaviour, write a small addon file in a scratch folder whose `.luarc.json` has
   `"workspace.library": ["<repo>/WoW-API/library"]` and check it with LuaLS. Valid calls must
   stay quiet; deprecated calls (`UnitAura` on Era) must warn.

## Rules that keep the output right

- Use the BIR dumps for existence and Blizzard's docs for types. The wiki is retail-first, so trust it
  only for descriptions, tags and functions Blizzard does not document.
- Never make Blizzard `ScriptObject` doc systems into globals. They document widget methods
  (`SimpleButtonAPI` has `GetText`), and treating them as globals overwrote real functions.
- Compare names the way MediaWiki stores titles. Titles use spaces, so `C_Item.GetItemInfo` is the
  page `API:C Item.GetItemInfo`. Use `api_name`, never ad hoc string replaces.
- Respect TOC gating for anything loaded per client: `[AllowLoadGameType]`,
  `[ExcludeLoadGameType]`, `[Game]`, `[Family]`.
- Keep `WoW-API/` generated. Hand edits there are lost on the next run.
- Do not hit the wiki without the throttle. Unthrottled probes got HTTP 429 within seconds.
- The wiki's robots.txt says `ai-train=no`. The dump is for reference use; do not use it to train models.

## Code style

Two-space indentation, 120-column lines, focused tests over broad ones. Keep docstrings and comments
in sync with behaviour. `ruff format` would switch to four spaces, so don't run it.
