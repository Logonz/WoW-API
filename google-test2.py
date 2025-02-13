import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import re
import requests
import shutil
from WikiGetData import GetData
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

load_dotenv()

# Only run this block for Gemini Developer API
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with open("LuaTypes.md", "r") as f:  # changed variable from os to f
  LuaTypesContent = f.read()

model = "gemini-2.0-flash-lite-preview-02-05"
# model = "gemini-2.0-flash"

system_prompt = f"""You are an expert at writing Lua Language Server compatible Type hints:

## Documentation about Lua Types

<lua_types>
{LuaTypesContent}
</lua_types>

<banned_lua_language_keywords>
<keywords>
and       break     do        else      elseif
end       false     for       function  if
in        local     nil       not       or
repeat    return    then      true      until     while
</keywords>
Explanation: These keywords are banned and cannot be used as parameters.
</banned_lua_language_keywords>

Always have the function be one line, this is part of a file that are ---@meta definitions and do not contain the function body.

# Steps to follow:

1. You will get RAW HTML content your job is to convert it to Lua Type hints.
2. Never include the 'API_' prefix in the function name.
4. Always include all the parameters and return types. Omit if no parameters or return types.
5. If the type is not known, use 'unknown'.
6. Write a summary of the function in the first line. Using <br> to separate lines, like in the examples.
7. If there are additional details about the function, focus only on the the most important parts and keep it SHORT.

# Typing rules:

- The type float is not used in Lua, use number instead.
- Always use lowercase for primitives. The primitive types are: number, string, boolean, table, function, userdata, thread, and nil.
- If a parameter is optional, use the nilable type by adding a '?' after the type. Example: number?
- When there are multiple returns as vararg (a, b, ...), use ... as name and add "a, b, ..." to the description to denote the multiple returns
- Do not add the [ ] to the param_name. The [ ] is used to denote optional parameters. The nilable type is denoted by adding a '?' after the type.

# Function Signature:

- Multiple variants of a function should be added separately. Example: GetItemInfo(itemID) and GetItemInfo(itemName) should be added as two separate functions.
- Always have valid Lua syntax in the function signature i.e, 'AddQuestWatch(questIndex [, watchTime])' is not valid Lua syntax, it should be 'AddQuestWatch(questIndex, watchTime)'.


# Examples of Tool Outputs in Python Objects:

## Example 1:

### Input (Partial example):

<div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
[...]
<p>Returns the hyperlink for a spell.
</p>
<pre>link, spellId = GetSpellLink(spell]
              = GetSpellLink(index, bookType)
</pre>
[...]
<dd><dl><dt>spell</dt>
  <dd><font color="#ecbc2a">number</font>|<font color="#ecbc2a">string</font> - Spell ID or Name. When passing a name requires the spell to be in your <a href="/wiki/Spellbook" title="Spellbook">Spellbook</a>.</dd></dl></dd>
[...]
<dd><dl><dt>link</dt>
<dd><font color="#ecbc2a">string</font>&nbsp;: <a href="/wiki/Hyperlinks#spell" title="Hyperlinks">spellLink</a></dd>
<dt>spellID</dt>
<dd><font color="#ecbc2a">number</font></dd></dl></dd>
[...]
</div>

### Output:

args={{'for_function_signature': 'GetSpellLink(spell)', "summary": 'Returns the hyperlink for a spell.'}} name='Add_summary'
args={{'for_function_signature': 'GetSpellLink(spell)',"param_description": 'Spell ID of a spell. When passing a name requires the spell to be in your Spellbook.', 'param_name': 'spell', 'param_type': 'number|string'}} name='Add_param'
args={{"for_function_signature": 'GetSpellLink(spell)', 'return_type': 'spellLink', 'return_description': '', 'return_name': 'link'}} name='Add_return'
args={{"for_function_signature": 'GetSpellLink(spell)', 'return_type': 'number', 'return_description': '', 'return_name': 'spellID'}} name='Add_return'
args={{"for_function_signature": 'GetSpellLink(index, bookType)', 'summary': 'Returns the hyperlink for a spell.'}} name='Add_summary'
args={{"for_function_signature": 'GetSpellLink(index, bookType)', 'param_description': 'Spellbook slot index, ranging from 1 through the total number of spells across all tabs and pages.', 'param_name': 'index', 'param_type': 'number'}} name='Add_param'
args={{"for_function_signature": 'GetSpellLink(index, bookType)', "param_description": 'BOOKTYPE_SPELL or BOOKTYPE_PET depending on if you wish to query the player or pet spellbook.', 'param_name': 'bookType', 'param_type': 'string'}} name='Add_param'
args={{"for_function_signature": 'GetSpellLink(index, bookType)', 'return_type': 'string', 'return_description': 'spellLink', "return_name": 'link'}} name='Add_return'
args={{"for_function_signature": 'GetSpellLink(index, bookType)', 'return_type': 'number', 'return_description': '', 'return_name': 'spellID'}} name='Add_return'

## Example 2:

### Input (Partial example):

<div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
[...]
<p>Returns true if a (pet) spell is autocastable. 
</p>
<pre>autocastable, autostate = GetSpellAutocast("spellName" or spellId, bookType)
</pre>
[...]
<dd><dl><dt>spellName</dt>
<dd><font color="#ecbc2a">string</font> - the name of the spell.</dd>
<dt>spellId</dt>
<dd><font color="#ecbc2a">number</font> - the offset (position) of spell in spellbook. SpellId can change when you learn new spells.</dd>
<dt>bookType</dt>
<dd><font color="#ecbc2a">string</font> - Either BOOKTYPE_SPELL ("spell") or BOOKTYPE_PET ("pet").</dd></dl></dd>
[...]
<dd><dl><dt>autocastable</dt>
<dd><font color="#ecbc2a">number</font> - whether a spell is autocastable.</dd>
<dd>Returns 1 if the spell is autocastable, nil otherwise.</dd>
<dt>autostate</dt>
<dd><font color="#ecbc2a">number</font> - whether a spell is currently set to autocast.</dd>
<dd>Returns 1 if the spell is currently set for autocast, nil otherwise.</dd></dl></dd>
[...]
</div>

### Output:

args={{'for_function_signature': 'GetSpellAutocast(spellName, bookType)', 'summary': 'Returns true if a (pet) spell is autocastable.'}} name='Add_summary'
args={{'for_function_signature': 'GetSpellAutocast(spellName, bookType)', 'param_description': 'The name of the spell.', 'param_name': 'spellName', 'param_type': 'string'}} name='Add_param'
args={{'for_function_signature': 'GetSpellAutocast(spellName, bookType)', 'param_description': 'Either BOOKTYPE_SPELL ("spell") or BOOKTYPE_PET ("pet").', 'param_name': 'bookType', 'param_type': 'string'}} name='Add_param'
args={{'for_function_signature': 'GetSpellAutocast(spellName, bookType)', 'return_description': 'whether a spell is autocastable.', 'return_name': 'autocastable', 'return_type': 'number?'}} name='Add_return'
args={{'for_function_signature': 'GetSpellAutocast(spellName, bookType)', 'return_description': 'whether a spell is currently set to autocast.', 'return_name': 'autostate', 'return_type': 'number?'}} name='Add_return'
args={{'for_function_signature': 'GetSpellAutocast(spellId, bookType)', 'summary': 'Returns true if a (pet) spell is autocastable.'}} name='Add_summary'
args={{'for_function_signature': 'GetSpellAutocast(spellId, bookType)', 'param_description': 'The offset (position) of spell in spellbook. SpellId can change when you learn new spells.', 'param_name': 'spellId', 'param_type': 'number'}} name='Add_param'
args={{'for_function_signature': 'GetSpellAutocast(spellId, bookType)', 'param_description': 'Either BOOKTYPE_SPELL ("spell") or BOOKTYPE_PET ("pet").', 'param_name': 'bookType', 'param_type': 'string'}} name='Add_param'
args={{'for_function_signature': 'GetSpellAutocast(spellId, bookType)', 'return_description': 'whether a spell is autocastable.', 'return_name': 'autocastable', 'return_type': 'number?'}} name='Add_return'
args={{'for_function_signature': 'GetSpellAutocast(spellId, bookType)', 'return_description': 'whether a spell is currently set to autocast.', 'return_name': 'autostate', 'return_type': 'number?'}} name='Add_return'

## Example 3:

### Input (Partial example):
<div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
[...]
<p>Returns information about a loss-of-control cooldown affecting a spell.
</p>
<pre>start, duration = GetSpellLossOfControlCooldown(spellSlot[, bookType] or spellName or spellID)
</pre>
[...]
<dl><dd><dl><dt>spellSlot</dt>
<dd><font color="#ecbc2a">number</font> - spell book slot index, ascending from 1.</dd>
<dt>bookType</dt>
<dd><font color="#ecbc2a">string</font> - spell book type token, e.g. "spell" from player's spell book.</dd></dl></dd></dl>
<p>or
</p>
<dl><dd><dl><dt>spellName</dt>
<dd><font color="#ecbc2a">string</font> - name of a spell in the player's spell book.</dd></dl></dd></dl>
<p>or
</p>
<dl><dd><dl><dt>spellID</dt>
<dd><font color="#ecbc2a">number</font> - spell ID of a spell accessible to the player.</dd></dl></dd></dl>
[...]
<dd><dl><dt>start</dt>
<dd><font color="#ecbc2a">number</font> - time at which the loss-of-control cooldown began, per <a href="/wiki/API_GetTime" title="API GetTime">GetTime</a>.</dd>
<dt>duration</dt>
<dd><font color="#ecbc2a">number</font> - duration of the loss-of-control cooldown in seconds; 0 if the spell is not currently affected by a loss-of-control cooldown.</dd></dl></dd>
[...]
</div>

### Reasoning:
The function `GetSpellLossOfControlCooldown` takes a mandatory `spellSlot` argument and one additional optional argument, which can be either `bookType`, `spellName`, or `spellID`. This results in four valid parameter combinations. To accurately document the flexibility of the API and ensure clarity in parameter descriptions and return values, four distinct function signatures were created, each representing a valid way to call the function.

### Output:
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot)', 'summary': 'Returns information about a loss-of-control cooldown affecting a spell.'}} name='Add_summary'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot)', 'param_description': 'spell book slot index, ascending from 1.', 'param_name': 'spellSlot', 'param_type': 'number'}} name='Add_param'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot)', 'return_description': 'time at which the loss-of-control cooldown began, per GetTime.', 'return_name': 'start', 'return_type': 'number'}} name='Add_return'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot)', 'return_description': 'duration of the loss-of-control cooldown in seconds; 0 if the spell is not currently affected by a loss-of-control cooldown.', 'return_name': 'duration', 'return_type': 'number'}} name='Add_return'

args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, bookType)', 'summary': 'Returns information about a loss-of-control cooldown affecting a spell.'}} name='Add_summary'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, bookType)', 'param_description': 'spell book slot index, ascending from 1.', 'param_name': 'spellSlot', 'param_type': 'number'}} name='Add_param'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, bookType)', 'param_description': 'spell book type token, e.g. "spell" from player\'s spell book.', 'param_name': 'bookType', 'param_type': 'string'}} name='Add_param'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, bookType)', 'return_description': 'time at which the loss-of-control cooldown began, per GetTime.', 'return_name': 'start', 'return_type': 'number'}} name='Add_return'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, bookType)', 'return_description': 'duration of the loss-of-control cooldown in seconds; 0 if the spell is not currently affected by a loss-of-control cooldown.', 'return_name': 'duration', 'return_type': 'number'}} name='Add_return'

args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellName)', 'summary': 'Returns information about a loss-of-control cooldown affecting a spell.'}} name='Add_summary'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellName)', 'param_description': 'spell book slot index, ascending from 1.', 'param_name': 'spellSlot', 'param_type': 'number'}} name='Add_param'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellName)', 'param_description': 'name of a spell in the player\'s spell book.', 'param_name': 'spellName', 'param_type': 'string'}} name='Add_param'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellName)', 'return_description': 'time at which the loss-of-control cooldown began, per GetTime.', 'return_name': 'start', 'return_type': 'number'}} name='Add_return'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellName)', 'return_description': 'duration of the loss-of-control cooldown in seconds; 0 if the spell is not currently affected by a loss-of-control cooldown.', 'return_name': 'duration', 'return_type': 'number'}} name='Add_return'

args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellID)', 'summary': 'Returns information about a loss-of-control cooldown affecting a spell.'}} name='Add_summary'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellID)', 'param_description': 'spell book slot index, ascending from 1.', 'param_name': 'spellSlot', 'param_type': 'number'}} name='Add_param'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellID)', 'param_description': 'spell ID of a spell accessible to the player.', 'param_name': 'spellID', 'param_type': 'number'}} name='Add_param'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellID)', 'return_description': 'time at which the loss-of-control cooldown began, per GetTime.', 'return_name': 'start', 'return_type': 'number'}} name='Add_return'
args={{'for_function_signature': 'GetSpellLossOfControlCooldown(spellSlot, spellID)', 'return_description': 'duration of the loss-of-control cooldown in seconds; 0 if the spell is not currently affected by a loss-of-control cooldown.', 'return_name': 'duration', 'return_type': 'number'}} name='Add_return'

## Example 4:

### Input (Partial example):
<div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
[...]
<p>Needs summary.
</p>
<pre>known, max = C_Engraving.GetNumRunesKnown([equipmentSlot])</pre>
<h2><span class="mw-headline" id="Arguments">Arguments</span></h2>
<dl><dd><dl><dt>equipmentSlot</dt>
<dd><font color="#ecbc2a">number</font><span title="nilable">?</span></dd></dl></dd></dl>
<h2><span class="mw-headline" id="Returns">Returns</span></h2>
<dl><dd><dl><dt>known</dt>
<dd><font color="#ecbc2a">number</font></dd>
<dt>max</dt>
<dd><font color="#ecbc2a">number</font></dd></dl></dd></dl>
[...]
</div>

### Output:

args={{'for_function_signature': 'C_Engraving.GetNumRunesKnown(equipmentSlot)', 'summary': 'Returns the number of runes known and the maximum number of runes available, optionally for a specified equipment slot.'}} name='Add_summary'
args={{'for_function_signature': 'C_Engraving.GetNumRunesKnown(equipmentSlot)', 'param_description': 'optional equipment slot index.', 'param_name': 'equipmentSlot', 'param_type': 'number?'}} name='Add_param'
args={{'for_function_signature': 'C_Engraving.GetNumRunesKnown(equipmentSlot)', 'return_description': 'number of runes known.', 'return_name': 'known', 'return_type': 'number'}} name='Add_return'
args={{'for_function_signature': 'C_Engraving.GetNumRunesKnown(equipmentSlot)', 'return_description': 'maximum number of runes available.', 'return_name': 'max', 'return_type': 'number'}} name='Add_return'


ONLY RESPOND WITH tool_calls
"""
# - If a function parameter can accept multiple types (e.g., string or number), use the format "type1|type2". Example: string|number. Additionally, if two parameters serve the same purpose but accept different types (e.g., spellName and spellId), consolidate them into a single parameter with a descriptive name (spellNameOrId in this case).

