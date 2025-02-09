---@meta

---Determines if the given item is dressable.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Item.IsDressableItem)
---@param itemInfo number|string @Item information specified as either an item ID or item link.
---@return boolean result @True if the item is dressable, false otherwise.
function C_Item.IsDressableItem(itemInfo) end


---Returns item ids of the gems socketed in the item in the specified inventory slot.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetInventoryItemGems)
---@param invSlot number The inventory slot index to query.
---@return number gem1 Item ID of the first gem.
---@return number gem2 Item ID of the second gem.
---@return number gem3 Item ID of the third gem.
function GetInventoryItemGems(invSlot) end


---Returns a table of stats for an item, omitting the effects of any enchantments or gems.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetItemStats)
---@param itemLink string An item link for which to get stats.
---@param statTable? table<string, number> An optional table to be filled with stats; if omitted, a new table is returned.
---@return table<string, number> stats A table of item stats.
function GetItemStats(itemLink, statTable) end

