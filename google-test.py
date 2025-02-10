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

load_dotenv()

# Only run this block for Gemini Developer API
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with open("LuaTypes.md", "r") as f:  # changed variable from os to f
  LuaTypesContent = f.read()

model = "gemini-2.0-flash-lite-preview-02-05"
model = "gemini-2.0-flash"

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

## Examples of Outputs
<example_1>
---Returns the bounty set for a specified map ID.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetBountySetInfoForMapID)
---@param uiMapID number
---@return Enum.MapOverlayDisplayLocation displayLocation
---@return number lockQuestID
---@return number bountySetID
---@return boolean isActivitySet
function C_QuestLog.GetBountySetInfoForMapID(uiMapID) end
</example_1>

<example_2>
---Returns info for the objectives of a quest.<br>
---Quests that have been encountered before (i.e. cached) are able to be queried instantly, however if the function is supplied a quest ID of a quest that isn't cached yet, it will not return anything until called again. Sometimes three calls are needed to fully cache everything (such as text).<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestObjectives)
---@param questID number
---@return QuestObjectiveInfo[] objectives
function C_QuestLog.GetQuestObjectives(questID) end
</example_2>

<example_3>
---! DRAFT - NEEDS REVIEW<br>
---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestAdditionalHighlights)
---@param questID number
---@return number uiMapID
---@return boolean worldQuests
---@return boolean worldQuestsElite
---@return boolean dungeons
---@return boolean treasures
function C_QuestLog.GetQuestAdditionalHighlights(questID) end
</example_3>

<example_4>
---Retrieves tag information about the quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestTagInfo)
---@param questID number The ID of the quest to retrieve the tag info for.
---@return number? tagID The tag ID, or nil if quest is not tagged.
---@return string? tagName Human readable representation of the tag ID, or nil if quest is not tagged.
---@return number? worldQuestType Type of world quest, or nil if not a world quest.
---@return number rarity The rarity of the quest (used for world quests).
---@return boolean isElite Whether this is an elite quest (used for world quests).
---@return number tradeskillLineIndex Tradeskill ID if this is a profession quest (used to determine which profession icon to display for world quests).
---@return unknown displayTimeLeft The remaining display time, may need further documentation for exact type.
function GetQuestTagInfo(questID) end
</example_4>

<example_5>
---Returns the currently tracked achievements.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTrackedAchievements)
---@return number ... id1, id2, id3, ... The IDs of the achievements being tracked.
function GetTrackedAchievements() end
</example_5>

<example_6>
Note: The example below used a banned keyword 'repeat' in the HTML which is not allowed in the function signature. Let's change it to repeatCount instead.

---! DRAFT - NEEDS REVIEW<br>
---Performs the tradeskill a specified number of times.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_DoTradeSkill)
---@param index number The index of the tradeskill recipe.
---@param repeatCount number The number of times to repeat the creation of the specified recipe.
function DoTradeSkill(index, repeatCount) end
</example_6>

<example_skeleton>
--- SUMMARY<br>
--- EXTRA DETAILS<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_)
---@param param1 type1
---@param param2 type2
---@return returnType1
---@return returnType2
function FunctionName(param1, param2) end
</example_skeleton>


Always have the function be one line, this is part of a file that are ---@meta definitions and do not contain the function body.

# Steps to follow:
1. You will get RAW HTML content your job is to convert it to Lua Type hints.
2. Never include the 'API_' prefix in the function name.
4. Always include all the parameters and return types. Omit if no parameters or return types.
5. If the type is not known, use 'unknown'.
6. Write a summary of the function in the first line. Using <br> to separate lines, like in the examples.
7. If there are additional details about the function, focus only on the the most important parts and keep it SHORT.
8. ALWAYS include the documentation link. NEVER use ---@see - PS. ONLY USE 'https://warcraft.wiki.gg' NO OTHER LINKS ALLOWED
9. Always respond with the function signature, if you are unsure add a comment on the first line '---! DRAFT - NEEDS REVIEW'
10. NEVER include anything more than the function signature. No fluff or extra responses.


# Parsed functions so far:
<functions>
"""

# <example_6>
# ---Converts the current party to a raid.<br>
# ---[Documentation](https://warcraft.wiki.gg/wiki/API_ConvertToRaid)
# function ConvertToRaid() end
# </example_6>
# 11. NEVER change the function name, on a redirect page, use the original function name.


def GetHTMLContent(url: str) -> str:
  response = requests.get("https://warcraft.wiki.gg" + url)
  return response.text


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

dat = GetData()

# Use regex to extract the namespaces such as C_QuestLog, C_BattleNet and so on.
namespaces = []
responseData = {}
count = 1
for url in dat:
  print(count, "/", len(dat), f"Processing {url}")
  content = GetHTMLContent(url)

  response = client.models.generate_content(
    model=model,
    # This pure also works, the extra is a second test that was last used.
    # contents=content,
    contents="# HTML TO PARSE:\n\n" + content + "\n\n\n\n\nNEVER output any duplicate functions.",
    config=types.GenerateContentConfig(
      # This pure also works, the extra is a second test that was last used.
      # Remember to ermove the <functions> from the system_instruction if you are using the pure contents.
      # system_instruction=system_prompt,
      system_instruction=system_prompt + json.dumps(responseData, indent=2) + "\n</functions>",
      temperature=0,
    ),
  )
  response = response.text
  response = response.replace("```lua", "").strip()
  response = response.replace("```", "").strip()
  responseData[url] = response

  matches = re.findall(r"function\W+(C_.*?)\.", response)
  namespace = matches[0] if matches else None
  if namespace and namespace not in namespaces:
    namespaces.append(namespace)
  # filename = url_to_filename[url]
  # write_file(response, filename)
  count += 1

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