# 8. ALWAYS include the documentation link. NEVER use ---@see - PS. ONLY USE 'https://warcraft.wiki.gg' NO OTHER LINKS ALLOWED
# 9. Always respond with the function signature, if you are unsure add a comment on the first line '---! DRAFT - NEEDS REVIEW'
# 10. NEVER include anything more than the function signature. No fluff or extra responses.

# default_api.Add_summary_Hint(summary = "Retrieves tag information about the quest.")
# default_api.Add_param_Hint(param_name = "questID", param_type = "number", param_description = "The ID of the quest to retrieve the tag info for.")
# default_api.Add_return_Hint(return_name = "tagID", return_type = "number", return_description = "the tagID, nil if quest is not tagged")
# default_api.Add_return_Hint(return_name = "tagName", return_type = "string", return_description = "human readable representation of the tagID, nil if quest is not tagged")
# default_api.Add_return_Hint(return_name = "worldQuestType", return_type = "number", return_description = "type of world quest, or nil if not world quest")
# default_api.Add_return_Hint(return_name = "rarity", return_type = "number", return_description = "the rarity of the quest (used for world quests)")
# default_api.Add_return_Hint(return_name = "isElite", return_type = "boolean", return_description = "is this an elite quest?  (used for world quests)")
# default_api.Add_return_Hint(return_name = "tradeskillLineIndex", return_type = "unknown", return_description = "tradeskillID if this is a profession quest  (used to determine which profession icon to display for world quests)")
# default_api.Add_return_Hint(return_name = "displayTimeLeft", return_type = "unknown", return_description = "?")
# default_api.Add_function_definition(function_signature = "GetQuestTagInfo(questID)")

