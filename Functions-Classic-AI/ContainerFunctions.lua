---@meta

C_Container = {}

---Retrieves the item IDs of gems socketed in the specified container item's equipment slot.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Container.GetContainerItemGems)
---@param bagID number The bag ID.
---@param slotIndex number The slot index.
---@return number[] gemIDs An array containing the item IDs of the socketed gems.
function C_Container.GetContainerItemGems(bagID, slotIndex) end

---! DRAFT - NEEDS REVIEW
---Determines if a bag slot flag is enabled on other bank bags.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Container.IsBagSlotFlagEnabledOnOtherBankBags)
---@param flag number
---@return boolean isEnabled
function C_Container.IsBagSlotFlagEnabledOnOtherBankBags(flag) end