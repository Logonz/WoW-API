---@meta

C_Reforge = {}

---Closes the reforging window.
function C_Reforge.CloseReforge() end

---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetDestinationReforgeStats)
---@param baseStats ReforgeStats Item's initial stats before reforging
---@param reforgeID number Identifier of the reforge operation
---@return ReforgeStats statValues Modified stat values after applying reforge
function C_Reforge.GetDestinationReforgeStats(baseStats, reforgeID) end

---Returns the number of reforge options available.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetNumReforgeOptions)
---@return number numReforgeOptions
function C_Reforge.GetNumReforgeOptions() end

---! DRAFT - NEEDS REVIEW
---Retrieves information about a specified reforge item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeItemInfo)
---@return number itemID
---@return string itemName
---@return string itemLink
function C_Reforge.GetReforgeItemInfo() end


---Returns the reforge item stats for a given item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeItemStats)
---@param itemID number The ID of the item to query stats for.
---@return table stats A table of the reforge item stats.
function C_Reforge.GetReforgeItemStats(itemID) end


---Retrieves information about a specific reforge option.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeOptionInfo)
---@param optionIndex number
---@return number reforgeID
---@return string name
---@return number itemLevelRequirement
function C_Reforge.GetReforgeOptionInfo(optionIndex) end

---Returns the source reforge stats for a given item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetSourceReforgeStats)
---@return ReforgeStat[] reforgeStats
function C_Reforge.GetSourceReforgeStats() end

---Reforges an item to change its attributes.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.ReforgeItem)
---@param itemGUID string The globally unique identifier for the item
---@param reforgeID number The ID of the reforge action to apply
function C_Reforge.ReforgeItem(itemGUID, reforgeID) end

---Sets the reforge source to the item currently on the cursor.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.SetReforgeFromCursorItem)
function C_Reforge.SetReforgeFromCursorItem() end