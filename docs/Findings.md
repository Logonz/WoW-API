# Findings

What we learned building this generator. Each item says where it matters in the code. Dates and
counts are from October 2026 (wiki dump of 2026-10-08, Era 1.15.9 build 70003, Forever 1.60.1
build 70245).

## The clients

- **Era** is Gethe branch `classic_era`, game type `vanilla` in the `classic` family.
- **Forever** is Gethe branch `forever`. Blizzard developed it as **camelot**, and that is the name
  the TOCs and the wiki's data use. Forever belongs to the **mainline** family. Its TOCs contain
  lines like `[AllowLoadGameType mainline] [ExcludeLoadGameType camelot]`, which only make sense if
  `mainline` includes camelot.
- Era has 5,060 C globals and Forever 6,883. 4,550 are shared, 510 are Era only (arena teams,
  `AbandonQuest`) and 2,333 Forever only (archaeology, glyphs, retail systems).
- Forever has secret values (retail 12.0 system). Era does not have them in the same way. Era's
  Blizzard docs mark no secret returns or predicates, only a few `Requires...` preconditions.
- The Forever branch also ships UI files that only other game types load (`Classic/` folders).
  That is fine for usage references; the user accepted it.

## Ketho/BlizzardInterfaceResources (BIR)

Branches `classic_era` and `forever`, folder `Resources/`. Dumped from the running clients, so
this is the authority on what exists. Formats, as parsed by `load_client`:

| File | Shape | Notes |
|---|---|---|
| `GlobalAPI.lua` | `return {GlobalAPI, LuaAPI}` | C functions only. Lua-defined globals are **not** here. |
| `FrameXML.lua` | `return {FrameXML, LoadOnDemand}` | Lua-defined globals, including dotted names like `AuraUtil.ForEachAura`. |
| `Mixins.lua` | list | Mixin names. |
| `Frames.lua` | `return {Frames, LoadOnDemand}` | Named global frames (572). No widget types. |
| `Templates.lua` | `name -> {type = "Button"}` | 32 `Secure*`/`Insecure*` templates per client. |
| `WidgetAPI.lua` | `class -> {inherits, methods, handlers}` | `Region` lists itself as its parent. `build_widgets` falls back to Ketho's parents for that. Resizing methods (`SetPoint`, `ClearAllPoints`) sit on `ScriptRegion` here. |
| `Events.lua` | `system -> {names}` | |
| `LuaEnum.lua` | `Enum = {...}`, `Constants = {...}`, then `LE_X = n` lines | `LE_*` are plain assignments, read with a regex. |
| `CVars.lua` | `return {CVars, PTR}`, data under `CVars.var` | Columns: default, category, account, character, (secure), help. |

`parse_lua_module` reads these statically. It honours `return name` and the
`for k, v in pairs(a) do b[k] = v end` merge, and never executes Lua.

## Gethe/wow-ui-source

Checked out whole (`Interface/`, about 50 MB per branch) because three things need it: Blizzard's
generated API docs, the deprecation addons, and the usage scan.

### Blizzard_APIDocumentationGenerated

- One file per system: `{Name, Type, Namespace, Functions, Events, Tables}`. Arguments carry
  `Nilable` and `Default`. Tables are `Structure`, `Enumeration` or `CallbackType`.
- `Type = "ScriptObject"` systems (`SimpleButtonAPI`, `SimpleFrameAPI`, ...) have no namespace and
  document **widget methods**. Treating them as globals once gave `GetText()` a button's signature
  and put `GetTime` in the wrong file. `system_owner` maps them to classes using the wiki's
  `Module:Wowapi/data/scriptobject` table.
- Security flags per client. Both clients have `IsProtectedFunction`, `HasRestrictions`,
  `SecureHooksAllowed` and `RestrictedForMacroChatMessages`. Only Forever has `SecretArguments`
  (3,942 entries), `SecretReturns`, `SecretWhen*`, `SecretIn*`, `SecretPayloads` and
  `ChecksForbiddenAspects`. `blizzard_security_flags` collects them.
- The docs list parameters as required where the real API accepts nil (`SetPoint`). Ketho's widget
  blocks mark them optional, which is why his block wins unless Blizzard lists more parameters
  (`PlayerModel:SetRotation(radians, animate)`).

