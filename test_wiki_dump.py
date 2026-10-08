"""Parsing rules of wiki_dump.py, checked against real warcraft.wiki.gg snippets.

Run: uv run --with pytest --with requests pytest test_wiki_dump.py
"""

import pytest

from wiki_dump import (
  api_name,
  api_template_targets,
  clean,
  is_api_shaped,
  listing_entry,
  page_kind,
  parse_lua_module,
  relation,
  template_calls,
)

CLASSES = {"Frame", "Region", "ScriptRegion", "ScriptRegionResizing", "GameTooltip"}


@pytest.mark.parametrize(
  ("title", "kind", "expected"),
  [
    ("API:C AccountInfo.GetIDFromBattleNetAccountGUID", "function", "C_AccountInfo.GetIDFromBattleNetAccountGUID"),
    ("API:ScriptRegionResizing ClearAllPoints", "widget-method", "ScriptRegionResizing:ClearAllPoints"),
    ("API Region ClearAllPoints", "redirect", "Region:ClearAllPoints"),
    ("API EJ GetCurrentInstance", "redirect", "EJ_GetCurrentInstance"),  # EJ is not a class
    ("API ChatFrame AddChannel", "removed-function", "ChatFrame_AddChannel"),
    ("API Vector2DMixin RotateDirection", "framexml-function", "Vector2DMixin:RotateDirection"),
    ("API FramerateFrame:Toggle()", "framexml-function", "FramerateFrame:Toggle"),
    ("Event:ACCOUNT CVARS LOADED", "event", "ACCOUNT_CVARS_LOADED"),
    ("SOULBIND CONDUITS RESET", "redirect", "SOULBIND_CONDUITS_RESET"),
    ("CVar checkAddonVersion", "cvar", "checkAddonVersion"),
    ("MACRO targetraid", "macro", "/targetraid"),
    ("Structure BidInfo", "type", "Structure BidInfo"),
  ],
)
def test_api_name(title, kind, expected):
  assert api_name(title, kind, CLASSES) == expected


@pytest.mark.parametrize(
  ("name", "target", "expected"),
  [
    ("AbandonSkill", "AbandonSkill", "same-name"),
    ("Getpoint", "ScriptRegionResizing:GetPoint", "unqualified"),
    ("Frame:EnableMouse", "ScriptRegion:EnableMouse", "moved"),
    ("GetUnitName", "UnitName", "renamed"),
  ],
)
def test_relation(name, target, expected):
  assert relation(name, target) == expected


def test_clean_keeps_parentheses_and_splits_fragment():
  assert clean("API_FramerateFrame:Toggle()") == ("API FramerateFrame:Toggle()", "")
  assert clean(":API:UnitAura#FindAuraByName") == ("API:UnitAura", "FindAuraByName")


def test_template_calls_handles_nesting_and_escaped_equals():
  text = "{{apisig|data {{=}} AbbreviateConfig:GetAbbreviateNumberData()}} {{wowapi|t=a|note=see {{api|Foo}}}}"
  assert template_calls(text, "apisig") == [{"1": "data = AbbreviateConfig:GetAbbreviateNumberData()"}]
  assert template_calls(text, "wowapi") == [{"t": "a", "note": "see {{api|Foo}}"}]
  assert template_calls("{{restrictedapi|protected,hwevent|note=x}}", "restrictedapi") == [
    {"1": "protected,hwevent", "note": "x"}
  ]


def test_page_kind_ignores_templates_in_comments():
  text = "{{wowapi|t=a}}\n<!-- or {{wowapievent}}, {{widgetmethod}} -->"
  assert page_kind("API:C Garrison.GetLandingPageShipmentInfo", 3000, text) == "function"
  assert page_kind("Template:Framexmlfunc", 10, "{{framexmlfunc}}") == "other"


@pytest.mark.parametrize(
  ("line", "expected"),
  [
    (
      ": {{apilink|t=w|ScriptRegionResizing:SetPoint|arg=point [, relativeTo]}} {{apitag|secureframe}} - Sets.",
      {"name": "ScriptRegionResizing:SetPoint", "type": "w", "args": "point [, relativeTo]"},
    ),
    (
      ": {{apilink|t=a|framexml=TooltipUtil.DebugCopyGameTooltip}}",
      {"name": "TooltipUtil.DebugCopyGameTooltip", "type": "a"},
    ),
    (
      ": {{apilink.lua|string.format|arg=formatstring, ...}}",
      {"name": "string.format", "type": "", "args": "formatstring, ..."},
    ),
    (": {{api|t=e|CRITERIA_EARNED}}<small>: achievementID</small>", {"name": "CRITERIA_EARNED", "type": "e"}),
    (": [[API:EJ_GetInstanceForMap|EJ_GetInstanceForMap]](mapID)", {"name": "EJ_GetInstanceForMap"}),
  ],
)
def test_listing_entry(line, expected):
  assert listing_entry(line, CLASSES) == expected


def test_api_template_targets_follow_module_api_link():
  text = "{{api|Frame:Show}} {{api|GetTime()}} {{api|t=e|ADDON_LOADED}} {{api|t=o|Region}} {{api|t=c|nameplateShowAll}}"
  assert list(api_template_targets(text)) == [
    "API:Frame Show", "API:GetTime", "Event:ADDON LOADED", "UIOBJECT Region", "CVar nameplateShowAll",
  ]


@pytest.mark.parametrize(
  ("title", "expected"),
  [
    ("RegisterUnitWatch", True),
    ("SPELL AURA APPLIED", True),
    ("API Foo", True),
    ("HOWTO: Use OnUpdate Correctly", False),
  ],
)
def test_is_api_shaped(title, expected):
  assert is_api_shaped(title) is expected


def test_parse_lua_module_applies_merge_and_return():
  src = 'local data = {\n\t["A"] = {"1.0.0", "9.0.1"},\n}\nlocal lua = {\n\t["math.clamp"] = {"12.1.5"},\n}\n'
  src += "\nfor k, v in pairs(lua) do\n\tdata[k] = v\nend\n\nreturn data"
  assert parse_lua_module(src) == {"A": ["1.0.0", "9.0.1"], "math.clamp": ["12.1.5"]}


def test_parse_lua_module_reads_literals_without_executing():
  src = 'local data = {\n\t["X"] = 0x1C, -- c\n\tf = { b = true, "s" },\n\tcall = mw.loadData("M"),\n}\nreturn data'
  assert parse_lua_module(src) == {"X": 28, "f": {"b": True, "1": "s"}, "call": {"$expr": 'mw.loadData("M")'}}