# <example_6>
# ---Converts the current party to a raid.<br>
# ---[Documentation](https://warcraft.wiki.gg/wiki/API_ConvertToRaid)
# function ConvertToRaid() end
# </example_6>
# 11. NEVER change the function name, on a redirect page, use the original function name.

add_summary_hint_def = types.FunctionDeclaration(
  name="Add_summary",
  description="""Add a summary to a function signature.
# Example 1:

# Input (Partial example):

<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
[...]
<p>Retrieves tag information about the quest.</p>
<pre>tagID, tagName, worldQuestType, rarity, isElite, tradeskillLineIndex, displayTimeLeft = GetQuestTagInfo(questID)</pre>
[...]
<dd><dl><dt>questID</dt>
<dd><font color="#ecbc2a">number</font> - The ID of the quest to retrieve the tag info for.</dd></dl></dd>
[...]
<dd><dl><dt>tagID</dt>
<dd><font color="#ecbc2a">number</font> - the tagID, nil if quest is not tagged</dd>
<dt>tagName</dt>
<dd><font color="#ecbc2a">string</font> - human readable representation of the tagID, nil if quest is not tagged</dd>
<dt>worldQuestType</dt>
<dd><font color="#ecbc2a">number</font> - type of world quest, or nil if not world quest</dd>
<dt>rarity</dt>
<dd><font color="#ecbc2a">number</font> - the rarity of the quest (used for world quests)</dd>
<dt>isElite</dt>
<dd><font color="#ecbc2a">boolean</font> - is this an elite quest?  (used for world quests)</dd>
<dt>tradeskillLineIndex</dt>
<dd>tradeskillID if this is a profession quest  (used to determine which profession icon to display for world quests)</dd>
<dt>displayTimeLeft</dt>
<dd>?</dd></dl></dd>
[...]
</div>

# Output:

default_api.Add_summary_Hint(summary = "Retrieves tag information about the quest.", for_function_signature = "GetQuestTagInfo(questID)")

# Example 2:

## Input (Partial example):

<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output">
[...]
<p>Retrieves the number of runes known, optionally for a specified equipment slot.</p>
<pre>known, max = C_Engraving.GetNumRunesKnown([equipmentSlot])</pre>
[...]
<dd><dl><dt>equipmentSlot</dt>
<dd><font color="#ecbc2a">number</font><span title="nilable">?</span> - Optional equipment slot index for querying the rune count.</dd></dl></dd>
[...]
</div>

## Reasoning:
Do not add the [ ] to the param_name. The [ ] is used to denote optional parameters. The nilable type is denoted by adding a '?' after the type.

## Output:

default_api.Add_summary_Hint(summary = "Retrieves the number of runes known, optionally for a specified equipment slot.", for_function_signature = "C_Engraving.GetNumRunesKnown(equipmentSlot)")

# Note:

ALWAYS include for_function_signature to specify which function the return is for.
""",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "summary": types.Schema(
        type=types.Type.STRING,
        description="The summary of the function",
      ),
      "for_function_signature": types.Schema(
        type=types.Type.STRING,
        description="The function signature this param is for",
      ),
    },
    required=["summary", "for_function_signature"],
  ),
)

