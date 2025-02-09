---@meta

---Abandons the quest specified by SetAbandonQuest() after a confirmation dialog.
---[Documentation](https://warcraft.wiki.gg/wiki/API_AbandonQuest)
function AbandonQuest() end


---Adds a quest to the list of quests being watched with an optional time to watch it.
---[Documentation](https://warcraft.wiki.gg/wiki/API_AddQuestWatch)
---@param questIndex number The index of the quest in the quest log.
---@param watchTime? number The amount of time to watch the quest in seconds.
function AddQuestWatch(questIndex, watchTime) end


---Returns the name for a given Quest ID.
---This API does not require the quest to be in your quest log. If the name is still an empty string after being queried, then the quest is assumed to have been removed.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestInfo)
---@param questID number
---@return string title The name of the quest
function C_QuestLog.GetQuestInfo(questID) end


---Returns whether the player can abandon a specific quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CanAbandonQuest)
---@param questID number The ID of the quest to query.
---@return boolean canAbandon Returns true if the player can abandon the quest; false otherwise.
function CanAbandonQuest(questID) end


---Returns a list of item IDs associated with quests that are set to be abandoned. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetAbandonQuestItems)
---@return number[] itemIDs
function C_QuestLog.GetAbandonQuestItems() end


---Returns the name of a quest that will be abandoned if AbandonQuest is called.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAbandonQuestName)
---@return string questName Name of the quest that will be abandoned.
function GetAbandonQuestName() end


---Returns the number of currencies rewarded for a specific quest in the quest log or the current quest if no ID is provided.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestLogRewardCurrencies)
---@param questID? number
---@return number numCurrencies
function GetNumQuestLogRewardCurrencies(questID) end


---Returns the number of entries in the quest log, including collapsable zone headers and actual quests. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestLogEntries)
---@return number numEntries Number of entries in the Quest Log, including collapsable zone headers.
---@return number numQuests Number of actual quests in the Quest Log, not counting zone headers.
function GetNumQuestLogEntries() end


---Returns the number of tracked quests.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestWatches)
---@return number numWatches
function GetNumQuestWatches() end


---Returns the number of levels below your character that quests and mobs remain "green," allowing them to yield experience.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestGreenRange)
---@return number range an integer value, currently up to 12 at level 60
function GetQuestGreenRange() end


---Returns the suggested number of players for a quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogGroupNum)
---@param questID number
---@return number suggestedGroup
function GetQuestLogGroupNum(questID) end


---Returns the current quest log index of a quest by its ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogIndexByID)
---@param questID number Unique identifier for each quest.
---@return number questLogIndex The index of the queried quest in the quest log. Returns "0" if a quest with this questID does not exist in the quest log.
function GetQuestLogIndexByID(questID) end


---Gets the quest log index of a quest being timed.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestIndexForTimer)
---@param timerId number The ID of a quest timer.
---@return number questIndex The quest log's index of the timed quest.
function GetQuestIndexForTimer(timerId) end


---Gets the quest log index of a watched quest.
---This function can return nil for valid watchIndex values if the watched quest isn't cached.
---[Documentation](https://warcraft.wiki.gg/wiki/GetQuestIndexForWatch)
---@param watchIndex number The index of a quest watch; an integer between 1 and GetNumQuestWatches().
---@return number|nil questIndex The quest log's index of the watched quest.
function GetQuestIndexForWatch(watchIndex) end


---Returns information about a quest in the player's quest log.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetInfo)
---@param questLogIndex number
---@return QuestInfo? info
function C_QuestLog.GetInfo(questLogIndex) end


---Returns the amount of money required for quest completion.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetRequiredMoney)
---@param questID? number Uses the selected quest if no questID is provided.
---@return number requiredMoney
function C_QuestLog.GetRequiredMoney(questID) end


---Returns true if the currently loaded quest in the quest window can be shared with other players.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogPushable)
---@return boolean? isPushable 1 if the quest can be shared, nil otherwise.
function GetQuestLogPushable() end


---Returns information about a currency token rewarded from the quest currently being viewed in the quest info frame.
---Does not work for quests viewed from the player's quest log; use GetQuestLogRewardCurrencyInfo instead.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestCurrencyInfo)
---@param itemType string The category of the currency to query. Currently "reward" is the only category in use for currencies.
---@param index number The index of the currency to query, in the range [1, GetNumRewardCurrencies()].
---@return string name The localized name of the currency.
---@return string texture The path to the icon texture used for the currency.
---@return number numItems The amount of the currency that will be rewarded.
---@return number quality Indicates the rarity of the currency.
function GetQuestCurrencyInfo(itemType, index) end


---Returns a number associated with the QuestLogSelection index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogSelection)
---@return number questSelected The number for the currently selected quest.
function GetQuestLogSelection() end


---Returns all of the quest timers currently in progress.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestTimers)
---@return string[] questTimers Values in seconds of all quest timers currently in progress
function GetQuestTimers() end


---Returns a list of quests the character has completed in its lifetime.
---If a table is supplied, it fills that table with quests while keeping other keys unchanged.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestsCompleted)
---@param table? table If supplied, fills this table with quests.
---@return table questsCompleted The list of completed quests, keyed by quest IDs.
function GetQuestsCompleted(table) end


