"""Wikitext-to-markdown conversion in reference.py, on snippets taken from warcraft.wiki.gg pages.

Run: uv run --with pytest --with requests pytest test_reference.py
"""

from reference import Entry, entry_path, front_matter, scan_usage, usage_section, wiki_to_markdown


def test_headings_lists_and_definition_lists():
  text = "==Arguments==\n:;unit:{{apitype|UnitToken}}\n* first\n** nested\n# numbered\n===Sub==="
  assert wiki_to_markdown(text) == (
    "## Arguments\n\n- **unit**: `UnitToken`\n- first\n  - nested\n1. numbered\n\n### Sub"
  )


def test_code_blocks_inline_code_and_preformatted_lines():
  text = (
    'Separated by <syntaxhighlight lang=lua inline>"|"</syntaxhighlight> pipes, e.g. <code>HARMFUL|PLAYER</code>.\n'
    '<syntaxhighlight lang="lua">\nprint(UnitAura("target", 3))\n</syntaxhighlight>\n'
    " RegisterUnitWatch(frame, asState)\n UnregisterUnitWatch(frame, asState)\nAfter."
  )
  assert wiki_to_markdown(text) == (
    'Separated by `"|"` pipes, e.g. `HARMFUL|PLAYER`.\n\n'
    '```lua\nprint(UnitAura("target", 3))\n```\n\n'
    "```\nRegisterUnitWatch(frame, asState)\nUnregisterUnitWatch(frame, asState)\n```\nAfter."
  )


def test_tables_with_continuation_cells_and_a_nested_table():
  text = (
    '{| class="sortable darktable"\n! Constant !! Filter\n|-\n| <code>Helpful</code>\n|| {{apiname|HELPFUL}}\n'
    '|-\n| <code>Raid</code>\n||\n  {| class="zebra"\n  |-\n  | with HELPFUL || can apply\n  |}\n|}'
  )
  assert wiki_to_markdown(text) == (
    "| Constant | Filter |\n|---|---|\n| `Helpful` | `HELPFUL` |\n| `Raid` | with HELPFUL — can apply |"
  )


def test_templates_and_links():
  text = (
    "{{wowapi}} See {{api|GetTime}}() and [[API UnitName|UnitName]], [[Category:API functions]]"
    "[https://example.com docs].\n"
    "{{deprecatedapi|patch=10.2.5|removed=11.0.2}}\n"
    "* {{Patch 1.13.2|note=Added.}} {{Wow-inline}}\n"
    "{{restrictedapi|protected}}"
  )
  assert wiki_to_markdown(text) == (
    "See `GetTime`() and UnitName, [docs](https://example.com).\n\n"
    "> **Deprecated** in patch 10.2.5, removed in 11.0.2.\n\n"
    "- **Patch 1.13.2**: Added. (Classic)\n\n"
    "> **Restricted:** protected"
  )


def test_expanded_transclusions_lose_their_comments():
  def expand(text: str) -> str:
    return text.replace("{{AuraType|aura}}", "<!-- Template:AuraType\n-->:;1. name : string - The name.")

  returns = wiki_to_markdown("==Returns==\n{{AuraType|aura}}", expand)
  assert returns == "## Returns\n\n- **1. name**: string - The name."


def test_scan_usage_finds_calls_events_and_methods_but_not_declarations(tmp_path):
  addons = tmp_path / "Interface/AddOns"
  (addons / "Blizzard_Auras").mkdir(parents=True)
  (addons / "Blizzard_APIDocumentationGenerated").mkdir()
  (addons / "Blizzard_Auras/Auras.lua").write_text(
    'local name = UnitAura("player", 1)\nframe:RegisterEvent("UNIT_AURA")\n'
    "frame:SetPoint(\"CENTER\")\nlocal info = C_Item.GetItemInfo(id)\nlocal x = self.UnitAura\n"
  )
  (addons / "Blizzard_APIDocumentationGenerated/UnitAuraDocumentation.lua").write_text("local UnitAura = {}\n")
  usage = scan_usage(tmp_path, "forever @ test", {"UnitAura", "UNIT_AURA", "C_Item.GetItemInfo"}, {"SetPoint"})
  auras = "Interface/AddOns/Blizzard_Auras/Auras.lua"
  assert usage.names == {
    "UnitAura": {auras: [1, 1]},
    "UNIT_AURA": {auras: [1, 2]},
    "C_Item.GetItemInfo": {auras: [1, 4]},
  }
  assert usage.methods == {"SetPoint": {auras: [1, 3]}}

  section, files = usage_section(Entry("UnitAura", "function", ["Era"], "", "API/Global.lua"), usage, 50)
  assert files == 1
  assert section.endswith(f"1 file uses `UnitAura`:\n\n- wow-ui-source/{auras}:1 (1 use)")


def test_entry_paths_and_front_matter():
  method = Entry(
    "ScriptRegion:SetPoint", "method", ["Era", "Forever"], "", "Security/Security.lua", tags=["secureframe"]
  )
  function = Entry("C_Item.GetItemInfo", "function", ["Era"], "", "API/Item.lua")
  assert entry_path(method) == "methods/ScriptRegion/SetPoint.md"
  assert entry_path(function) == "functions/C_Item.GetItemInfo.md"
  assert front_matter(method) == (
    '---\nname: "ScriptRegion:SetPoint"\nkind: "method"\nclients: ["Era", "Forever"]\n'
    'library: "Security/Security.lua"\nrestrictions: ["secureframe"]\n---'
  )
