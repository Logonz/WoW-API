---@meta

C_QuestLog = {}

---Abandons the currently tracked quest. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_AbandonQuest)
function AbandonQuest() end


---! DRAFT - NEEDS REVIEW
---Adds a quest to the quest watch list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_AddQuestWatch)
---@param questIndex number
---@param watchType? QuestWatchType
---@return boolean success
function AddQuestWatch(questIndex, watchType) end


---Retrieves detailed information about a specific quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.GetQuestInfo)
---@param questID number
---@return string title
---@return number level
---@return boolean isTrivial
function C_QuestLog.GetQuestInfo(questID) end

---Determines if a quest can be abandoned by the player.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CanAbandonQuest)
---@param questID number
---@return boolean canAbandon
function CanAbandonQuest(questID) end

---Gets the items associated with an abandoned quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAbandonQuestItems)
---@return string items
function GetAbandonQuestItems() end

---Returns the name of the quest that is marked to be abandoned.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetAbandonQuestName)
---@return string? questName
function GetAbandonQuestName() end

---Returns the number of quest log entries. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestLogEntries)
---@return number numEntries
---@return number numQuests
function GetNumQuestLogEntries() end

---Returns the number of reward currencies for a quest in the quest log.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestLogRewardCurrencies)
---@param questID number
---@return number numRewardCurrencies
function GetNumQuestLogRewardCurrencies(questID) end


---Get the number of quests currently being watched.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumQuestWatches)
---@return number numQuestWatches
function GetNumQuestWatches() end


---! DRAFT - NEEDS REVIEW  
---Returns information about a specific currency required for a quest.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestCurrencyInfo)  
---@param type string  
---@param index number  
---@return string name  
---@return string texture  
---@return number numItems  
---@return number currencyID  
function GetQuestCurrencyInfo(type, index) end

---Returns the range within which quests appear green.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestGreenRange)
---@return number range
function GetQuestGreenRange() end


---! DRAFT - NEEDS REVIEW
---Returns the index of the quest associated with a given timer.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestIndexForTimer)
---@param timerID number
---@return number questIndex
function GetQuestIndexForTimer(timerID) end


---Retrieves the quest index for a specified watch slot.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestIndexForWatch)
---@param watchSlot number The watch slot index.
---@return number index Quest index.
function GetQuestIndexForWatch(watchSlot) end


---Returns the suggested group number for a quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogGroupNum)
---@param questID number
---@return number suggestedGroupNum
function GetQuestLogGroupNum(questID) end



---Returns the quest log index for a given quest ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogIndexByID)
---@param questID number
---@return number questLogIndex
function GetQuestLogIndexByID(questID) end


---Determine if a quest in the quest log is set to automatically complete.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogIsAutoComplete)
---@param questID number
---@return boolean isAutoComplete
function GetQuestLogIsAutoComplete(questID) end

---Determines if quests in the quest log can be shared with other players.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogPushable)
---@return boolean arePushable
function GetQuestLogPushable() end

---Returns the amount of money required to complete a specific quest. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogRequiredMoney)
---@param questIndex number
---@return number requiredMoney
function GetQuestLogRequiredMoney(questIndex) end

---Retrieves information about reward currency for a specific quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogRewardCurrencyInfo)
---@param currencyIndex number
---@param questID number
---@return string name
---@return string texture
---@return number amount
---@return number currencyID
function GetQuestLogRewardCurrencyInfo(currencyIndex, questID) end

---Returns the index of the currently selected quest in the quest log.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetQuestLogSelection)
---@return number index
function GetQuestLogSelection() end


---Returns the title and other details about a specific quest in the quest log.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestLogTitle)
---@param questIndex number
---@return string questLogTitleText
---@return boolean level
---@return boolean suggestedGroup
---@return boolean isHeader
---@return boolean isCollapsed
---@return boolean isComplete
---@return number frequency
---@return boolean isTracked
---@return number questID
---@return boolean hasLocalPOI
---@return boolean isTask
function GetQuestLogTitle(questIndex) end


---Returns the tag information for a quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestTagInfo)
---@param questID number
---@return string tag
---@return string tagID
function GetQuestTagInfo(questID) end

---Returns the time remaining for each active quest with a timer.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetQuestTimers)
---@return number[] questTimers 
function GetQuestTimers() end

---Returns a table containing all completed quests for the player. 
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetQuestsCompleted)
---@return table completedQuests A table where keys are quest IDs of completed quests
function GetQuestsCompleted() end

---! DRAFT - NEEDS REVIEW
---Returns the suggested number of players for a quest or dungeon.
---@param questID number
---@return number suggestedGroupNum
function GetSuggestedGroupNum(questID) end

---Returns the quest ID for the super tracked quest.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetSuperTrackedQuestID)
---@return number questID
function GetSuperTrackedQuestID() end

---Checks if a specific quest is complete.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsQuestComplete)
---@param questID number
---@return boolean isComplete
function IsQuestComplete(questID) end

---Checks if a quest is being hard-watched.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsQuestHardWatched)
---@param questID number
---@return boolean isHardWatched
function IsQuestHardWatched(questID) end

---Checks if a quest is currently being watched.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsQuestWatched)
---@param questIndex number
---@return boolean isWatched
function IsQuestWatched(questIndex) end

---Checks if a unit is on a specific quest.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsUnitOnQuest)  
---@param questID number
---@param unit string
---@return boolean onQuest
function IsUnitOnQuest(questID, unit) end

---Checks if a unit is on a quest by the quest ID.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsUnitOnQuestByQuestID)  
---@param questID number The ID of the quest.  
---@param unit string The unit to check, typically "player".  
---@return boolean isOnQuest Indicates if the unit is on the specified quest.  
function IsUnitOnQuestByQuestID(questID, unit) end

---! DRAFT - NEEDS REVIEW
---Retrieves icon information for a quest point of interest.
---@param index number
---@return number x
---@return number y
---@return number icon
---@return number objectType
---@return number scale
---@return boolean alpha
function QuestPOIGetIconInfo(index) end

---Removes a quest from the quest watch list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RemoveQuestWatch)
---@param watchIndex number The index of the quest in the quest watch list
function RemoveQuestWatch(watchIndex) end

---Selects a quest log entry.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SelectQuestLogEntry)
---@param selectedIndex number
function SelectQuestLogEntry(selectedIndex) end

---Abandon the currently tracked quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetAbandonQuest)
function SetAbandonQuest() end


---Sets the currently super tracked quest to the specified quest ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSuperTrackedQuestID)
---@param questID number
function SetSuperTrackedQuestID(questID) end



---! DRAFT - NEEDS REVIEW
---Adjusts the order of watched quests in the quest log.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShiftQuestWatches)
---@param startQuestWatchIndex number
---@param endQuestWatchIndex number
function ShiftQuestWatches(startQuestWatchIndex, endQuestWatchIndex) end



---! DRAFT - NEEDS REVIEW
---Sorts the quest watches.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_QuestLog.SortQuestWatches)
---@param backwards boolean
---@param reindex boolean
function C_QuestLog.SortQuestWatches(backwards, reindex) end
