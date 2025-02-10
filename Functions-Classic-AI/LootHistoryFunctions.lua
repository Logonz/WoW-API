---@meta
--* GENERATED BY gemini-2.0-flash

---Returns item details for a loot event.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_LootHistory.GetItem)
---@param itemIdx number Loot history ID
---@return number rollID
---@return string itemLink
---@return number numPlayers Total players eligible for item
---@return boolean isDone
---@return number winnerIdx See C_LootHistory.GetPlayerInfo
---@return boolean isMasterLoot
function C_LootHistory.GetItem(itemIdx) end

---Returns player details for a loot event.<br>
---name, class, rollType, roll, isWinner, isMe = C_LootHistory.GetPlayerInfo(itemIdx, playerIdx)
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_LootHistory.GetPlayerInfo)
---@param itemIdx number See C_LootHistory.GetItem
---@return string name
---@return string class
---@return number rollType (0:pass, 1:need, 2:greed, 3:disenchant)
---@return number roll
---@return boolean isWinner
---@return boolean isMe
function C_LootHistory.GetPlayerInfo(itemIdx) end