add_param_hint_def = types.FunctionDeclaration(
  name="Add_param",
  description="""Add a parameter to a function signature.

# Example 1:

## Input (Partial example):

<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
[...]
<p>Retrieves tag information about the quest.</p>
<pre>tagID, tagName, worldQuestType, rarity, isElite, tradeskillLineIndex, displayTimeLeft = GetQuestTagInfo(questID)</pre>
[...]
<dd><dl><dt>questID</dt>
<dd><font color="#ecbc2a">number</font> - The ID of the quest to retrieve the tag info for.</dd></dl></dd>
[...]
<dd><dl><dt>tagID</dt>
<dd><font color="#ecbc2a">number</font> - the tagID, nil if quest is not tagged</dd>
<dt>tagName</dt>
<dd><font color="#ecbc2a">string</font> - human readable representation of the tagID, nil if quest is not tagged</dd>
<dt>worldQuestType</dt>
<dd><font color="#ecbc2a">number</font> - type of world quest, or nil if not world quest</dd>
<dt>rarity</dt>
<dd><font color="#ecbc2a">number</font> - the rarity of the quest (used for world quests)</dd>
<dt>isElite</dt>
<dd><font color="#ecbc2a">boolean</font> - is this an elite quest?  (used for world quests)</dd>
<dt>tradeskillLineIndex</dt>
<dd>tradeskillID if this is a profession quest  (used to determine which profession icon to display for world quests)</dd>
<dt>displayTimeLeft</dt>
<dd>?</dd></dl></dd>
[...]
</div>

## Output:

default_api.Add_param_Hint(param_name = "questID", param_type = "number", param_description = "The ID of the quest to retrieve the tag info for.", for_function_signature = "GetQuestTagInfo(questID)")

# Example 2:

## Input (Partial example):

<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output">
[...]
<p>Retrieves the number of runes known, optionally for a specified equipment slot.</p>
<pre>known, max = C_Engraving.GetNumRunesKnown([equipmentSlot])</pre>
[...]
<dd><dl><dt>equipmentSlot</dt>
<dd><font color="#ecbc2a">number</font><span title="nilable">?</span> - Optional equipment slot index for querying the rune count.</dd></dl></dd>
[...]
</div>

## Reasoning:
Do not add the [ ] to the param_name. The [ ] is used to denote optional parameters. The nilable type is denoted by adding a '?' after the type.

## Output:

default_api.Add_param_Hint(param_name = "equipmentSlot", param_type = "number?", param_description = "Optional equipment slot index for querying the number of known runes.", for_function_signature = "C_Engraving.GetNumRunesKnown(equipmentSlot)")

# Note:

ALWAYS include for_function_signature to specify which function the return is for.
""",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "param_name": types.Schema(
        type=types.Type.STRING,
        description="The name of the parameter",
      ),
      "param_type": types.Schema(
        type=types.Type.STRING,
        description="The type of the parameter",
      ),
      "param_description": types.Schema(
        type=types.Type.STRING,
        description="The description of the parameter",
      ),
      "for_function_signature": types.Schema(
        type=types.Type.STRING,
        description="The function signature this param is for",
      ),
    },
    required=["param_name", "param_type", "param_description", "for_function_signature"],
  ),
)

