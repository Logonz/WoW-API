# Secure execution, taint and restricted API

This file is the header of `Security/Security.lua` in the generated library. `generate.py` copies it
in verbatim and appends, below it, a generated summary and every function, widget method and type
that is restricted on Classic Era or Forever. Edit this document freely; the lists are rebuilt from
the sources on every run.

Sources on warcraft.wiki.gg (the Secure Execution trail):
[Secure Execution and Tainting](https://warcraft.wiki.gg/wiki/Secure_Execution_and_Tainting),
[Object security](https://warcraft.wiki.gg/wiki/Object_security),
[SecureTemplates](https://warcraft.wiki.gg/wiki/SecureTemplates),
[SecureActionButtonTemplate](https://warcraft.wiki.gg/wiki/SecureActionButtonTemplate),
[SecureHandlers](https://warcraft.wiki.gg/wiki/SecureHandlers),
[SecureStateDriver](https://warcraft.wiki.gg/wiki/SecureStateDriver),
[RestrictedEnvironment](https://warcraft.wiki.gg/wiki/RestrictedEnvironment),
[Secret Values](https://warcraft.wiki.gg/wiki/Secret_Values),
[Template:Restrictedapi](https://warcraft.wiki.gg/wiki/Template:Restrictedapi) (the restriction tags).

## Why it exists

The UI API "mandates human decision-making, particularly in combat": addons may show information
and suggest, but may not decide whom to target or what to cast. Since patch 2.0 (and on every
Classic client) this is enforced by secure execution and taint.

## Taint

- Lua execution starts **secure**. Blizzard's signed FrameXML and AddOns, and their saved
  variables, are secure; every third-party AddOn, its saved variables and `/script` are **tainted**.
- Every Lua value carries taint: locals, globals, table keys and values, function closures.
  - New values take the taint of the execution path that creates them.
  - Reading a tainted value taints the execution path; reading a secure value from tainted
    execution gives a tainted copy (the original stays clean).
  - Writing a global from tainted execution taints that global, and through it every Blizzard
    code path that reads it afterwards.
  - Calling a tainted closure taints the current execution.
- Taint lasts until `/reload` or relog. When a protected function is reached on a tainted path it
  refuses to run and the game fires `ADDON_ACTION_BLOCKED` (or `ADDON_ACTION_FORBIDDEN` for actions
  that are always forbidden, such as movement or targeting) naming the AddOn last involved, which
  is not necessarily the culprit.
- The wiki's "honey" analogy: addon code is sticky, everything it touches gets sticky, and Blizzard
  code that touches it gets sticky too; a protected call with sticky hands errors.

How to avoid spreading taint:

- Do not overwrite or pre-hook Blizzard globals. Post-hook them with `hooksecurefunc([tbl,] name, fn)`:
  your function runs after the original, with a copy of its arguments, without tainting it.
- For widget scripts use `frame:HookScript(script, fn)` instead of `SetScript` on Blizzard frames.
- `securecall(fn, ...)` calls a function in a way that does not let taint escape into the caller.
- `issecure()` tells whether the current execution is secure; `issecurevariable([tbl,] name)` tells
  whether a variable is secure and which AddOn tainted it.

## Terminology

- **Secure**: without taint. "Clean" values mean the same.
- **Protected function**: can only be called successfully from secure execution (casting,
  targeting, moving, using items, ...). AddOns reach them only through secure templates.
- **Protected frame**: a frame locked down during combat. Created from secure templates (or made
  protected by Blizzard); once protected it cannot become unprotected.
- **Protected method**: a widget method that cannot be called on a protected frame from tainted
  execution during combat (`Show`, `Hide`, `SetPoint`, `SetAttribute`, ...). The wiki tags these
  `#secureframe`.
- **Secure template**: an XML template whose script handlers are secure; usually it also makes the
  frame protected.

## Restriction tags

Functions and methods in this file carry the wiki's restriction tags in their doc comments:

| Tag | Meaning |
|---|---|
| `#protected` | Can only be called from secure code. |
| `#hwevent` | Requires a hardware event, i.e. keyboard or mouse input; it fails from timers and events. |
| `#nocombat` | Cannot be called while in combat. |
| `#noinstance` | Only works outdoors, not in dungeons, raids, battlegrounds or arenas. |
| `#noscript` | Cannot be called directly from `/run`, `/script`, `RunScript` or `loadstring` (WowLua, WeakAuras). |
| `#grouponly` | Can only be queried on units in your party or raid. |
| `#secureframe` | Cannot be called on secure (protected) frames during combat; see SecureStateDriver. |
| `#restrictedframe` | Cannot be called on restricted frames, e.g. nameplates (anchor restricted regions). |
| `#anchorfamily` | Frames anchored to a restricted frame may only anchor their other points within that anchor family. |
| `#nopermission` | Fails with "You do not have permission to perform that function". |
| `#nofreetrial` | Not available to Free Trial / non-subscriber accounts. |

Blizzard's own API documentation (per client, so these differ between Era and Forever) adds:

| Blizzard flag | Meaning |
|---|---|
| `IsProtectedFunction` | The function is protected (secure code only). |
| `HasRestrictions` | The function has extra restrictions (combat, chat lockdown, ...); see its wiki page. |
| `RestrictedForMacroChatMessages` | Chat cannot be sent on externally observable chat types from macros. |
| `SecureHooksAllowed` | Can be post-hooked securely. Listed for information, not a restriction. |
| `SecretReturns`, `SecretWhen...`, `SecretIn...` | May return secret values (see Secret values). |
| `SecretArguments` | Whether secret values may be passed in: `AllowedWhenTainted`, `AllowedWhenUntainted`, `NotAllowed`. |
| `ChecksForbiddenAspects` | Refuses to work on objects with certain forbidden aspects. |

## Combat lockdown

- `InCombatLockdown()` is true while protected frames are locked (between `PLAYER_REGEN_DISABLED`
  and `PLAYER_REGEN_ENABLED`). Check it before creating secure frames or changing their attributes,
  points, size, parent or visibility.
- Changes you could not make in combat must be queued and applied on `PLAYER_REGEN_ENABLED`.
- Lockdown spreads: restrictions on a protected frame also apply to its parents and to frames it is
  anchored to, until re-parented or re-anchored out of combat. Anchoring a protected frame to a
  normal frame can unexpectedly lock that frame.

## Secure templates and handlers

- **SecureTemplates** (FrameXML `SecureTemplates.xml`) let addons trigger protected actions through
  attributes set out of combat:
  - `SecureActionButtonTemplate` (Button): performs the action described by its attributes, chosen
    by the modified `type` attribute (`type`, `type1`, `shift-type2`, `*type1`, ...): `action`,
    `actionbar`, `spell`, `item`, `macro`, `pet`, `target`, `focus`, `assist`, `cancelaura`,
    `stop`, `attribute`, `click`, ... with attributes such as `unit`, `spell`, `item`, `macrotext`.
    `InsecureActionButtonTemplate` (7.2.0+) is the unprotected variant for out-of-combat use.
  - `SecureUnitButtonTemplate` (Button): unit frames (left click targets, right click menu), with
    `RegisterUnitWatch(frame [, asState])` to show the frame only while its `unit` exists.
  - `SecureGroupHeaderTemplate`, `SecurePartyHeaderTemplate`, `SecureRaidGroupHeaderTemplate`,
    `SecureGroupPetHeaderTemplate`, `SecurePartyPetHeaderTemplate`, `SecureRaidPetHeaderTemplate`,
    `SecureAuraHeaderTemplate` (Frame): headers that create and lay out child frames securely.
- **SecureHandlers** (`SecureHandlerBaseTemplate` and `SecureHandler<Event>Template`) run code
  *snippets* (strings) in the restricted environment when something happens: `_onstate-<name>`,
  `_onattributechanged`, `_onclick`, `_ondoubleclick`, `_ondragstart`/`_onreceivedrag`,
  `_onmouseup`/`_onmousedown`, `_onmousewheel`, `_onenter`/`_onleave`, `_onshow`/`_onhide`.
  The base template adds `frame:Execute(body)`, `frame:WrapScript(frame, script, pre [, post])`,
  `frame:UnwrapScript(frame, script)` and `frame:SetFrameRef(id, frame)`.
- **SecureStateDriver**: `RegisterAttributeDriver(frame, attribute, conditional)` evaluates a macro
  conditional on every state change and securely sets the attribute; `"state-visibility"` shows and
  hides the frame. `RegisterStateDriver(frame, state, conditional)` is the older form (prefixes
  `state-`). `RegisterUnitWatch` / `UnregisterUnitWatch` do the same for unit existence.

## Restricted environment

Snippets run with only a small API. Available, per the wiki:

- `SecureCmdOptionParse`, `GetShapeshiftForm`, `IsStealthed`, `UnitExists`, `UnitIsDead`,
  `UnitIsGhost`, `UnitPlayerOrPetInParty`, `UnitPlayerOrPetInRaid`, the `Is*KeyDown` modifier
  functions, `IsModifiedClick`, `GetMouseButtonClicked`, `GetActionBarPage`, `GetBonusBarOffset`,
  `IsMounted`, `IsSwimming`, `IsSubmerged`, `IsFlying`, `IsFlyableArea`, `IsIndoors`, `IsOutdoors`,
  `GetBindingKey`, `HasAction`, `IsHarmfulSpell`, `IsHarmfulItem`, `IsHelpfulSpell`, `IsHelpfulItem`,
  `PlayerCanAttack`, `PlayerCanAssist`, `PlayerIsChanneling`, `PlayerPetSummary`, `PlayerInCombat`,
  `PlayerInGroup`, `UnitHasVehicleUI`, `RegisterStateDriver`, `GetActionInfo`, and the vehicle and
  override bar queries (`HasVehicleActionBar`, `HasOverrideActionBar`, `GetVehicleBarIndex`, ...).
- `math` and `string` in full, plus `select`, `tonumber`, `tostring`, `print`, `format`, `strsplit`,
  `strjoin`, `strtrim`, ... Tables are *restricted tables*: use `newtable`, `pairs`, `ipairs`,
  `next`, `unpack`, `wipe`, `tinsert`, `tremove`, `rtgsub` and the `rtable.*` / restricted-aware
  `table.*` functions. `table.sort` cannot take a comparison function.
- Frames are only reachable as *handles*: `self`, `owner`, and handles from
  `handle:GetFrameRef(name)` (set from insecure code with `frame:SetFrameRef`). Handles support
  getters (`GetName`, `IsShown`, `GetAttribute`, `GetRect`, `GetChildren`, ...) and, for protected
  frames, setters (`Show`, `Hide`, `SetAttribute`, `SetPoint`, ...). Only `GetName`,
  `GetObjectType`, `IsObjectType` and `IsProtected` work on handles to non-protected frames.

## Object security

- **Protected regions** (2.0.1): positioning, size, visibility and secure attributes cannot be
  changed by insecure code in combat. Action buttons and unit frames are the common case.
  `region:IsProtected()` tells whether a region will be protected in combat.
- **Forbidden objects** (5.4.0): insecure code may call almost no methods on them, ever, except
  `GetAttribute`/`SetAttribute`. They are skipped by `EnumerateFrames` and `C_System.GetFrameStack`.
  Test with `object:IsForbidden()`.
- **Anchor restricted regions** (8.2.0), e.g. nameplates and chat bubbles: insecure code cannot read
  their position (`GetRect`, `GetPoint`, ...), and `SetPoint` fails with a forbidden-action error
  when the resulting anchors would bridge two anchor families (typically: anchoring to both the
  screen and `UIParent`; `ClearAllPoints` first). Test with `region:IsAnchoringRestricted()`.
- **Inaccessible objects** (10.1.0, private auras): no reference can be obtained through methods;
  `GetDebugName` returns `"$parent.inaccessible"`, `GetParentKey` returns nil, and `GetChildren` /
  `GetRegions` never return them.

## Secret values (Forever)

Introduced with retail 12.0.0 and part of Forever, which belongs to the mainline family. **Era does
not have secret values in this way**: its API documentation marks no secret returns, predicates or
aspects (only a few `Requires...` preconditions). Everything in this section is about Forever; items
below that may return secrets say `(Forever only)` on their `Blizzard:` line.

- Some combat APIs return *secret values* to tainted code (e.g. `UnitHealth`, `UnitName` on
  non-player units in combat). Tainted code may store them, pass them to functions and concatenate
  string/number secrets, but any arithmetic, comparison, boolean test on boolean secrets, `#`,
  indexing, use as a table key or calling them raises an immediate Lua error. `type()` still works.
- Only APIs marked to accept secrets take them from tainted code (`SecretArguments`), e.g.
  `StatusBar:SetValue`, `FontString:SetText`. Passing a secret to a widget can mark the widget with
  a *secret aspect* (or as having secret values), after which its getters return secrets too;
  anchoring secrecy propagates to regions anchored to it. `SetToDefaults()` clears aspects;
  clearing anchors resets anchoring secrecy.
- Tables can be secret (indexing yields secrets) or forbidden ("attempted to index a forbidden
  table").
- Test with `issecretvalue`, `canaccessvalue`, `issecrettable`, `canaccesstable`,
  `object:HasSecretAspect(aspect)`, `object:HasSecretValues()`, `region:IsAnchoringSecret()`.
  `C_RestrictedActions` reports which addon restriction states are active; `C_Secrets` evaluates
  the secret predicates. Curve, ColorCurve and Duration objects let addons display secret values.
- For testing, the CVars `addonCombatRestrictionsForced`, `addonEncounterRestrictionsForced`,
  `addonChatRestrictionsForced`, `addonMapRestrictionsForced`, `addonPvPMatchRestrictionsForced`
  and `addonChallengeModeRestrictionsForced` simulate the restrictions (not saved across restarts).

## Practical checklist

1. Never call a `#protected` function from addon code; use a secure template with attributes.
2. Do anything to protected frames (create, `SetAttribute`, `SetPoint`, `Show`/`Hide`, re-parent)
   only when `InCombatLockdown()` is false; queue it for `PLAYER_REGEN_ENABLED` otherwise.
3. Call `#hwevent` functions only from a click or key handler, never from `OnUpdate`, timers or events.
4. Post-hook Blizzard code with `hooksecurefunc` / `HookScript`; never replace Blizzard globals or
   methods, and never write to globals Blizzard reads.
5. Do not anchor your frames to nameplates or other restricted frames from two anchor families.
6. On Forever, guard combat data that may be secret with `issecretvalue` before doing math or
   comparisons on it, and feed secrets straight into widgets that accept them.
7. When something breaks in combat, read the `ADDON_ACTION_BLOCKED` message and use
   `issecurevariable` to find out which addon tainted the variable involved.