---Provides information about a currency reward for the quest currently being viewed in the quest log, or of the provided questId.
---If no questId is provided, it works only for a quest currently viewed in the quest log. Requires quest reward data to be loaded.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogRewardCurrencyInfo)
---@param index number The index of the currency to query
---@param questId? number The id of a quest
---@return string name The localized name of the currency
---@return string texture The path to the icon texture used for the currency
---@return number numItems The amount of the currency that will be rewarded
---@return number currencyId The id of the currency
---@return number quality The quality of the currency
function C_QuestLog.GetQuestLogRewardCurrencyInfo(index, questId) end


---Retrieves tag information about the quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestTagInfo)
---@param questID number The ID of the quest to retrieve the tag info for.
---@return number|nil tagID The tag ID, or nil if quest is not tagged.
---@return string|nil tagName Human readable representation of the tag ID, or nil if quest is not tagged.
---@return number|nil worldQuestType Type of world quest, or nil if not a world quest.
---@return number rarity The rarity of the quest (used for world quests).
---@return boolean isElite Whether this is an elite quest (used for world quests).
---@return any tradeskillLineIndex Tradeskill ID if this is a profession quest (used to determine which profession icon to display for world quests).
---@return any displayTimeLeft The remaining display time, may need further documentation for exact type.
function GetQuestTagInfo(questID) end


---Returns information about a quest in your quest log.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogTitle)
---@param questLogIndex number The index of the quest you wish to get information about.
---@return string|nil title The title of the quest, or nil if the index is out of range.
---@return number level The level of the quest.
---@return number suggestedGroup Suggested group size for the quest.
---@return boolean isHeader True if the entry is a header.
---@return boolean isCollapsed True if the entry is a collapsed header.
---@return number|nil isComplete Status indicating if the quest is complete, failed, or incomplete.
---@return number frequency Frequency category of the quest.
---@return number questID The identifier of the quest.
---@return boolean startEvent Whether the quest starts an event.
---@return boolean displayQuestID If questID is displayed before the title.
---@return boolean isOnMap If the quest is on the map.
---@return boolean hasLocalPOI If the quest has a local point of interest.
---@return boolean isTask True if the quest is a task.
---@return boolean isBounty True if the quest is a bounty.
---@return boolean isStory True if the quest is part of a storyline.
---@return boolean isHidden True if the quest is not visible in quest log.
---@return boolean isScaling If the quest scales with the player.
function GetQuestLogTitle(questLogIndex) end


---Returns the suggested number of players for a quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetSuggestedGroupSize)
---@param questID number
---@return number suggestedGroupSize
function C_QuestLog.GetSuggestedGroupSize(questID) end


---Returns the quest ID currently being tracked, if set.
---Replaces `GetSuperTrackedQuestID`.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_SuperTrack.GetSuperTrackedQuestID)
---@return number? questID
function C_SuperTrack.GetSuperTrackedQuestID() end


---Returns the watchType associated with a given quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestWatchType)
---@param questID number
---@return Enum.QuestWatchType? watchType
function C_QuestLog.GetQuestWatchType(questID) end


---Returns whether a quest in the quest log is complete.
---This only returns true if the quest is in the log and complete; if already completed, it returns false.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsQuestComplete)
---@param questID number - The ID of the quest.
---@return boolean isComplete - true if the quest is both in the quest log and is complete, false otherwise.
function IsQuestComplete(questID) end


---Returns the watchType associated with a given quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestWatchType)
---@param questID number
---@return Enum.QuestWatchType? watchType
function C_QuestLog.GetQuestWatchType(questID) end


---Determines if a specified unit is currently undertaking a specified quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsUnitOnQuest)
---@param questIndex number The index of the quest to check for
---@param unit string UnitId representing the unit, such as "player"
---@return boolean onQuest True if the unit is on the quest, false otherwise
function IsUnitOnQuest(questIndex, unit) end


---Returns true if the unit is on the specified quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.IsUnitOnQuest)
---@param unit string @UnitId
---@param questID number
---@return boolean isOnQuest
function C_QuestLog.IsUnitOnQuest(unit, questID) end


---Removes a quest from being watched.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RemoveQuestWatch)
---@param questIndex number The index of the quest in the quest log.
function RemoveQuestWatch(questIndex) end


---Returns WorldMap POI icon information for the given quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_QuestPOIGetIconInfo)
---@param questId number
---@return boolean completed Indicates whether the quest is completed
---@return number posX The X position on the map (between 0 and 1)
---@return number posY The Y position on the map (between 0 and 1)
---@return number objective An identifier, sometimes negative, unrelated to quest's actual objectives
function QuestPOIGetIconInfo(questId) end


---Selects the currently selected quest to be abandoned.
---Quests are selected by calling SelectQuestLogEntry().<br>After calling this function, you can abandon the quest by calling AbandonQuest().
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetAbandonQuest)
function SetAbandonQuest() end


---Makes a quest in the quest log the currently selected quest.
---This function is called whenever the user clicks on a quest name in the quest log. It is necessary to call this function to allow other API functions that do not take a questIndex argument to return information about specific quests.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SelectQuestLogEntry)
---@param questIndex number Quest log entry index to select, ascending from 1.
function SelectQuestLogEntry(questIndex) end


---! DRAFT - NEEDS REVIEW
---Sets the super tracked quest ID. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSuperTrackedQuestID)
---@param questID number
function SetSuperTrackedQuestID(questID) end

---! DRAFT - NEEDS REVIEW
---Changes the watch state of the current quests in the quest log.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShiftQuestWatches)
function C_ShiftQuestWatches() end

---! DRAFT - NEEDS REVIEW
---Sets the quest watches to be sorted by priority.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SortQuestWatches)
function SortQuestWatches() end

