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



ONLY RESPOND WITH tool_calls
"""

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
</div>

# Output:

default_api.Add_summary_Hint(summary = "Retrieves tag information about the quest.", for_function_signature = "GetQuestTagInfo(questID)")

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

[...]
<dd><dl><dt>questID</dt>
<dd><font color="#ecbc2a">number</font> - The ID of the quest to retrieve the tag info for.</dd></dl></dd>
[...]

## Output:

default_api.Add_param_Hint(param_name = "questID", param_type = "number", param_description = "The ID of the quest to retrieve the tag info for.", for_function_signature = "GetQuestTagInfo(questID)")

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
[...]
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
<dd>?</dd>
[...]

## Output:

default_api.Add_return_Hint(return_name = "tagID", return_type = "number", return_description = "the tagID, nil if quest is not tagged", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "tagName", return_type = "string", return_description = "human readable representation of the tagID, nil if quest is not tagged", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "worldQuestType", return_type = "number", return_description = "type of world quest, or nil if not world quest", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "rarity", return_type = "number", return_description = "the rarity of the quest (used for world quests)", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "isElite", return_type = "boolean", return_description = "is this an elite quest?  (used for world quests)", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "tradeskillLineIndex", return_type = "unknown", return_description = "tradeskillID if this is a profession quest  (used to determine which profession icon to display for world quests)", for_function_signature = "GetQuestTagInfo(questID)")
default_api.Add_return_Hint(return_name = "displayTimeLeft", return_type = "unknown", return_description = "?", for_function_signature = "GetQuestTagInfo(questID))

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

dat = GetData()

# dat = [
#   # "/wiki/API_C_QuestLog.GetQuestWatchType",
#   # "/wiki/API_C_QuestLog.GetBountySetInfoForMapID",
#   "/wiki/API_BNGetFriendInfo",
# ]

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
for url in dat:
  print(count, "/", len(dat), f"Processing {url}")
  html = GetHTMLContent(url)
  content = extract_content_body(html)

  response = client.models.generate_content(
    model=model,
    # This pure also works, the extra is a second test that was last used.
    contents=content,
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
          }
      if func.name == "Add_summary" and func.args:
        for_function_signature = func.args["for_function_signature"]
        summary = func.args["summary"]
        if len(summary) == 0:
          summary = "Needs summary."
        function_signatures[for_function_signature]["summary"] = summary
      elif func.name == "Add_param" and func.args:
        for_function_signature = func.args["for_function_signature"]
        param_name = func.args["param_name"]
        param_type = func.args["param_type"]
        param_description = func.args["param_description"]
        param_hint = f"---@param {param_name} {param_type}"
        if len(param_description) == 0:
          param_hint += f" - {param_description}"
        function_signatures[for_function_signature]["params"].append(param_hint)

      elif func.name == "Add_return" and func.args:
        for_function_signature = func.args["for_function_signature"]
        return_name = func.args["return_name"]
        return_type = func.args["return_type"]
        return_description = func.args["return_description"]
        return_hint = f"---@return {return_type} {return_name}"
        if len(return_description) == 0:
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

  functions = {}
  for signature, data in function_signatures.items():
    hint = ""
    if len(function_signatures) > 1:
      hint += "---! DRAFT - More than one function signature\n"
    if data["summary"]:
      hint += f"---{data['summary']}\n"
    if data["params"]:
      hint += "\n".join(data["params"]) + "\n"
    if data["returns"]:
      hint += "\n".join(data["returns"]) + "\n"
    hint += f"function {signature} end"

    functions[signature] = hint
    print(hint, "\n")

  combined_functions = "\n\n".join(functions.values())
  responseData[url] = combined_functions

  matches = re.findall(r"function\W+(C_.*?)\.", combined_functions)
  namespace = matches[0] if matches else None
  if namespace and namespace not in namespaces:
    namespaces.append(namespace)

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