### Blizzard_Deprecated* addons

- On Era 1.15.8+, `UnitAura`, `UnitBuff`, `UnitDebuff` and `GetTalentInfo` exist only as Lua
  fallbacks there, loaded while the CVar `loadDeprecationFallbacks` is on. BIR's `GlobalAPI` does
  not list them. Across both clients 198 functions are fallback-only. The library marks them
  `@deprecated` with the `C_` replacement: 188 in `API/Deprecated.lua`, and 10 restricted ones in
  `Security/Security.lua`.
- Two shapes: `X = function(args) ... end` and aliases `X = C_Ns.Fn`. Aliases take the
  replacement's Blizzard signature. Fallbacks on a local (`searcher.Foo`) are ignored.
- TOC lines are gated with `[AllowLoadGameType a, b]` and `[ExcludeLoadGameType c]`, and paths use
  tokens: `Deprecated_Specialization_[Game].lua`, `[Family]\Foo.lua`. `toc_files` resolves them
  with `GAME_TYPES` and `TOC_TOKENS`: Era `{vanilla, classic}`, Game `Vanilla`, Family `Classic`;
  Forever `{camelot, mainline}`, Game `Camelot`, Family `Mainline`.
- A function can be a C function on one client and a fallback on the other
  (`GetWeaponEnchantInfo` is C on Era, a fallback on Forever). It is only `@deprecated` when every
  client that has it has only the fallback; otherwise the doc says "Deprecated on Forever".
- The fallback's body end is found by matching `end` at the header's indentation; cutting at the
  first `end` made replacement hints spill into the next fallback.

## warcraft.wiki.gg

MediaWiki 1.43 with `api.php`, Scribunto and CirrusSearch; no Cargo, no Semantic MediaWiki. The
dump holds 27,800 pages (13,055 redirects) from about 1,550 requests.

### Namespaces and titles

- Content is in `API:` (3000, functions and widget methods) and `Event:` (3004). The `CVar:` (3002)
  and `Widget:` (274) namespaces exist but are empty.
- Many API pages live in the main namespace: `UIOBJECT Frame` (widget classes and their method
  lists), `UIHANDLER`, `ScriptObject`, `INTRINSIC`, `CVar X`, `MACRO x`, `Structure X`, `Enum.X`,
  `API types/X`, `XML/X`, plus 189 old-style `API X` content pages.
- MediaWiki stores titles with spaces. `C_Item.GetItemInfo` is the page `API:C Item.GetItemInfo`;
  the old `API_C_Item.GetItemInfo` is a redirect. `api_name` turns titles back into API names using
  the wiki's own rules (`Module:Wowapi/src/page`). Spaces become `_` for functions and events, and
  `Class Method` becomes `Class:Method` only when `Class` is a known widget, ScriptObject or mixin.
  `API EJ GetCurrentInstance` stays `EJ_GetCurrentInstance`.
- Titles can end in `()` (`API FramerateFrame:Toggle()`), so `clean` must keep parentheses.
- The page type comes from the template it uses: `{{wowapi}}`, `{{widgetmethod}}`,
  `{{intrinsicmethod}}`, `{{wowapievent}}`, `{{wowapitype}}`, `{{widget}}`, `{{widgethandler}}`,
  `{{wowsystem}}`, `{{luaapi}}`, `{{framexmlfunc}}`, `{{cvar}}`, `{{Macro API}}`, `{{removedapi}}`.
  Ignore templates inside HTML comments; editor boilerplate like `<!-- or {{widgetmethod}} -->`
  misclassified pages.

### Page content

- Signatures are `{{apisig|returns {{=}} Name(args)}}`. `{{=}}` is an escaped `=`. One apisig can
  hold several call forms sharing the returns: `... = GetSpellInfo(spell) = GetSpellInfo(index,
  bookType)`. The first becomes the signature and the others `@overload`s.
- Argument and return lines are `:;name:{{apitype|Type?|default=x}} - description`, the older
  `;name : Type - description`, or, in old templates, `:;1. name : <span class="apitype">string</span>`.
  A trailing `?` or `default=` means optional; `{{apitype|number|string}}` is a union.
