---@meta
--* GENERATED BY gemini-2.0-flash

---Abandons the quest specified by SetAbandonQuest().<br>
---Calling SetAbandonQuest() triggers a dialog to confirm the user's intention, and the dialog calls AbandonQuest() when the user clicks "accept".<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_AbandonQuest)
function AbandonQuest() end

---Adds a quest to the list of quests being watched with an optional time to watch it.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_AddQuestWatch)
---@param questIndex number The index of the quest in the quest log.
---@param watchTime? number The amount of time to watch the quest in seconds.
function AddQuestWatch(questIndex, watchTime) end

---Returns the name for a Quest ID.<br>
---This API does not require the quest to be in your quest log.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestInfo)
---@param questID number
---@return string title - name of the quest
function C_QuestLog.GetQuestInfo(questID) end

---Returns whether the player can abandon a specific quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CanAbandonQuest)
---@param questID number quest ID of the quest to query, e.g. 5944 for [60G] In Dreams
---@return boolean canAbandon 1 if the player is currently on the specified quest and can abandon it, nil otherwise.
function CanAbandonQuest(questID) end

---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetAbandonQuestItems)
---@return number[] itemIDs
function C_QuestLog.GetAbandonQuestItems() end

---Returns the name of a quest that will be abandoned if AbandonQuest is called.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAbandonQuestName)
---@return string questName - Name of the quest that will be abandoned.
function GetAbandonQuestName() end

---Returns the number of entries in the quest log.<br>
---Includes collapsable zone headers and actual quests.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestLogEntries)
---@return number numEntries Number of entries in the Quest Log, including collapsable zone headers.
---@return number numQuests Number of actual quests in the Quest Log, not counting zone headers.
function GetNumQuestLogEntries() end

---Returns the number of currencies rewarded for a quest in the quest log.<br>
---Returns the number of currencies rewarded for the currently open quest in the quest log, or for the provided questID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestLogRewardCurrencies)
---@param questID? number
---@return number numCurrencies
function GetNumQuestLogRewardCurrencies(questID) end

---Returns the number of tracked quests.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestWatches)
---@return number numWatches
function GetNumQuestWatches() end

---Returns information about a currency token rewarded from the quest currently being viewed in the quest info frame.<br>
---This API only exists in Cata Classic and Classic Era.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestCurrencyInfo)
---@param itemType string The category of the currency to query. Currently "reward" is the only category in use for currencies.
---@param index number The index of the currency to query, in the range [1,GetNumRewardCurrencies()].
---@return string name The localized name of the currency.
---@return string texture The path to the icon texture used for the currency.
---@return number numItems The amount of the currency that will be rewarded.
---@return number quality Indicates the rarity of the currency.
function GetQuestCurrencyInfo(itemType, index) end

---Returns how many levels below you quests and mobs remain "green" (i.e. yield xp).<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestGreenRange)
---@return number range - an integer value, currently up to 12 (at level 60)
function GetQuestGreenRange() end

---Gets the quest log index of a quest being timed.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 9.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestIndexForTimer)
---@param timerId number The ID of a quest timer.
---@return number questIndex The quest log's index of the timed quest.
function GetQuestIndexForTimer(timerId) end

---Gets the quest log index of a watched quest.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 9.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestIndexForWatch)
---@param watchIndex number The index of a quest watch; an integer between 1 and GetNumQuestWatches().
---@return number questIndex The quest log's index of the watched quest.
function GetQuestIndexForWatch(watchIndex) end

---Returns the suggested number of players for a quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogGroupNum)
---@param questID number
---@return number suggestedGroup
function GetQuestLogGroupNum(questID) end

---Returns the current quest log index of a quest by its ID.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogIndexByID)
---@param questID number Unique identifier for each quest.
---@return number The index of the queried quest in the quest log. Returns "0" if a quest with this questID does not exist in the quest log.
function GetQuestLogIndexByID(questID) end

---Returns information about a quest in the player's quest log.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetInfo)
---@param questLogIndex number
---@return QuestInfo? info
function C_QuestLog.GetInfo(questLogIndex) end

---Returns true if the currently loaded quest in the quest window is able to be shared with other players.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogPushable)
---@return boolean? isPushable 1 if the quest can be shared, nil otherwise.
function GetQuestLogPushable() end

---Returns the amount of money required for quest completion.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetRequiredMoney)
---@param questID number? Uses the selected quest if no questID is provided.
---@return number requiredMoney
function C_QuestLog.GetRequiredMoney(questID) end

---Provides information about a currency reward for the quest currently being viewed in the quest log, or of the provided questId.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogRewardCurrencyInfo)
---@param index number The index of the currency to query, in the range of [1,GetNumRewardCurrencies()] or [1, GetNumQuestLogRewardCurrencies()]
---@param questId number? The id of a quest
---@return string name The localized name of the currency
---@return string texture The path to the icon texture used for the currency
---@return number numItems The amount of the currency that will be rewarded
---@return number currencyId The id of the curreny
---@return number quality The quality of the curreny
function GetQuestLogRewardCurrencyInfo(index, questId) end

---Returns a number associated with the QuestLogSelection index.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogSelection)
---@return number questSelected The number for the currently selected quest.
function GetQuestLogSelection() end

