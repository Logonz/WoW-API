"""Wiki parsing and client-loading rules of generate.py, on real warcraft.wiki.gg / Blizzard snippets.

Run: uv run --with pytest --with requests pytest test_generate.py
"""

from generate import (
  SigArg,
  Transcluder,
  clean_type,
  definitions,
  evaluate,
  flag_note,
  flavor_tag,
  per_client,
  restricted_on,
  security_section,
  sig_params,
  signature_args,
  split_signature,
  toc_files,
  type_names,
  widget_restricted,
)


def test_split_signature_marks_optional_arguments():
  calls, returns = split_signature("name, icon, count, ... = UnitAura(unit, index [, filter])")
  assert calls == [("UnitAura", [SigArg(["unit"]), SigArg(["index"]), SigArg(["filter"], optional=True)])]
  assert returns == ["name", "icon", "count", "..."]


def test_split_signature_reads_every_call_form_sharing_the_returns():
  sig = "name, subtext, icon\n  = GetSpellInfo(spell)\n  = GetSpellInfo(index, bookType)"
  calls, returns = split_signature(sig)
  assert [(name, [a.names[0] for a in args]) for name, args in calls] == [
    ("GetSpellInfo", ["spell"]),
    ("GetSpellInfo", ["index", "bookType"]),
  ]
  assert returns == ["name", "subtext", "icon"]


def optional_flags(args: str) -> list[bool]:
  return [a.optional for a in signature_args(args)]


def test_signature_args_optional_notations():
  setpoint = "point [, relativeTo [, relativePoint]] [, offsetX, offsetY]"
  assert optional_flags(setpoint) == [False, True, True, True, True]
  assert optional_flags("relativePoint [, relativeTo] [, offsetX, offsetY]") == [False, True, True, True]
  assert optional_flags("[name [, templateName]]") == [True, True]
  assert optional_flags("slotIndex, onOff{, exclusive}") == [False, False, True]
  assert optional_flags("recipeID, craftingReagents, recraftItemGUID?") == [False, False, True]
  assert optional_flags("name, [shortName], description") == [False, True, False]
  assert optional_flags("index [, returnTable") == [False, True]  # unclosed on the wiki
  assert optional_flags("low,] high]") == [False, False]  # unbalanced on the wiki


def test_signature_args_alternatives_varargs_and_omittable_leading_args():
  assert signature_args("itemId or itemName or itemLink[, slot]") == [
    SigArg(["itemId", "itemName", "itemLink"]),
    SigArg(["slot"], optional=True),
  ]
  assert signature_args('"spellName" or spellId, bookType')[0].names == ["spellName", "spellId"]
  assert signature_args("attributeName [, ...arguments]")[1] == SigArg(["arguments"], optional=True, vararg=True)
  assert signature_args("[tbl,] functionName, hookfunc")[0] == SigArg(["tbl"], optional=True, omittable=True)


def test_sig_params_types_alternatives_and_leaves_omittable_args_required():
  info = {"itemId": ("number", False, "Item ID"), "itemLink": ("string", False, ""), "...": ("string", False, "")}
  params, omittable = sig_params(signature_args("[tbl,] itemId or itemLink, ..."), info)
  assert [(p.name, p.type, p.optional) for p in params] == [
    ("tbl", "any", False),
    ("itemId", "number|string", False),
    ("...", "string", False),
  ]
  assert omittable == [True, False, False]


def test_clean_type():
  assert clean_type("AuraFilters?") == ("AuraFilters", True)
  assert clean_type("number,string") == ("number|string", False)
  assert clean_type("CraftingReagentInfo[]?") == ("CraftingReagentInfo[]", True)
  assert clean_type("Boolean") == ("boolean", False)


