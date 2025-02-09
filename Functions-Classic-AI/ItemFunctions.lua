---@meta

C_Item = {}

---Checks if the specified item can be dressed.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Item.IsDressableItem)
---@param itemInfo ItemInfo
---@return boolean isDressable
function C_Item.IsDressableItem(itemInfo) end

---Returns the gem item IDs of up to four gem sockets for the item in the specified inventory slot. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetInventoryItemGems)
---@param unit string
---@param slot number
---@return number gemID1
---@return number gemID2
---@return number gemID3
---@return number gemID4
function GetInventoryItemGems(unit, slot) end


---Returns a table containing specified item statistics.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetItemStats)
---@param itemLink string
---@param statTable? table
---@return table stats
function GetItemStats(itemLink, statTable) end
