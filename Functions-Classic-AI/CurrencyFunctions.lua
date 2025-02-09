---@meta

---Alters the expanded state of a currency list header.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandCurrencyList)
---@param id number Index of the header in the currency list to expand/collapse.
---@param expanded number 0 to set to collapsed state; 1 to set to expanded state.
function ExpandCurrencyList(id, expanded) end


---Returns info for a tracked currency in the backpack.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBackpackCurrencyInfo)
---@param index number Ascending index from 1 to GetNumWatchedTokens().
---@return string name Localized currency name.
---@return number count Amount currently possessed by the player.
---@return number icon FileID of the currency icon.
---@return number currencyID CurrencyID of the currency.
function GetBackpackCurrencyInfo(index) end


---Retrieves the currency link for a specified currency ID.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyLink)
---@param currencyID integer The currency index
---@param currencyAmount integer The amount of currency
---@return string? currencyLink The currency link, or nil if the index is for a header
function GetCurrencyLink(currencyID, currencyAmount) end


---Returns the number of entries in the player's currency list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyListSize)
---@return number listSize
function GetCurrencyListSize() end


---Returns information about an entry in the currency list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyListInfo)
---@param index number The position of the currency in the list, starting from 1.
---@return string name Localized currency or currency header name.
---@return boolean isHeader True if the entry is a header.
---@return boolean isExpanded True if the header is expanded.
---@return boolean isUnused True if the currency is marked as unused.
---@return boolean isWatched True if the currency is being displayed on the backpack.
---@return number count Amount of this currency in the player's possession.
---@return string icon Path to the icon texture for item-based currencies.
---@return number maximum The maximum amount for the currency with 2 extra zeros or 0 if none.
---@return number|nil hasWeeklyLimit 1 if a weekly limit exists for the currency.
---@return number|nil currentWeeklyAmount Current week's amount of the currency.
---@return any unknown Possibly a deprecated slot, returns nil.
---@return number itemID Item ID corresponding to this currency if item-based.
function GetCurrencyListInfo(index) end


---Retrieves information about a currency, including its name, amount, and rarity.
---This function can accept an ID, a currency link, or a string fragment to identify the currency.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyInfo)
---@param identifier number|string Either a CurrencyID, a currencyLink, or a currencyString
---@return string name The name of the currency, localized
---@return number currentAmount Current amount of the currency
---@return string texture The file name of the currency's icon
---@return number earnedThisWeek The amount of the currency earned this week
---@return number weeklyMax Maximum amount of currency that can be earned this week
---@return number totalMax Total maximum currency that can be stockpiled
---@return boolean isDiscovered Whether the currency has been discovered by the character
---@return integer rarity Rarity indicator for the currency
function GetCurrencyInfo(identifier) end


---Returns the number of currency rewards for the currently viewed quest in the quest log or quest info frame.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumRewardCurrencies)
---@return number numCurrencies The number of currency rewards
function GetNumRewardCurrencies() end


---Picks up a specified currency to the cursor.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupCurrency)
---@param type number
function PickupCurrency(type) end


---Alters the backpack tracking state of a currency.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetCurrencyBackpack)
---@param id number Index of the currency in the currency list.
---@param backpack number 1 to track; 0 to clear tracking.
function SetCurrencyBackpack(id, backpack) end


---Marks or unmarks a currency as unused, altering its position in the currency list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetCurrencyUnused)
---@param id number Index of the currency in the currency list.
---@param unused number 1 to mark as unused, 0 to mark as used.
function SetCurrencyUnused(id, unused) end

