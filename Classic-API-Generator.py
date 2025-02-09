from openai import OpenAI
import json
import os
import requests
from dotenv import load_dotenv
import threading
from concurrent.futures import ThreadPoolExecutor

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


# https://warcraft.wiki.gg/wiki/World_of_Warcraft_API/Classic
# Get shit here, i just copy the tables.
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


#### Functions ot fetch


def GetData():
  return [
    "/wiki/API_AbandonQuest",
    "/wiki/API_AcceptArenaTeam",
    "/wiki/API_AddQuestWatch",
    "/wiki/API_AddTrackedAchievement",
    "/wiki/API_ArenaTeamDisband",
    "/wiki/API_ArenaTeamInviteByName",
    "/wiki/API_ArenaTeamLeave",
    "/wiki/API_ArenaTeamRoster",
    "/wiki/API_ArenaTeamSetLeaderByName",
    "/wiki/API_ArenaTeamUninviteByName",
    "/wiki/API_BNGetFriendGameAccountInfo",
    "/wiki/API_BNGetFriendInfo",
    "/wiki/API_BNGetFriendInfoByID",
    "/wiki/API_BNGetGameAccountInfo",
    "/wiki/API_BNGetGameAccountInfoByGUID",
    "/wiki/API_BNGetNumFriendGameAccounts",
    "/wiki/API_BuyStableSlot",
    "/wiki/API_C_AreaPoiInfo.GetAreaPOITimeLeft",
    "/wiki/API_C_BarberShop.CycleCharCustomization",
    "/wiki/API_C_BarberShop.GetBarbersChoiceCost",
    "/wiki/API_C_BarberShop.GetCustomizationTypeInfo",
    "/wiki/API_C_BarberShop.IsValidCustomizationType",
    "/wiki/API_C_BarberShop.IsViewingNativeSex",
    "/wiki/API_C_BarberShop.IsViewingVisibleSex",
    "/wiki/API_C_BarberShop.SetPortraitTexture",
    "/wiki/API_C_BattleNet.AreHighResTexturesInstalled",
    "/wiki/API_C_ChatInfo.CanReportPlayer",
    "/wiki/API_C_ChatInfo.ReportServerLag",
    "/wiki/API_C_Container.GetContainerItemGems",
    "/wiki/API_C_Container.IsBagSlotFlagEnabledOnOtherBankBags",
    "/wiki/API_C_Engraving.AddCategoryFilter",
    "/wiki/API_C_Engraving.AddExclusiveCategoryFilter",
    "/wiki/API_C_Engraving.CastRune",
    "/wiki/API_C_Engraving.ClearAllCategoryFilters",
    "/wiki/API_C_Engraving.ClearCategoryFilter",
    "/wiki/API_C_Engraving.ClearExclusiveCategoryFilter",
    "/wiki/API_C_Engraving.EnableEquippedFilter",
    "/wiki/API_C_Engraving.GetCurrentRuneCast",
    "/wiki/API_C_Engraving.GetEngravingModeEnabled",
    "/wiki/API_C_Engraving.GetExclusiveCategoryFilter",
    "/wiki/API_C_Engraving.GetNumRunesKnown",
    "/wiki/API_C_Engraving.GetRuneCategories",
    "/wiki/API_C_Engraving.GetRuneForEquipmentSlot",
    "/wiki/API_C_Engraving.GetRuneForInventorySlot",
    "/wiki/API_C_Engraving.GetRunesForCategory",
    "/wiki/API_C_Engraving.HasCategoryFilter",
    "/wiki/API_C_Engraving.IsEngravingEnabled",
    "/wiki/API_C_Engraving.IsEquipmentSlotEngravable",
    "/wiki/API_C_Engraving.IsEquippedFilterEnabled",
    "/wiki/API_C_Engraving.IsInventorySlotEngravable",
    "/wiki/API_C_Engraving.IsInventorySlotEngravableByCurrentRuneCast",
    "/wiki/API_C_Engraving.IsKnownRuneSpell",
    "/wiki/API_C_Engraving.IsRuneEquipped",
    "/wiki/API_C_Engraving.RefreshRunesList",
    "/wiki/API_C_Engraving.SetEngravingModeEnabled",
    "/wiki/API_C_Engraving.SetSearchFilter",
    "/wiki/API_C_GameRules.IsHardcoreActive",
    "/wiki/API_C_GameRules.IsSelfFoundAllowed",
    "/wiki/API_C_Item.IsDressableItem",
    "/wiki/API_C_LootHistory.GetItem",
    "/wiki/API_C_LootHistory.GetPlayerInfo",
    "/wiki/API_C_Macro.GetNumIcons",
    "/wiki/API_C_Map.GetBountySetIDForMap",
    "/wiki/API_C_PlayerInfo.IsXPUserDisabled",
    "/wiki/API_C_PvP.GetHolidayBGLossRewards",
    "/wiki/API_C_PvP.GetHolidayBGRewards",
    "/wiki/API_C_PvP.GetRandomBGLossRewards",
    "/wiki/API_C_PvP.GetWorldPvPWaitTime",
    "/wiki/API_C_QuestLog.GetQuestInfo",
    "/wiki/API_C_Reforge.CloseReforge",
    "/wiki/API_C_Reforge.GetDestinationReforgeStats",
    "/wiki/API_C_Reforge.GetNumReforgeOptions",
    "/wiki/API_C_Reforge.GetReforgeItemInfo",
    "/wiki/API_C_Reforge.GetReforgeItemStats",
    "/wiki/API_C_Reforge.GetReforgeOptionInfo",
    "/wiki/API_C_Reforge.GetSourceReforgeStats",
    "/wiki/API_C_Reforge.ReforgeItem",
    "/wiki/API_C_Reforge.SetReforgeFromCursorItem",
    "/wiki/API_C_Seasons.GetActiveSeason",
    "/wiki/API_C_Seasons.HasActiveSeason",
    "/wiki/API_C_StorePublic.HasPurchaseableProducts",
    "/wiki/API_C_UIWidgetManager.GetTextureWithStateVisualizationInfo",
    "/wiki/API_CanAbandonQuest",
    "/wiki/API_CanSendAuctionQuery",
    "/wiki/API_CancelSell",
    "/wiki/API_CancelTrackingBuff",
    "/wiki/API_CastingInfo",
    "/wiki/API_ChannelInfo",
    "/wiki/API_ClickAuctionSellItemButton",
    "/wiki/API_ClickStablePet",
    "/wiki/API_CloseAuctionHouse",
    "/wiki/API_CloseBankFrame",
    "/wiki/API_ClosePetStables",
    "/wiki/API_CloseTradeSkill",
    "/wiki/API_CollapseFactionHeader",
    "/wiki/API_CollapseSkillHeader",
    "/wiki/API_CollapseTrainerSkillLine",
    "/wiki/API_ConfirmBarbersChoice",
    "/wiki/API_ConfirmBinder",
    "/wiki/API_ConfirmPetUnlearn",
    "/wiki/API_ConvertToParty",
    "/wiki/API_ConvertToRaid",
    "/wiki/API_CursorCanGoInSlot",
    "/wiki/API_DeclineArenaTeam",
    "/wiki/API_DoTradeSkill",
    "/wiki/API_DoesSpellExist",
    "/wiki/API_ExpandCurrencyList",
    "/wiki/API_ExpandFactionHeader",
    "/wiki/API_ExpandSkillHeader",
    "/wiki/API_ExpandTradeSkillSubClass",
    "/wiki/API_ExpandTrainerSkillLine",
    "/wiki/API_FactionToggleAtWar",
    "/wiki/API_FillLocalizedClassList",
    "/wiki/API_GMSubmitBug",
    "/wiki/API_GMSubmitSuggestion",
    "/wiki/API_GetAbandonQuestItems",
    "/wiki/API_GetAbandonQuestName",
    "/wiki/API_GetActiveTalentGroup",
    "/wiki/API_GetArenaTeam",
    "/wiki/API_GetArenaTeamIndexBySize",
    "/wiki/API_GetArenaTeamRosterInfo",
    "/wiki/API_GetArmorPenetration",
    "/wiki/API_GetAuctionItemBattlePetInfo",
    "/wiki/API_GetAuctionItemInfo",
    "/wiki/API_GetAuctionItemLink",
    "/wiki/API_GetAuctionItemSubClasses",
    "/wiki/API_GetAuctionItemTimeLeft",
    "/wiki/API_GetAuctionSellItemInfo",
    "/wiki/API_GetBackpackCurrencyInfo",
    "/wiki/API_GetBattlefieldFlagPosition",
    "/wiki/API_GetBattlefieldInstanceInfo",
    "/wiki/API_GetBattlefieldStatInfo",
    "/wiki/API_GetCompanionCooldown",
    "/wiki/API_GetCraftDescription",
    "/wiki/API_GetCraftDisplaySkillLine",
    "/wiki/API_GetCraftInfo",
    "/wiki/API_GetCraftItemLink",
    "/wiki/API_GetCraftName",
    "/wiki/API_GetCraftNumReagents",
    "/wiki/API_GetCraftReagentInfo",
    "/wiki/API_GetCraftReagentItemLink",
    "/wiki/API_GetCraftRecipeLink",
    "/wiki/API_GetCraftSkillLine",
    "/wiki/API_GetCraftSpellFocus",
    "/wiki/API_GetCurrencyInfo",
    "/wiki/API_GetCurrencyLink",
    "/wiki/API_GetCurrencyListInfo",
    "/wiki/API_GetCurrencyListSize",
    "/wiki/API_GetCurrentLevelSpells",
    "/wiki/API_GetCurrentResolution",
    "/wiki/API_GetEclipseDirection",
    "/wiki/API_GetExpertisePercent",
    "/wiki/API_GetFactionInfo",
    "/wiki/API_GetFactionInfoByID",
    "/wiki/API_GetFirstBagBankSlotIndex",
    "/wiki/API_GetFirstTradeSkill",
    "/wiki/API_GetGuildFactionInfo",
    "/wiki/API_GetInspectPVPRankProgress",
    "/wiki/API_GetInventoryItemGems",
    "/wiki/API_GetInviteReferralInfo",
    "/wiki/API_GetItemStats",
    "/wiki/API_GetMerchantItemInfo",
    "/wiki/API_GetNextStableSlotCost",
    "/wiki/API_GetNextTalentLevel",
    "/wiki/API_GetNumAuctionItems",
    "/wiki/API_GetNumBattlefieldStats",
    "/wiki/API_GetNumBattlefields",
    "/wiki/API_GetNumCrafts",
    "/wiki/API_GetNumFactions",
    "/wiki/API_GetNumQuestLogEntries",
    "/wiki/API_GetNumQuestLogRewardCurrencies",
    "/wiki/API_GetNumQuestWatches",
    "/wiki/API_GetNumRewardCurrencies",
    "/wiki/API_GetNumSkillLines",
    "/wiki/API_GetNumSpellTabs",
    "/wiki/API_GetNumStableSlots",
    "/wiki/API_GetNumTalentGroups",
    "/wiki/API_GetNumTalentTabs",
    "/wiki/API_GetNumTalents",
    "/wiki/API_GetNumTrackedAchievements",
    "/wiki/API_GetNumTradeSkills",
    "/wiki/API_GetOwnerAuctionItems",
    "/wiki/API_GetPVPLastWeekStats",
    "/wiki/API_GetPVPRankInfo",
    "/wiki/API_GetPVPRankProgress",
    "/wiki/API_GetPVPThisWeekStats",
    "/wiki/API_GetPetHappiness",
    "/wiki/API_GetPetLoyalty",
    "/wiki/API_GetPetTrainingPoints",
    "/wiki/API_GetPrimaryTalentTree",
    "/wiki/API_GetQuestCurrencyInfo",
    "/wiki/API_GetQuestGreenRange",
    "/wiki/API_GetQuestIndexForTimer",
    "/wiki/API_GetQuestIndexForWatch",
    "/wiki/API_GetQuestLogGroupNum",
    "/wiki/API_GetQuestLogIndexByID",
    "/wiki/API_GetQuestLogIsAutoComplete",
    "/wiki/API_GetQuestLogPushable",
    "/wiki/API_GetQuestLogRequiredMoney",
    "/wiki/API_GetQuestLogRewardCurrencyInfo",
    "/wiki/API_GetQuestLogSelection",
    "/wiki/API_GetQuestLogTitle",
    "/wiki/API_GetQuestTagInfo",
    "/wiki/API_GetQuestTimers",
    "/wiki/API_GetQuestsCompleted",
    "/wiki/API_GetRuneType",
    "/wiki/API_GetScreenResolutions",
    "/wiki/API_GetSelectedBattlefield",
    "/wiki/API_GetSelectedSkill",
    "/wiki/API_GetSelectedStablePet",
    "/wiki/API_GetSkillLineInfo",
    "/wiki/API_GetSpellAutocast",
    "/wiki/API_GetSpellBookItemInfo",
    "/wiki/API_GetSpellBookItemName",
    "/wiki/API_GetSpellBookItemTexture",
    "/wiki/API_GetSpellCharges",
    "/wiki/API_GetSpellCooldown",
    "/wiki/API_GetSpellCount",
    "/wiki/API_GetSpellDescription",
    "/wiki/API_GetSpellInfo",
    "/wiki/API_GetSpellLink",
    "/wiki/API_GetSpellLossOfControlCooldown",
    "/wiki/API_GetSpellPowerCost",
    "/wiki/API_GetSpellTabInfo",
    "/wiki/API_GetSpellTexture",
    "/wiki/API_GetStablePetFoodTypes",
    "/wiki/API_GetStablePetInfo",
    "/wiki/API_GetSuggestedGroupNum",
    "/wiki/API_GetSuperTrackedQuestID",
    "/wiki/API_GetTalentGroupRole",
    "/wiki/API_GetTalentPrereqs",
    "/wiki/API_GetTalentTabInfo",
    "/wiki/API_GetTalentTreeRoles",
    "/wiki/API_GetTrackedAchievements",
    "/wiki/API_GetTrackingTexture",
    "/wiki/API_GetTradeSkillDescription",
    "/wiki/API_GetTradeSkillInfo",
    "/wiki/API_GetTradeSkillInvSlotFilter",
    "/wiki/API_GetTradeSkillInvSlots",
    "/wiki/API_GetTradeSkillItemLink",
    "/wiki/API_GetTradeSkillItemStats",
    "/wiki/API_GetTradeSkillLine",
    "/wiki/API_GetTradeSkillListLink",
    "/wiki/API_GetTradeSkillNumMade",
    "/wiki/API_GetTradeSkillNumReagents",
    "/wiki/API_GetTradeSkillReagentInfo",
    "/wiki/API_GetTradeSkillReagentItemLink",
    "/wiki/API_GetTradeSkillRecipeLink",
    "/wiki/API_GetTradeSkillSelectionIndex",
    "/wiki/API_GetTradeSkillSubClassFilter",
    "/wiki/API_GetTradeSkillSubClasses",
    "/wiki/API_GetTradeSkillTools",
    "/wiki/API_GetTradeskillRepeatCount",
    "/wiki/API_GetUnspentTalentPoints",
    "/wiki/API_GetWatchedFactionInfo",
    "/wiki/API_HasInspectHonorData",
    "/wiki/API_HasPetSpells",
    "/wiki/API_InActiveBattlefield",
    "/wiki/API_InviteUnit",
    "/wiki/API_IsAttackSpell",
    "/wiki/API_IsAuctionSortReversed",
    "/wiki/API_IsCurrentSpell",
    "/wiki/API_IsFactionInactive",
    "/wiki/API_IsPassiveSpell",
    "/wiki/API_IsPlayerAttacking",
    "/wiki/API_IsQuestComplete",
    "/wiki/API_IsQuestHardWatched",
    "/wiki/API_IsQuestWatched",
    "/wiki/API_IsRatedBattleground",
    "/wiki/API_IsSpellInRange",
    "/wiki/API_IsTrackedAchievement",
    "/wiki/API_IsTradeSkillLinked",
    "/wiki/API_IsTrainerServiceLearnSpell",
    "/wiki/API_IsUnitOnQuest",
    "/wiki/API_IsUnitOnQuestByQuestID",
    "/wiki/API_IsUsableSpell",
    "/wiki/API_LeaveParty",
    "/wiki/API_PetAbandon",
    "/wiki/API_PetCanBeRenamed",
    "/wiki/API_PetRename",
    "/wiki/API_PickupCurrency",
    "/wiki/API_PickupSpell",
    "/wiki/API_PickupSpellBookItem",
    "/wiki/API_PickupStablePet",
    "/wiki/API_PlaceAuctionBid",
    "/wiki/API_PostAuction",
    "/wiki/API_QueryAuctionItems",
    "/wiki/API_QuestPOIGetIconInfo",
    "/wiki/API_RemoveQuestWatch",
    "/wiki/API_RemoveTrackedAchievement",
    "/wiki/API_RequestInspectHonorData",
    "/wiki/API_RequestInviteFromUnit",
    "/wiki/API_SelectQuestLogEntry",
    "/wiki/API_SetAbandonQuest",
    "/wiki/API_SetActiveTalentGroup",
    "/wiki/API_SetCurrencyBackpack",
    "/wiki/API_SetCurrencyUnused",
    "/wiki/API_SetFactionActive",
    "/wiki/API_SetFactionInactive",
    "/wiki/API_SetPetStablePaperdoll",
    "/wiki/API_SetPrimaryTalentTree",
    "/wiki/API_SetScreenResolution",
    "/wiki/API_SetSelectedAuctionItem",
    "/wiki/API_SetSelectedBattlefield",
    "/wiki/API_SetSelectedSkill",
    "/wiki/API_SetSuperTrackedQuestID",
    "/wiki/API_SetTradeSkillInvSlotFilter",
    "/wiki/API_SetTradeSkillItemLevelFilter",
    "/wiki/API_SetTradeSkillSubClassFilter",
    "/wiki/API_SetWatchedFactionIndex",
    "/wiki/API_ShiftQuestWatches",
    "/wiki/API_ShouldKnowUnitHealth",
    "/wiki/API_ShowCloak",
    "/wiki/API_ShowHelm",
    "/wiki/API_ShowingCloak",
    "/wiki/API_ShowingHelm",
    "/wiki/API_SortAuctionItems",
    "/wiki/API_SortAuctionSetSort",
    "/wiki/API_SortQuestWatches",
    "/wiki/API_StartAuction",
    "/wiki/API_StopTradeSkillRepeat",
    "/wiki/API_UnitAttackBothHands",
    "/wiki/API_UnitAura",
    "/wiki/API_UnitBuff",
    "/wiki/API_UnitCharacterPoints",
    "/wiki/API_UnitDebuff",
    "/wiki/API_UnitDefense",
    "/wiki/API_UnitInPhase",
    "/wiki/API_UnitIsCivilian",
    "/wiki/API_UnitPVPRank",
    "/wiki/API_UnitRangedAttack",
    "/wiki/API_UnitResistance",
  ]


if __name__ == "__main__":
  main()