add_return_hint_def = types.FunctionDeclaration(
  name="Add_return",
  description="""Add a return to a function signature.

# Example 1:

## Input (Partial example):

<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
[...]
<p>Retrieves tag information about the quest.</p>
<pre>tagID, tagName, worldQuestType, rarity, isElite, tradeskillLineIndex, displayTimeLeft = GetQuestTagInfo(questID)</pre>
[...]
<dd><dl><dt>questID</dt>
<dd><font color="#ecbc2a">number</font> - The ID of the quest to retrieve the tag info for.</dd></dl></dd>
[...]
<dd><dl><dt>tagID</dt>
<dd><font color="#ecbc2a">number</font> - the tagID, nil if quest is not tagged</dd>
<dt>tagName</dt>
<dd><font color="#ecbc2a">string</font> - human readable representation of the tagID, nil if quest is not tagged</dd>
<dt>worldQuestType</dt>
<dd><font color="#ecbc2a">number</font> - type of world quest, or nil if not world quest</dd>
<dt>rarity</dt>
<dd><font color="#ecbc2a">number</font> - the rarity of the quest (used for world quests)</dd>
<dt>isElite</dt>
<dd><font color="#ecbc2a">boolean</font> - is this an elite quest?  (used for world quests)</dd>
<dt>tradeskillLineIndex</dt>
<dd>tradeskillID if this is a profession quest  (used to determine which profession icon to display for world quests)</dd>
<dt>displayTimeLeft</dt>
<dd>?</dd></dl></dd>
[...]
</div>

## Output:

default_api.Add_return_Hint(return_name = "tagID", return_type = "number", return_description = "the tagID, nil if quest is not tagged", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "tagName", return_type = "string", return_description = "human readable representation of the tagID, nil if quest is not tagged", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "worldQuestType", return_type = "number", return_description = "type of world quest, or nil if not world quest", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "rarity", return_type = "number", return_description = "the rarity of the quest (used for world quests)", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "isElite", return_type = "boolean", return_description = "is this an elite quest?  (used for world quests)", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "tradeskillLineIndex", return_type = "unknown", return_description = "tradeskillID if this is a profession quest  (used to determine which profession icon to display for world quests)", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "displayTimeLeft", return_type = "unknown", return_description = "?", for_function_signature = "GetQuestTagInfo(questID))

# Example 2:

## Input (Partial example):

[...]
<dd><dl><dt>"itemLink"</dt>
<dd><a href="/wiki/ItemLink" title="ItemLink">itemLink</a> - the corresponding item link for that item or</dd></dl></dd>
<dd>nil, if the index is invalid or there is no active trade skill.</dd>
[...]

## Reasoning:
The extra <dd> is a part of the description and should be included in the return_description.

## Output:

default_api.Add_return_Hint(return_name = "itemLink", return_type = "ItemLink", return_description = "the corresponding item link for that item or nil, if the index is invalid or there is no active trade skill.", for_function_signature = "GetCraftItemLink(index)")

# Example 3:

## Input (Partial example):

[...]
<dd><dl><dt>gem1, gem2, ...</dt>
<dd>Number - Item ID of the gem(s) socketed within the item in the queried slot.</dd></dl></dd>
[...]

## Reasoning:
When there are multiple returns as vararg (gem1, gem2, ...), use ... as name and add "gem1, gem2, ..." to the description to denote the multiple returns

## Output:

default_api.Add_return_Hint(return_name = "...", return_type = "number", return_description = "gem1, gem2, ... - Item ID of the gem(s) socketed within the item in the queried slot.", for_function_signature = "GetInventoryItemGems(invSlot)")

# Example 4:

## Input (Partial example):

<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output">
[...]
<p>Retrieves the number of runes known, optionally for a specified equipment slot.</p>
<pre>known, max = C_Engraving.GetNumRunesKnown([equipmentSlot])</pre>
[...]
<dd><dl><dt>equipmentSlot</dt>
<dd><font color="#ecbc2a">number</font><span title="nilable">?</span> - Optional equipment slot index for querying the rune count.</dd></dl></dd>
[...]
</div>

## Reasoning:
Do not add the [ ] to the param_name. The [ ] is used to denote optional parameters. The nilable type is denoted by adding a '?' after the type.

## Output:

default_api.Add_return_Hint(return_name = "known", return_type = "number", return_description = "number of runes known.", for_function_signature = "C_Engraving.GetNumRunesKnown(equipmentSlot)")

# Note:

ALWAYS include for_function_signature to specify which function the return is for.
""",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "return_name": types.Schema(
        type=types.Type.STRING,
        description="The name of the return",
      ),
      "return_type": types.Schema(
        type=types.Type.STRING,
        description="The type of the return",
      ),
      "return_description": types.Schema(
        type=types.Type.STRING,
        description="The description of the return",
      ),
      "for_function_signature": types.Schema(
        type=types.Type.STRING,
        description="The function signature this return is for",
      ),
    },
    required=["return_name", "return_type", "return_description", "for_function_signature"],
  ),
)

