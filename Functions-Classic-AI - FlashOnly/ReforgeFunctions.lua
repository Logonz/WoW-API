---@meta
--* GENERATED BY gemini-2.0-flash-lite-preview-02-05

---Closes the Reforge UI.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.CloseReforge)
function C_Reforge.CloseReforge() end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetDestinationReforgeStats)
---@param srcStat number unknown
---@param srcStatValue number unknown
---@return dstReforgeStats[] dstStatsInfo unknown
function C_Reforge.GetDestinationReforgeStats(srcStat, srcStatValue) end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetNumReforgeOptions)
---@return number numOptions
function C_Reforge.GetNumReforgeOptions() end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeItemInfo)
---@return number index
---@return number itemID
---@return string itemName
---@return number itemQualityID
---@return string soulbound
---@return number reforgeCost
function C_Reforge.GetReforgeItemInfo() end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeItemStats)
---@return reforgeStatsInfo[] reforgeStats
function C_Reforge.GetReforgeItemStats() end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetReforgeOptionInfo)
---@param index number index
---@return string srcStatName
---@return number srcStat
---@return number srcStatReduction
---@return string dstStatName
---@return number dstStat
---@return number dstStatAddition
function C_Reforge.GetReforgeOptionInfo(index) end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.GetSourceReforgeStats)
---@return srcReforgeStats[] srcStatsInfo
function C_Reforge.GetSourceReforgeStats() end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.ReforgeItem)
---@param index number
function C_Reforge.ReforgeItem(index) end

---Needs summary.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Reforge.SetReforgeFromCursorItem)
function C_Reforge.SetReforgeFromCursorItem() end