- Optional arguments are written many ways, all handled by `signature_args`:

  | Notation | Example | Meaning |
  |---|---|---|
  | `a [, b]`, `a [, b [, c]]`, `a [, b] [, c, d]`, `[a [, b]]` | `SetPoint(point [, relativeTo [, relativePoint]] [, x, y])` | optional |
  | `a, [b], c` | `C_Club.CreateClub(name, [shortName], description, ...)` | optional, pass nil |
  | `[a,] b` | `hooksecurefunc([tbl,] functionName, hookfunc)` | may be left out; becomes an `@overload` |
  | `a{, b}` | `SetTradeSkillInvSlotFilter(slotIndex, onOff{, exclusive})` | braces as brackets |
  | `a?` | `...(recipeID, craftingReagents, recraftItemGUID?)` | optional |
  | `a or b or c` | `EquipItemByName(itemId or itemName or itemLink[, slot])` | one argument, union type |
  | `...name` | `RegisterForClicks(...buttons)` | vararg |
  | prose | `;rank : String (Optional)`, `Optional, will return ...` | optional |

  Unbalanced brackets occur on real pages (`fastrandom(low,] high])`, `[, returnTable`).
- Pages pull text from other pages. `{{:SpellArg}}` transcludes a page, often inside
  `<onlyinclude>` with `{{#if:{{{param|}}}|...}}`. Some returns come from plain templates whose
  body is a definition list (`{{AuraType|aura}}` holds `UnitAura`'s 15 returns). `Transcluder`
  expands both kinds and leaves ordinary templates alone.
- Pages that document several functions use `===Name===` subsections. Namespaced functions use the
  short name there (`===GetItemInfoByID===` for `C_BlackMarket.GetItemInfoByID`).
- A few pages have no `{{apisig}}` and show the call as preformatted text
  (` baseDefense, armorDefense = UnitDefense(unit);`). `wiki_funcs(want=...)` reads that.
- Classic-specific signatures live on `/Classic` subpages (`API:GetTalentInfo/Classic`). Only 2
  exist in the dump; Era-only functions use them.
- `prop=links` never reports whether a link target exists. Red links have to be checked by querying
  the targets. The 3,493 missing titles in `dump/raw/missing.json` are real. Most are CVars listed
  on `Console variables/Complete list` and functions listed on `World of Warcraft API` without a page.

### Data modules

The structured facts are Lua tables in `Module:Wowapi/data/*`, exported to `dump/data/*.json`.
The wiki's data comes from Ketho/WowDoc.

| Module | Contents |
|---|---|
| `gametype/function`, `event`, `widget`, `scriptobject` | Flavor bitmask per name: `0x1` standard, `0x2` forever (camelot), `0x4` mists, `0x8` tbc, `0x10` vanilla |
| `patch/<flavor>/function`, `event` | `{added, removed}` per flavor. `patch/standard/function` merges a second `lua` table with a `for ... in pairs` loop. |
| `group` | Rename groups, e.g. `{"C_ActionBar.GetActionAutocast", "GetActionAutocast"}` |
| `group/method` | Methods shared by several widget classes |
| `predicate/*` | Secret-value predicates and aspects (retail/Forever) |
| `system`, `system/function`, `event`, `table` | System membership. The wiki inverts `system/*` at runtime; the JSON keeps system -> names. |
| `scriptobject` | Blizzard system name -> widget class (`SimpleButtonAPI` -> `Button`) |
| `cfg` | Current build per flavor |
| `Module:API info/cvar/data` | CVars with default, category, scope, help |
| `Module:API info/restricted` | The official meaning of every `#protected`-style tag |

Some of this data lags the pages. It files 27 methods under `ScriptRegion` (`ScriptRegion:ClearAllPoints`)
while the pages are `ScriptRegionResizing ClearAllPoints`, and nothing on the wiki links the two.
The generator connects them with the "related class" rule in `build_widgets.donor`: one class name
being a prefix of the other.

### Index pages carry extra facts

`World of Warcraft API`, `World of Warcraft API/Classic`, `Events` and every `UIOBJECT X` page list
APIs with `{{apitag|protected}}`, `secureframe`, `hwevent`, `nocombat`, `restrictedframe`,
`anchorfamily`, ... and with `{{apicompat|0x1f}}` flavor bits. These tags are not always on the
function pages, so `parse_listings` reads them into `dump/listings.jsonl`. Their `{{apilink}}`
name is the first positional parameter, or `framexml=` for FrameXML functions.

### Fetching

- Throttle every request. A probe without a delay got HTTP 429 in seconds. The dump runs at 0.5 s
  per request across 10 proxy ports with no 429s.
- The fetch seeds from the API/Event namespaces, every page embedding the API templates, the
  index pages, the guide pages and the data modules. It then follows redirects, transclusions,
  `{{api|...}}` links (mapped like `Module:Api.link`: `t=e` -> `Event:`, `t=o` -> `UIOBJECT`, ...)
  and in-scope `[[links]]` until nothing new turns up, usually 4 rounds.
- `robots.txt` sets `Content-Signal: search=yes, ai-train=no, use=reference`.

## Ketho/vscode-wow-api

`Annotations/Core` is mainline-oriented. What we reuse and why:

- `Type/`, `Lua/`, `ScriptObject/`, `Widget/UIType/`, `Widget/Intrinsic/` are copied as they are.
- `FrameXML/` is copied per file, only when at least half of the globals a file defines exist in
  Era or Forever (`copy_framexml`). Mainline-only files such as `Menu.lua` and his own deprecation
  files are skipped.
- Widget method blocks are typed and mark optional arguments; they are the default source for
  method signatures.
- `Data/Wiki.lua` has 1,879 curated function blocks, but some mark optional arguments as required
  (`GetText(token, gender, ordinal)`). Only blocks with `---@generic` are used (`CreateFrame`,
  `securecall`, `securecallfunction`).
- His `CreateFrame` returns `table|T`, so LuaLS does not flag unknown methods on frames. That is
  his design, kept on purpose.
- Two upstream LuaLS warnings come with his files (`EventRegistry` injection in
  `GlobalCallbackRegistry.lua`, `n` injection in `TableUtil.lua`).
- Ketho's annotations do not cover Classic-only functions (`UnitAura` is absent). The old
  WoW-API project filled that gap with LLM output (`Functions-AI/`); this generator uses the wiki.

## LuaLS behaviour we rely on

- A class can be declared in several files. `Security.lua` repeats `---@class Frame` and
  `local Frame = {}` before moving restricted methods there, and they still resolve on frames.
- Undefined types produce warnings, so `Type/Undefined.lua` stubs them. Names used as a class
  parent must be stubbed as `---@class`, the rest as `---@alias X any`.
- An alias of `string` with listed values (`FrameEvent`) gives completion but does not reject
  other strings.
- Raw newlines in doc text break the comment. Blizzard's doc strings contain `\n` and `\t`, so
  `one_line` escapes control characters.

## Earlier projects

- `/mnt/d/Projekt/WoW-API/WoW-API` is the previous output (a fork of Ketho's layout plus
  `Functions-AI/`). Its structure inspired this one; its content is superseded.
- `/mnt/d/Projekt/wow-api-libraries` generated the missing Classic functions with OpenAI and Gemini
  from scraped HTML.
- `/mnt/d/Projekt/ProgrammingAssistant` scraped wowpedia/warcraft.wiki.gg with `Special:Export`.
- `~/projects/scraper-questie` owns the proxy setup this repo borrows.

## Known gaps

- About 9,000 Lua globals of Blizzard's UI have no annotation (`StaticPopup_Show`, `Clamp`,
  `Round`, the `SecureHandler*` helpers). BIR's `FrameXML.lua` lists them. `docs/Security.md`
  explains the secure helpers.
- Only 2 `/Classic` subpages exist, so most functions show retail's wiki text even when Era
  differs (`GetBattlefieldStatus` returns differ).
- Usage for widget methods is matched by `:Name(` calls on any object; common methods match many
  unrelated classes.
- Seven Secure Execution guide pages were added to the fetch list after the last dump and appear
  in `reference/guides/` after the next `uv run wiki_dump.py`.
