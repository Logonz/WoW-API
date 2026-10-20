# WoW-API

Generates a World of Warcraft API library for **Classic Era** and **Forever**:

- `WoW-API/library/`: LuaLS annotations (`---@meta` files) for completion, hover docs and
  type checking in your editor.
- `WoW-API/reference/`: one markdown file per function, widget method and event, for reading
  and for AI tools.

An item is annotated only if the client actually has it. Types come from Blizzard's generated API
docs, and descriptions, restriction tags and the remaining signatures come from
[warcraft.wiki.gg](https://warcraft.wiki.gg). Restricted API (protected, hardware event, combat
lockdown, secret values) is collected in `library/Security/Security.lua` together with a guide to
secure execution and taint.

## Build

Requires [uv](https://docs.astral.sh/uv/). The output is generated and not checked in.

```bash
uv run wiki_dump.py --network-mode local   # fetch the wiki into dump/ (throttled, slow)
uv run generate.py sources                 # clone Blizzard's UI source and Ketho's data into sources/
uv run generate.py                         # build WoW-API/library and WoW-API/reference
```

## Use in an addon

Point LuaLS at the library in your addon's `.luarc.json`:

```json
{
  "runtime.version": "Lua 5.1",
  "workspace.library": ["/path/to/WoW-API/WoW-API/library"]
}
```

## Sources

- [Gethe/wow-ui-source](https://github.com/Gethe/wow-ui-source): Blizzard's UI code and API docs
- [Ketho/BlizzardInterfaceResources](https://github.com/Ketho/BlizzardInterfaceResources): what
  each client has
- [Ketho/vscode-wow-api](https://github.com/Ketho/vscode-wow-api): widget, Lua and FrameXML
  annotations
- [warcraft.wiki.gg](https://warcraft.wiki.gg): descriptions and undocumented functions. Its
  robots.txt says `ai-train=no`, so the dump is for reference only and must not be used to train models.

`docs/Findings.md` explains how these sources behave and how they are merged.