# Add_function_definition_def = types.FunctionDeclaration(
#   name="Add_function_definition",
#   description="""Add a function name and parameters to a function signature.

# # Example 1:

# # Input (Partial example):

# <div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output"><div style="float:right; margin-left:1em; margin-left:max(1em, 1.5%); margin-bottom:0.2em;">
# [...]
# <pre>tagID, tagName, worldQuestType, rarity, isElite, tradeskillLineIndex, displayTimeLeft = GetQuestTagInfo(questID)</pre>
# [...]
# <dd><dl><dt>questID</dt>
# <dd><font color="#ecbc2a">number</font> - The ID of the quest to retrieve the tag info for.</dd></dl></dd>
# <dt>tagID</dt>
# [...]
# </div>

# # Output:

# default_api.Add_function_definition(function_signature = "GetQuestTagInfo(questID)")

# # Note:

# If there are multiple functions such as by index or ID, add each function signature separately.
# """,
#   parameters=types.Schema(
#     type=types.Type.OBJECT,
#     properties={
#       "function_signature": types.Schema(
#         type=types.Type.STRING,
#         description="The function signature",
#       ),
#     },
#     required=["function_signature"],
#   ),
# )


def GetHTMLContent(url: str) -> str:
  response = requests.get("https://warcraft.wiki.gg" + url)
  return response.text


