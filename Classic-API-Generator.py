from openai import OpenAI
import json
import os
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from WikiGetData import GetData

load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

model = "o3-mini"
model = "gpt-4o"


###############################
###############################
############## Lua Generation ###########
###############################
###############################


def write_file(content: str, filename: str) -> str:
  """Tool: Writes content to a file."""
  path = os.path.join(".", "Functions-Classic-AI")
  os.makedirs(path, exist_ok=True)
  filename = os.path.join(path, filename)
  fileExists = os.path.isfile(filename)
  with open(filename, "a+") as f:  # Change "w+" to "a"
    if not fileExists:
      f.write("---@meta\n")
    f.write(content + "\n")

  return f"Content written to {filename}"


def generate_output_with_tool(url: str) -> str:
  print("Fetching ", url)
  with open("LuaTypes.md", "r") as os:
    LuaTypesContent = os.read()

  system_prompt = f"""You are an expert at writing Lua Language Server compatible Type hints:
  
  
  ## Documentation about Lua Types
  {LuaTypesContent}

  ## Examples of Outputs
  Example 1:
  ---Returns the bounty set for a specified map ID. 
  ---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetBountySetInfoForMapID)
  ---@param uiMapID number
  ---@return Enum.MapOverlayDisplayLocation displayLocation
  ---@return number lockQuestID
  ---@return number bountySetID
  ---@return boolean isActivitySet
  function C_QuestLog.GetBountySetInfoForMapID(uiMapID) end

  Example 2:
  ---Returns info for the objectives of a quest. 
  ---
  ---Quests that have been encountered before (i.e. cached) are able to be queried instantly, however if the function is supplied a quest ID of a quest that isn't cached yet, it will not return anything until called again. Sometimes three calls are needed to fully cache everything (such as text). 
  ---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestObjectives)
  ---@param questID number
  ---@return QuestObjectiveInfo[] objectives
  function C_QuestLog.GetQuestObjectives(questID) end
  
  Example 3:
  ---Needs summary.
  ---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestAdditionalHighlights)
  ---@param questID number
  ---@return number uiMapID
  ---@return boolean worldQuests
  ---@return boolean worldQuestsElite
  ---@return boolean dungeons
  ---@return boolean treasures
  function C_QuestLog.GetQuestAdditionalHighlights(questID) end

  Always have the function be one line, this is part of a file that are ---@meta definitions and do not contain the function body.

  1. You will get RAW HTML content your job is to convert it to Lua Type hints.
  2. Never include the 'API_' prefix in the function name.
  4. Always include all the parameters and return types.
  5. Write a summary of the function in the first line.
  6. If there are additional details about the function, focus only on the the most important parts and keep it SHORT.
  7. ALWAYS include the documentation link.
  8. Always respond with the function signature, if you are unsure add a comment on the first line '---! DRAFT - NEEDS REVIEW'
  9. NEVER include anything more than the function signature. No fluff or extra responses.
"""

  content = GetHTMLContent(url)

  # Call GPT-4 with tool support (function calling)
  response = client.chat.completions.create(
    model=model,
    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": content}],
    # tools=tools,
    # tool_choice="auto",  # let the model decide if it wants to call a tool
  )

  message = response.choices[0].message

  # If GPT-4 decides to call our tool, decode the arguments and call it.
  # if message.tool_calls:
  #   for tool_call in message.tool_calls:
  #     func_name = tool_call.function.name
  #     args = json.loads(tool_call.function.arguments)
  #     if func_name == "write_file":
  #       result = write_file(args["content"], args["filename"])
  #       return result

  # Fallback: return the plain text response.
  return message.content.strip()


def GetHTMLContent(url: str) -> str:
  response = requests.get("https://warcraft.wiki.gg" + url)
  return response.text


def generate_output_with_tool_thread(url: str, url_to_filename: dict, data: dict):
  content = generate_output_with_tool(url)
  content = content.replace("```lua", "")
  content = content.replace("```", "")
  data[url] = content


def main():
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
    for url in GetData():
      print("Parsing ", url)
      added = PlaceFunctionIntoDict(GetData(), filedict, url)
      if not added:
        print(url, "Did not get added")
      # Dump the filedict to file
      with open(lookupfile, "w+", encoding="utf-8") as f:
        f.write(json.dumps(filedict, indent=2))

  # Revert the dict so that each url has a corresponding filename
  url_to_filename = {}
  for filename, urls in filedict.items():
    for url in urls:
      url_to_filename[url] = filename

  data = {}
  with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for url in GetData():
      future = executor.submit(generate_output_with_tool_thread, url, url_to_filename, data)
      futures.append(future)

    for future in futures:
      future.result()

  for url, content in data.items():
    write_file(content, url_to_filename[url])


