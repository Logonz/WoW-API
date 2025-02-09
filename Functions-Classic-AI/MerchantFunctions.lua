---@meta

---Returns info for a merchant item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetMerchantItemInfo)
---@param index number The index of the item in the merchant's inventory
---@return string name The name of the item
---@return number texture The texture that represents the item's icon
---@return number price The price of the item (in copper)
---@return number quantity The quantity that will be purchased
---@return number numAvailable The number of items in stock, -1 for unlimited
---@return boolean isPurchasable
---@return boolean isUsable True if the player can use this item
---@return boolean extendedCost True if item has extended cost info
---@return number? currencyID
---@return number? spellID
function GetMerchantItemInfo(index) end