def extract_content_body(html: str) -> str:
  soup = BeautifulSoup(html, "html.parser")
  content_div = soup.find("div", class_="content-body")
  if content_div:
    return str(content_div)
  else:
    return "Content-body not found."


path = os.path.join(".", "Functions-Classic-AI-GeminAI")
# Delete the directory and contents if it exists
if os.path.exists(path):
  shutil.rmtree(path)


def write_file(content: str, filename: str) -> str:
  """Tool: Writes content to a file."""
  os.makedirs(path, exist_ok=True)
  filename = os.path.join(path, filename)
  fileExists = os.path.isfile(filename)
  with open(filename, "a+") as f:  # Change "w+" to "a"
    if not fileExists:
      f.write(f"---@meta\n--* GENERATED BY {model}\n\n")
    f.write(content + "\n\n")

  return f"Content written to {filename}"


filedict = {}

lookupfile = "lookup.json"

# Check if file exists
fileExists = os.path.isfile(lookupfile)
if fileExists:
  print("Loading already existing file")
  with open(lookupfile, "r", encoding="utf-8") as f:
    data = f.read()
  filedict = json.loads(data)
else:
  print("File does not exist")
  exit(1)

# Revert the dict so that each url has a corresponding filename
url_to_filename = {}
for filename, urls in filedict.items():
  for url in urls:
    url_to_filename[url] = filename

dat = [
  # "/wiki/API_C_QuestLog.GetQuestWatchType",
  # "/wiki/API_C_QuestLog.GetBountySetInfoForMapID",
  # ? "/wiki/API_GetArenaTeam",
  # ? "/wiki/API_BNGetFriendInfo",
  # ? "/wiki/API_BNGetFriendGameAccountInfo",
  "/wiki/API_GetCraftItemLink",
  "/wiki/API_C_Engraving.GetNumRunesKnown",
  "/wiki/API_GetSpellLink",
  "/wiki/API_GetSpellLossOfControlCooldown",
  "/wiki/API_IsPassiveSpell",
  "/wiki/API_IsSpellInRange",
  "/wiki/API_GetSpellAutocast",
  "/wiki/API_GetInventoryItemGems",
  "/wiki/API_AddQuestWatch",
]

dat = GetData()


# Use regex to extract the namespaces such as C_QuestLog, C_BattleNet and so on.
namespaces = []
responseData = {}
count = 1
tool = types.Tool(
  function_declarations=[
    add_summary_hint_def,
    add_param_hint_def,
    add_return_hint_def,
    # Add_function_definition_def,
  ]
)


read_from_file = True
all_function_signatures = {}

# Read in all_function_signatures from a file
if os.path.isfile("all_function_signatures.json") and read_from_file:
  with open("all_function_signatures.json", "r") as f:
    all_function_signatures = json.load(f)


