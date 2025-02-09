---@meta
---! DRAFT - NEEDS REVIEW  
---Closes the Reforge UI in World of Warcraft.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.CloseReforge)  
function C_Reforge.CloseReforge() end

---Retrieves the destination reforge stats for a given source stat and its value.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetDestinationReforgeStats)
---@param srcStat number
---@param srcStatValue number
---@return dstReforgeStats[] dstStatsInfo
function C_Reforge.GetDestinationReforgeStats(srcStat, srcStatValue) end


---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetNumReforgeOptions)
---@return number numOptions
function C_Reforge.GetNumReforgeOptions() end


---! DRAFT - NEEDS REVIEW
---Retrieves the statistics of a reforged item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeItemStats)
---@return reforgeStatsInfo[] reforgeStats
function C_Reforge.GetReforgeItemStats() end


---! DRAFT - NEEDS REVIEW  
---Reforges an item at the specified index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.ReforgeItem)
---@param index number
function C_Reforge.ReforgeItem(index) end


---! DRAFT - NEEDS REVIEW
---Returns the source reforge stats.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetSourceReforgeStats)
---@return srcReforgeStats[] srcStatsInfo
function C_Reforge.GetSourceReforgeStats() end


---! DRAFT - NEEDS REVIEW
---Returns information about an item being reforged. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeItemInfo)
---@return number index
---@return number itemID
---@return string itemName
---@return number itemQualityID
---@return string soulbound
---@return number reforgeCost
function C_Reforge.GetReforgeItemInfo() end


---! DRAFT - NEEDS REVIEW
---Retrieves reforge option information for a given index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeOptionInfo)
---@param index number
---@return string srcStatName
---@return number srcStat
---@return number srcStatReduction
---@return string dstStatName
---@return number dstStat
---@return number dstStatAddition
function C_Reforge.GetReforgeOptionInfo(index) end


---! DRAFT - NEEDS REVIEW
---Sets reforge attributes for the item from the cursor.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.SetReforgeFromCursorItem)
function C_Reforge.SetReforgeFromCursorItem() end