###############################
###############################
############## Dict ###########
###############################
###############################


def PlaceFunctionIntoDict(array: list, filedict: dict, function: str) -> dict:
  system_prompt = f"""Please add this function into the dict where each function is part of a file.
For example, Quest functions will be in a file called "QuestFunctions.lua", Arena functions in "ArenaFunctions.lua" and so on.

# All functions to sort:
{json.dumps(array, indent=2)}

# EXAMPLE DICT STRUCTURE:
{{
  "QuestFunctions.lua": [
    "/wiki/API_AbandonQuest",
    "/wiki/API_AddQuestWatch",
    "/wiki/API_CanAbandonQuest"
  ],
  "ArenaFunctions.lua": [
    "/wiki/API_AcceptArenaTeam",
    "/wiki/API_ArenaTeamDisband",
    "/wiki/API_ArenaTeamInviteByName",
    "/wiki/API_ArenaTeamSetLeaderByName",
    "/wiki/API_ArenaTeamUninviteByName"
  ],
  "AchievementFunctions.lua": [
    "/wiki/API_AddTrackedAchievement"
  ],
  "BattleNetFunctions.lua": [
    "/wiki/API_BNGetFriendGameAccountInfo",
    "/wiki/API_BNGetFriendInfo",
    "/wiki/API_BNGetFriendInfoByID",
    "/wiki/API_BNGetGameAccountInfo",
    "/wiki/API_BNGetGameAccountInfoByGUID",
    "/wiki/API_BNGetNumFriendGameAccounts"
  ],
  "PetFunctions.lua": [
    "/wiki/API_BuyStableSlot",
    "/wiki/API_ClickStablePet",
    "/wiki/API_ClosePetStables",
    "/wiki/API_ConfirmPetUnlearn"
  ],
  "TradeSkillFunctions": [
    "/wiki/API_CloseTradeSkill"
  ],
  "BankFunctions.lua": [
    "/wiki/API_CloseBankFrame"
  ],
  "ChannelFunctions.lua": [
    "/wiki/API_ChannelInfo"
  ],
  "AuctionFunctions.lua": [
    "/wiki/API_CanSendAuctionQuery",
    "/wiki/API_CancelSell",
    "/wiki/API_ClickAuctionSellItemButton",
    "/wiki/API_CloseAuctionHouse"
  ],
  "SkillFunctions.lua": [
    "/wiki/API_CollapseSkillHeader"
  ],
  "TalentFunctions.lua": [
    "/wiki/API_GetActiveTalentGroup"
  ],
  "BattlefieldFunctions.lua": [
    "/wiki/API_GetBattlefieldFlagPosition",
    "/wiki/API_GetBattlefieldInstanceInfo",
    "/wiki/API_GetBattlefieldStatInfo"
  ]
}}


# Current dict structure:
```json
{json.dumps(filedict, indent=2)}
```

# Task list:
1. Write the function in the format "/wiki/API_FunctionName"
2. Write the function to the correct file.
3. If the file does not exist, create it.
4. If the function already exists in the file, do not add it again.
5. If the function is not part of a specific category, add it to a file called "GeneralFunctions.lua"
6. If you are unsure where to place the function, add it to a file called "UnsortedFunctions.lua"
"""

  def add_function_to_dict(filedict: dict, function: str, filename: str):
    if filename not in filedict:
      filedict[filename] = []
    filedict[filename].append(function)
    print(f"Added function {function} to {filename}")

  tools = [
    {
      "type": "function",
      "function": {
        "name": "add",
        "description": "Adds a function to a dictionary",
        "parameters": {
          "type": "object",
          "properties": {
            "func": {
              "type": "string",
              "description": "The function to add",
            },
            "fname": {
              "type": "string",
              "description": "The filename to add the function to",
            },
          },
          "required": ["func", "fname"],
        },
      },
    }
  ]

  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": f"Add function to dict: '{function}'"},
    ],
    tools=tools,
    tool_choice="auto",
    temperature=0,
  )

  message = response.choices[0].message

  if message.tool_calls:
    for tool_call in message.tool_calls:
      func_name = tool_call.function.name
      args = json.loads(tool_call.function.arguments)
      if func_name == "add":
        add_function_to_dict(filedict, args["func"], args["fname"])
        return True
  return False