for url in dat:
  if read_from_file and url in all_function_signatures:
    print(count, "/", len(dat), f"Skipping https://warcraft.wiki.gg{url}")
    count += 1
    continue
  else:
    print(count, "/", len(dat), f"Processing https://warcraft.wiki.gg{url}")
  html = GetHTMLContent(url)
  content = extract_content_body(html)

  response = client.models.generate_content(
    model=model,
    # This pure also works, the extra is a second test that was last used.
    contents=f"```html\n{content}\n```\nUsing the examples and data in the system instruction please return the function signature(s) for the HTML data in this message.",
    # contents="# HTML TO PARSE:\n\n" + content + "\n\n\n\n\nNEVER output any duplicate functions.",
    config=types.GenerateContentConfig(
      # This pure also works, the extra is a second test that was last used.
      # Remember to ermove the <functions> from the system_instruction if you are using the pure contents.
      # system_instruction=system_prompt,
      system_instruction=system_prompt,
      temperature=0,
      tools=[tool],
    ),
  )

  # print(response)

  function_signatures = {}
  for func in response.function_calls or []:
    if func:
      print(func)
      if func.args and "for_function_signature" in func.args:
        function_signature = func.args["for_function_signature"]
        if function_signature not in function_signatures:
          function_signatures[function_signature] = {
            "summary": "",
            "params": [],
            "returns": [],
            "documenation": [f"---[Documentation](https://warcraft.wiki.gg{url})"],
          }
      if func.name == "Add_summary" and func.args:
        for_function_signature = func.args["for_function_signature"]
        summary = func.args["summary"]
        if len(summary) != 0:
          summary = "Needs summary."
        function_signatures[for_function_signature]["summary"] = summary
      elif func.name == "Add_param" and func.args:
        for_function_signature = func.args["for_function_signature"]
        param_name = func.args["param_name"]
        param_type = func.args["param_type"]
        param_description = func.args.get("param_description", "")
        param_hint = f"---@param {param_name} {param_type}"
        if len(param_description) != 0:
          param_hint += f" - {param_description}"
        function_signatures[for_function_signature]["params"].append(param_hint)

      elif func.name == "Add_return" and func.args:
        for_function_signature = func.args["for_function_signature"]
        return_name = func.args["return_name"]
        return_type = func.args["return_type"]
        return_description = func.args.get("return_description", "")
        return_hint = f"---@return {return_type} {return_name}"
        if len(return_description) != 0:
          return_hint += f" - {return_description}"
        function_signatures[for_function_signature]["returns"].append(return_hint)

      # elif func.name == "Add_function_definition" and func.args:
      #   if func.args["function_signature"] not in function_signatures:
      #     function_signatures[func.args["function_signature"]] = {
      #       "summary": "",
      #       "params": [],
      #       "returns": [],
      #     }

  # print(json.dumps(function_signatures, indent=2))
  all_function_signatures[url] = function_signatures

  count += 1

for url, function_signatures in all_function_signatures.items():
  functions = {}
  for signature, data in function_signatures.items():
    hint = ""
    if len(function_signatures) > 1:
      hint += "---! DRAFT - More than one function signature<br>\n"
    if data["summary"]:
      hint += f"---{data['summary']}<br>\n"
    if data["documenation"]:
      hint += "\n".join(data["documenation"]) + "\n"
    if data["params"]:
      # Multi-line param hints
      for param in data["params"]:
        param = param.replace("\n", "<br>\n---")
        hint += param + "\n"
    if data["returns"]:
      for ret in data["returns"]:
        ret = ret.replace("\n", "<br>\n---")
        hint += ret + "\n"
      # hint += "\n".join(data["returns"]) + "\n"
    hint += f"function {signature} end"

    functions[signature] = hint
    print(hint, "\n")

  combined_functions = "\n\n".join(functions.values())

  # In IsPassiveSpell there is a non-breaking-space that does not play well with LuaLS.
  combined_functions = combined_functions.replace("\xa0", " ")

  responseData[url] = combined_functions

  matches = re.findall(r"function\W+(C_.*?)\.", combined_functions)
  namespace = matches[0] if matches else None
  if namespace and namespace not in namespaces:
    namespaces.append(namespace)

# # Dump all_function_signatures to a file
# with open("all_function_signatures.json", "w") as f:
#   json.dump(all_function_signatures, f, indent=2)

for url, content in responseData.items():
  filename = url_to_filename[url]
  write_file(content, filename)
  print(f"Content written to {filename} - {url}")

# Write the namespaces to a file
write_file(
  f"""
{" = {}\n".join(namespaces)} = {{}}
""",
  "Namespaces.lua",
)
