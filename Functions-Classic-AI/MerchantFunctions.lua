---@meta


---Returns details about a specific item from a merchant.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetMerchantItemInfo)
---@param index number The index of the item in the merchant's inventory
---@return string name The name of the item
---@return string texture The texture path of the item's icon
---@return number price The cost of the item in the vendor's currency
---@return number stackCount The size of the item's stack
---@return number numAvailable The number of items available in the vendor's inventory
---@return boolean isUsable Indicates if the item can be used by the player
---@return number extendedCost The extended cost of the item
function GetMerchantItemInfo(index) end