def test_definitions_reads_apitype_union_default_and_old_style():
  text = (
    "==Arguments==\n"
    ":;spell:{{apitype|number|string}} - Spell ID or Name.\n"
    ":;filter:{{apitype|AuraFilters|default=HELPFUL}}\n"
    ";buttonID : Number - The button ID\n"
    ";rank : String (Optional) - rank of the buff\n"
    ":;isInspect:{{apitype|boolean}} - Optional, for the inspect target if true\n"
    "==Returns==\n"
  )
  assert definitions(text, ("Arguments",))[""] == {
    "spell": ("number|string", False, "Spell ID or Name."),
    "filter": ("AuraFilters", True, ""),
    "buttonID": ("number", False, "The button ID"),
    "rank": ("string", True, "rank of the buff"),
    "isInspect": ("boolean", True, "Optional, for the inspect target if true"),
  }


def test_definitions_reads_span_types_and_numbered_names():
  text = (
    "==Returns==\n"
    ':;1. name : <span class="apitype">string</span> - The localized name.\n'
    ':;4. dispelType : <span title="nilable"><span class="apitype">string</span>?</span> - Magic type.\n'
  )
  assert definitions(text, ("Returns",))[""] == {
    "name": ("string", False, "The localized name."),
    "dispelType": ("string", True, "Magic type."),
  }


def test_definitions_split_by_function_subsections():
  text = (
    "==Arguments==\n===BNGetFriendInfo===\n:;index:{{apitype|number}}\n"
    "===BNGetFriendInfoByID===\n:;id:{{apitype|number}}\n"
  )
  defs = definitions(text, ("Arguments",))
  assert set(defs["BNGetFriendInfo"]) == {"index"} and set(defs["BNGetFriendInfoByID"]) == {"id"}


def test_evaluate_fills_params_and_if():
  body = ":;{{#if:{{{onlyname|}}}|spellName:{{apitype|string}}|spell:{{apitype|number,string}}}} - The {{{1|aura}}}."
  assert evaluate(body, {}) == ":;spell:{{apitype|number,string}} - The aura."
  assert evaluate(body, {"onlyname": "1", "1": "debuff"}) == ":;spellName:{{apitype|string}} - The debuff."


def test_transcluder_expands_pages_and_definition_templates_only():
  t = Transcluder.__new__(Transcluder)
  t.files = {}
  t.bodies = {
    "SpellArg": ":;spell:{{apitype|number}}",
    "Template:AuraType": ':;1. name : <span class="apitype">string</span> - The {{{1|aura}}}.',
    "Template:Apitype": "{{#invoke:Apitype|main}}",
  }
  text = "==Arguments==\n{{:SpellArg}}\n==Returns==\n{{AuraType|buff}}\n{{apitype|number}}"
  assert t.expand(text) == (
    "==Arguments==\n:;spell:{{apitype|number}}\n==Returns==\n"
    ':;1. name : <span class="apitype">string</span> - The buff.\n{{apitype|number}}'
  )


def test_toc_files_honours_game_type_gates(tmp_path):
  (tmp_path / "Blizzard_Deprecated.toc").write_text(
    "## Title: Blizzard_Deprecated\n"
    "Classic/Deprecated_1_15_8.lua [AllowLoadGameType classic]\n"
    "Mainline/Deprecated_12_0_1.lua [AllowLoadGameType mainline]\n"
    "Shared/Deprecated_12_1_0.lua\n"
    "Deprecated_Specialization_[Game].lua\n"
    "[Family]\\Deprecated_UnitScriptOverrides.lua [AllowLoadGameType classic]\n"
  )
  era_files = toc_files(tmp_path, {"vanilla", "classic"}, {"Game": "Vanilla", "Family": "Classic"})
  forever_files = toc_files(tmp_path, {"camelot", "mainline"}, {"Game": "Camelot", "Family": "Mainline"})
  assert [p.relative_to(tmp_path).as_posix() for p in era_files] == [
    "Classic/Deprecated_1_15_8.lua",
    "Shared/Deprecated_12_1_0.lua",
    "Deprecated_Specialization_Vanilla.lua",
    "Classic/Deprecated_UnitScriptOverrides.lua",
  ]
  assert [p.relative_to(tmp_path).as_posix() for p in forever_files] == [
    "Mainline/Deprecated_12_0_1.lua",
    "Shared/Deprecated_12_1_0.lua",
    "Deprecated_Specialization_Camelot.lua",
  ]


