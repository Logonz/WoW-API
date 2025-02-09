---@meta

C_LootHistory = {}

---Retrieves information about a specific item in the loot history.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_LootHistory.GetItem)
---@param itemIndex number
---@return number itemID
---@return string playerGUID
---@return number rollType
---@return number roll
---@return boolean hidden
function C_LootHistory.GetItem(itemIndex) end

---Get information about a player's role in the loot history. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_LootHistory.GetPlayerInfo)
---@param lootHistoryID number
---@param playerIndex number
---@return string name
---@return boolean isMasterLoot
---@return number role
function C_LootHistory.GetPlayerInfo(lootHistoryID, playerIndex) end