---@meta
--* GENERATED BY gemini-2.0-flash-lite-preview-02-05

---Alters the expanded state of a currency list header.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandCurrencyList)
---@param id number Index of the header in the currency list to expand/collapse.
---@param expanded number 0 to set to collapsed state; 1 to set to expanded state.
function ExpandCurrencyList(id, expanded) end

---Returns info for a tracked currency in the backpack.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBackpackCurrencyInfo)
---@param index number Index, ascending from 1 to GetNumWatchedTokens().
---@return string name Localized currency name.
---@return number count Amount currently possessed by the player.
---@return number icon FileID
---@return number currencyID CurrencyID
function GetBackpackCurrencyInfo(index) end

---! DRAFT - More than one function signature<br>
---Retrieve Information about a currency at index including it's amount.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyInfo)
---@param id number Integer - CurrencyID
---@return string name the name of the currency, localized to the language
---@return number amount Current amount of the currency at index
---@return string texture The file name of the currency's icon.
---@return number earnedThisWeek The amount of the currency earned this week
---@return number weeklyMax Maximum amount of currency possible to be earned this week
---@return number totalMax Total maximum currency possible to stockpile
---@return boolean isDiscovered Whether the character has ever got some of this currency
---@return number rarity Rarity indicator for this currency
function GetCurrencyInfo(id) end

---! DRAFT - More than one function signature<br>
---Retrieve Information about a currency at index including it's amount.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyInfo)
---@param currencyLink string String - The full currencyLink as found with GetCurrencyLink() or GetCurrencyListLink().
---@return string name the name of the currency, localized to the language
---@return number amount Current amount of the currency at index
---@return string texture The file name of the currency's icon.
---@return number earnedThisWeek The amount of the currency earned this week
---@return number weeklyMax Maximum amount of currency possible to be earned this week
---@return number totalMax Total maximum currency possible to stockpile
---@return boolean isDiscovered Whether the character has ever got some of this currency
---@return number rarity Rarity indicator for this currency
function GetCurrencyInfo(currencyLink) end

---! DRAFT - More than one function signature<br>
---Retrieve Information about a currency at index including it's amount.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyInfo)
---@param currencyString string String - A fragment of the currencyLink string for the item, e.g. "currency:396" for Valor Points.
---@return string name the name of the currency, localized to the language
---@return number amount Current amount of the currency at index
---@return string texture The file name of the currency's icon.
---@return number earnedThisWeek The amount of the currency earned this week
---@return number weeklyMax Maximum amount of currency possible to be earned this week
---@return number totalMax Total maximum currency possible to stockpile
---@return boolean isDiscovered Whether the character has ever got some of this currency
---@return number rarity Rarity indicator for this currency
function GetCurrencyInfo(currencyString) end

---Get the currencyLink for the specified currencyID.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyLink)
---@param currencyID integer currency index - see table at GetCurrencyInfo for a list
---@param currencyAmount integer currency amount
---@return string currencyLink The currency link (similar to itemLink) for the specified index (e.g. "|cffa335ee|Hcurrency:396:0|h[Valor Points]|h|r" for Valor Points) or nil if the index is for a header.
function GetCurrencyLink(currencyID, currencyAmount) end

---Returns information about an entry in the currency list.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyListInfo)
---@param index number index, ascending from 1 to GetCurrencyListSize().
---@return string name localized currency (or currency header) name.
---@return boolean isHeader true if this entry is a header, false otherwise.
---@return boolean isExpanded true if this entry is an expanded header, false otherwise.
---@return boolean isUnused true if this entry is a currency marked as unused, false otherwise.
---@return boolean isWatched true if this entry is a currency currently displayed on the backpack, false otherwise.
---@return number count amount of this currency in the player's possession (0 for headers).
---@return string icon path to the icon texture for item-based currencies, invalid for arena/honor points.
---@return number maximum 0 if this currency has no limit, otherwise integer value with 2 extra zeros (e.g. 400000 = 4000.00 as in Justice Points and Honor Points)
---@return number? hasWeeklyLimit 1 if this currency has a weekly limit (Valor Points), nil otherwise
---@return number? currentWeeklyAmount amount of this currency obtained for the current week, nil otherwise
---@return unknown unknown possible deprecated slot for itemID? All known cases return nil
---@return number itemID item ID corresponding to this item-based currency, invalid for arena/honor points.
function GetCurrencyListInfo(index) end

---Returns the number of entries in the currency list.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyListSize)
---@return number listSize number of entries in the player's currency list.
function GetCurrencyListSize() end

---Returns the number of currency rewards for the quest currently being viewed in the quest log or quest info frame.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumRewardCurrencies)
---@return number numCurrencies The number of currency rewards
function GetNumRewardCurrencies() end

---Picks up a currency to the cursor.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupCurrency)
---@param type number
function PickupCurrency(type) end

---Marks/unmarks a currency as unused.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetCurrencyUnused)
---@param id number Index of the currency in the currency list to alter unused status of.
---@param unused number 1 to mark the currency as unused; 0 to mark the currency as used.
function SetCurrencyUnused(id, unused) end