def test_toc_files_honours_exclude_gates(tmp_path):
  (tmp_path / "Blizzard_Collections.toc").write_text(
    "[Family]\\Blizzard_ToyBoxProgressTracker.lua [AllowLoadGameType mainline] [ExcludeLoadGameType camelot]\n"
    "[Game]\\Blizzard_CollectionsConstants.lua [AllowLoadGameType camelot]\n"
  )
  forever = toc_files(tmp_path, {"camelot", "mainline"}, {"Game": "Camelot", "Family": "Mainline"})
  assert [p.relative_to(tmp_path).as_posix() for p in forever] == ["Camelot/Blizzard_CollectionsConstants.lua"]


def test_per_client_notes_other_values_and_missing_clients():
  assert per_client({"era": -2, "forever": -1}, 2) == (-2, "Forever: -1")
  assert per_client({"forever": 3}, 2) == (3, "**Forever only**")
  assert per_client({"era": True, "forever": True}, 2) == (True, "")


def test_type_names_reads_the_type_part_of_each_tag():
  assert type_names("param unit", "UnitToken|nil The unit to query") == {"UnitToken", "nil"}
  assert type_names("return", "string? name # localized") == {"string"}
  assert type_names(
    "overload", "fun(unit: UnitToken): string, fileID, number, UnitCastBarID?, number"
  ) == {"UnitToken", "string", "fileID", "number", "UnitCastBarID"}
  assert type_names("field __newindex", "table|fun(t,k,v)|nil") == {"table", "nil"}
  assert type_names("param mode", '"HELPFUL"|"HARMFUL"') == set()
  assert type_names("class Region", ": ScriptRegion, AnimatableObject") == {"ScriptRegion", "AnimatableObject"}
  assert type_names(
    "param isEnabled", "boolean|fun(elementDescription: ElementMenuDescriptionProxy): boolean Whether it is"
  ) == {"boolean", "ElementMenuDescriptionProxy"}


def test_security_section_first_match_wins():
  assert security_section("hooksecurefunc", set(), set()) == "tools"
  assert security_section("CastSpellByName", {"protected", "hwevent"}, set()) == "protected"
  assert security_section("C_Item.UseItem", set(), {"IsProtectedFunction"}) == "protected"
  assert security_section("JumpOrAscendStart", {"hwevent"}, set()) == "hwevent"
  assert security_section("SetCVar", {"nocombat"}, set()) == "restricted"
  assert security_section("SendChatMessage", set(), {"RestrictedForMacroChatMessages"}) == "restricted"
  assert security_section("UnitName", set(), {"SecretWhenUnitNameIdentityRestricted"}) == "secret"
  assert security_section("GetTime", set(), {"SecureHooksAllowed"}) is None


def test_restricted_on_uses_the_clients_whose_docs_set_the_flag():
  both = {"era", "forever"}
  assert restricted_on("secret", set(), {"SecretWhenUnitIdentityRestricted": {"forever"}}, both) == {"forever"}
  assert restricted_on("protected", {"protected"}, {}, both) == both
  assert restricted_on("restricted", set(), {"HasRestrictions": {"forever"}}, both) == {"forever"}
  assert restricted_on("widget", {"secureframe"}, {"IsProtectedFunction": {"era"}}, both) == both


def test_widget_restricted_and_flag_note():
  assert widget_restricted({"secureframe"}, set())
  assert widget_restricted(set(), {"IsProtectedFunction"})
  assert not widget_restricted(set(), {"SecureHooksAllowed"})
  assert flag_note({"IsProtectedFunction": {"era", "forever"}, "HasRestrictions": {"forever"}}, 2) == (
    "Blizzard: HasRestrictions (Forever only), IsProtectedFunction"
  )


def test_flavor_tag_only_when_one_client_has_it():
  assert flavor_tag({"era"}) == "**Era only**"
  assert flavor_tag({"era", "forever"}) == ""
