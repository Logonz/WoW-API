---@meta

---Returns item details for a loot event.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_LootHistory.GetItem)
---@param itemIdx number Loot history ID
---@return number rollID
---@return string itemLink
---@return number numPlayers Total players eligible for item
---@return boolean isDone
---@return number winnerIdx
---@return boolean isMasterLoot
function C_LootHistory.GetItem(itemIdx) end


---Returns player details for a loot event.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_LootHistory.GetPlayerInfo)
---@param itemIdx number
---@param playerIdx number
---@return string name
---@return string class
---@return number rollType 0 for pass, 1 for need, 2 for greed, 3 for disenchant
---@return number roll
---@return boolean isWinner
---@return boolean isMe
function C_LootHistory.GetPlayerInfo(itemIdx, playerIdx) end