---Returns information about a quest in your quest log.<br>
---title, level, suggestedGroup, isHeader, isCollapsed, isComplete, frequency, questID, startEvent, displayQuestID, isOnMap, hasLocalPOI, isTask, isBounty, isStory, isHidden, isScaling = GetQuestLogTitle(questLogIndex)
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogTitle)
---@param questLogIndex number The index of the quest you wish to get information about, between 1 and GetNumQuestLogEntries()'s first return value.
---@return string title The title of the quest, or nil if the index is out of range.
---@return number level The level of the quest.
---@return number suggestedGroup If the quest is designed for more than one player, it is the number of players suggested to complete the quest. Otherwise, it is 0.
---@return boolean isHeader true if the entry is a header, false otherwise.
---@return boolean isCollapsed true if the entry is a collapsed header, false otherwise.
---@return number isComplete 1 if the quest is completed, -1 if the quest is failed, nil otherwise.
---@return number frequency 1 if the quest is a normal quest, LE_QUEST_FREQUENCY_DAILY (2) for daily quests, LE_QUEST_FREQUENCY_WEEKLY (3) for weekly quests.
---@return number questID The quest identification number.
---@return boolean startEvent ?
---@return boolean displayQuestID true if the questID is displayed before the title, false otherwise.
---@return boolean isOnMap ?
---@return boolean hasLocalPOI ?
---@return boolean isTask ?
---@return boolean isBounty ? (true for Legion World Quests; is it true for other WQs?)
---@return boolean isStory ?
---@return boolean isHidden true if the quest is not visible inside the player's quest log.
---@return boolean isScaling ?
function GetQuestLogTitle(questLogIndex) end

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

---Returns all of the quest timers currently in progress.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestTimers)
---@return string ... questTimers Values in seconds of all quest timers currently in progress
function GetQuestTimers() end

---Returns a list of quests the character has completed in its lifetime.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestsCompleted)
---@param table table? If supplied, fills this table with quests. Any other keys will be unchanged.
---@return table questsCompleted The list of completed quests, keyed by quest IDs.
function GetQuestsCompleted(table) end

---Returns the suggested number of players for a quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetSuggestedGroupSize)
---@param questID number
---@return number suggestedGroupSize
function C_QuestLog.GetSuggestedGroupSize(questID) end

---Returns the quest ID currently being tracked, if set. Replaces `GetSuperTrackedQuestID`.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_SuperTrack.GetSuperTrackedQuestID)
---@return number? questID
function C_SuperTrack.GetSuperTrackedQuestID() end

---Returns whether the supplied quest in the quest log is complete.<br>
---This function will only return true if the questID corresponds to a quest in the player's log.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsQuestComplete)
---@param questID number The ID of the quest.
---@return boolean true if the quest is both in the quest log and is complete, false otherwise.
function IsQuestComplete(questID) end

---Returns the watchType associated with a given quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestWatchType)
---@param questID number
---@return Enum.QuestWatchType? watchType
function C_QuestLog.GetQuestWatchType(questID) end

---Returns the watchType associated with a given quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestWatchType)
---@param questID number
---@return Enum.QuestWatchType? watchType
function C_QuestLog.GetQuestWatchType(questID) end

---Returns whether the passed unit is on the passed quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsUnitOnQuest)
---@param questIndex number The index of the quest to check for
---@param unit string UnitId
---@return boolean
function IsUnitOnQuest(questIndex, unit) end

---Returns true if the unit is on the specified quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.IsUnitOnQuest)
---@param unit string UnitId
---@param questID number
---@return boolean isOnQuest
function C_QuestLog.IsUnitOnQuest(unit, questID) end

---Returns WorldMap POI icon information for the given quest.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_QuestPOIGetIconInfo)
---@param questId number you can get this from the quest link or from GetQuestLogTitle(questLogIndex).
---@return boolean completed is the quest completed (the icon is a question mark).
---@return number posX the X position where the icon is shown on the map (between 0 and 1 inclusive).
---@return number posY the Y position where the icon is shown on the map (between 0 and 1 inclusive).
---@return number objective which is sometimes negative and doesn't appear to have anything to do with the quest's actual objectives.
function QuestPOIGetIconInfo(questId) end

---Removes a quest from being watched.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_RemoveQuestWatch)
---@param questIndex number The index of the quest in the quest log.
function RemoveQuestWatch(questIndex) end

---Makes a quest in the quest log the currently selected quest.<br>
---This function is called whenever the user clicks on a quest name in the quest log.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_SelectQuestLogEntry)
---@param questIndex number quest log entry index to select, ascending from 1.
function SelectQuestLogEntry(questIndex) end

---Selects the currently selected quest to be abandoned.<br>
---Quests are selected by calling SelectQuestLogEntry(). After calling this function, you can abandon the quest by calling AbandonQuest().<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetAbandonQuest)
function SetAbandonQuest() end

---Changes the quest ID actively being tracked.<br>
---Replaces `SetSuperTrackedQuestID`.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_SuperTrack.SetSuperTrackedQuestID)
---@param questID number
function C_SuperTrack.SetSuperTrackedQuestID(questID) end

---Exchanges the order of two watched quests.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 6.0.2.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShiftQuestWatches)
---@param id1 number Indices of the quest watches to exchange positions of.
---@param id2 number Indices of the quest watches to exchange positions of.
function ShiftQuestWatches(id1, id2) end

---Sorts watched quests by proximity to the player character.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_SortQuestWatches)
---@return boolean changed # true if any change to the order of watched quests was made, false otherwise.
function SortQuestWatches() end

