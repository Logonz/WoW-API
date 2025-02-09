---@meta

---! DRAFT - NEEDS REVIEW
---Returns the gem IDs for a container item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Container.GetContainerItemGems)
---@param containerIndex Enum.BagIndex
---@param slotIndex number
---@return number[] numGems
function C_Container.GetContainerItemGems(containerIndex, slotIndex) end


---Checks if a bag slot flag is enabled on other bank bags. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Container.IsBagSlotFlagEnabledOnOtherBankBags)
---@param bagIndex Enum.BagIndex
---@param flagIndex number
---@return boolean isSet
function C_Container.IsBagSlotFlagEnabledOnOtherBankBags(bagIndex, flagIndex) end

