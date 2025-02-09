---@meta


---Expands or collapses the list of currencies.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandCurrencyList)
---@param currencyTypeIndex number
---@param isExpanded boolean
function ExpandCurrencyList(currencyTypeIndex, isExpanded) end


---Retrieves information about a specified currency in the player's backpack.  
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetBackpackCurrencyInfo)
---@param index number The index of the currency in the backpack (1 to 3).
---@return string currencyName The name of the currency.
---@return number currencyAmount The amount of the currency.
---@return number currencyIconFileID The file ID of the currency's icon.
function GetBackpackCurrencyInfo(index) end

---Retrieves information about a specific currency.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyInfo)
---@param currencyID number
---@return string name
---@return string currentAmount
---@return string iconFileID
---@return string earnedThisWeek
---@return string weeklyMax
---@return string totalMax
---@return boolean isDiscovered
function GetCurrencyInfo(currencyID) end

---Returns a hyperlink for a specified currency.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyLink)
---@param currencyID number
---@param currencyAmount number
---@return string hyperlink
function GetCurrencyLink(currencyID, currencyAmount) end

---! DRAFT - NEEDS REVIEW
---Retrieves detailed information about a currency based on its index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyListInfo)
---@param index number
---@return string name
---@return boolean isHeader
---@return boolean isExpanded
---@return boolean isUnused
---@return boolean isWatched
---@return number count
---@return string icon
---@return number unusedCurrencyType
---@return number itemID
function GetCurrencyListInfo(index) end

---Returns the number of currencies in the currency list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrencyListSize)
---@return number numCurrencies
function GetCurrencyListSize() end

---Returns the number of currencies rewarded for a specified quest.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumRewardCurrencies)
---@param questID number
---@return number currencyCount
function GetNumRewardCurrencies(questID) end

---Picks up a currency, placing it on the cursor.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupCurrency)
---@param type string The type of the currency, either "currency" or "token".
---@param index number The index of the currency or token.
function PickupCurrency(type, index) end

---Sets whether a specific currency should be tracked in the backpack.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetCurrencyBackpack)
---@param currencyType number
---@param backpackEnabled boolean
function SetCurrencyBackpack(currencyType, backpackEnabled) end


---Marks a specified currency ID as unused.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetCurrencyUnused)
---@param currencyID number
---@param unused boolean
function SetCurrencyUnused(currencyID, unused) end
