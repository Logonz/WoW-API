---@meta

C_Engraving = {}

---Adds a category filter.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.AddCategoryFilter)
---@param categoryID number
function C_Engraving.AddCategoryFilter(categoryID) end

---Adds an exclusive category filter.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.AddExclusiveCategoryFilter)
---@param categoryID number
function C_Engraving.AddExclusiveCategoryFilter(categoryID) end

---Cast a rune with the specified engraving ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.CastRune)
---@param engravingID number
function C_Engraving.CastRune(engravingID) end

---Clears all category filters for engravings.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.ClearAllCategoryFilters)
function C_Engraving.ClearAllCategoryFilters() end

---! DRAFT - NEEDS REVIEW
---Clears the category filter for engravings.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.ClearCategoryFilter)
function C_Engraving.ClearCategoryFilter() end

---Clears exclusive category filters for the engraving system.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.ClearExclusiveCategoryFilter)
function C_Engraving.ClearExclusiveCategoryFilter() end


---! DRAFT - NEEDS REVIEW
---Enables a filter for engravings on equipped items.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.EnableEquippedFilter)
function C_Engraving.EnableEquippedFilter() end


---Returns information about the currently cast rune.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetCurrentRuneCast)
---@return number runeID
---@return string icon
---@return string name
---@return number startTime
---@return number endTime
function C_Engraving.GetCurrentRuneCast() end


---Checks if the engraving mode is enabled.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetEngravingModeEnabled)
---@return boolean enabled
function C_Engraving.GetEngravingModeEnabled() end


---! DRAFT - NEEDS REVIEW
---Retrieve the filter status for an exclusive engraving category.
---@param index number
---@return boolean isEnabled
function C_Engraving.GetExclusiveCategoryFilter(index) end

---Returns the number of runes known for a character.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetNumRunesKnown)
---@return number numRunesKnown
function C_Engraving.GetNumRunesKnown() end

---Returns information about rune categories.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRuneCategories)
---@return table categories Information about available rune categories
function C_Engraving.GetRuneCategories() end

---Retrieves the rune associated with a specific equipment slot. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRuneForEquipmentSlot)
---@param equipmentSlot number
---@return number runeID
function C_Engraving.GetRuneForEquipmentSlot(equipmentSlot) end

---Returns the rune for a specified inventory slot. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRuneForInventorySlot)
---@param inventorySlotID number
---@return number runeID
function C_Engraving.GetRuneForInventorySlot(inventorySlotID) end

---Returns the list of runes available for a specified category.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRunesForCategory)
---@param categoryID number
---@return RuneInfo[] runes
function C_Engraving.GetRunesForCategory(categoryID) end

---Checks if a category filter is applied.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.HasCategoryFilter)
---@param categoryID number
---@return boolean hasFilter
function C_Engraving.HasCategoryFilter(categoryID) end

---Checks if engraving is enabled for a given map. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsEngravingEnabled)
---@param uiMapID number
---@return boolean isEnabled
function C_Engraving.IsEngravingEnabled(uiMapID) end

---Determines if an equipment slot can be engraved.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsEquipmentSlotEngravable)
---@param equipmentSlotIndex number
---@return boolean isEngravable
function C_Engraving.IsEquipmentSlotEngravable(equipmentSlotIndex) end


---Checks if the equipped filter is enabled.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsEquippedFilterEnabled)
---@return boolean isEnabled
function C_Engraving.IsEquippedFilterEnabled() end


---Determines if an inventory slot can have an engraving applied to it. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsInventorySlotEngravable)
---@param inventorySlot number
---@return boolean isEngravable
function C_Engraving.IsInventorySlotEngravable(inventorySlot) end

---! DRAFT - NEEDS REVIEW
---Determines if the inventory slot can be engraved by the current rune cast.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsInventorySlotEngravableByCurrentRuneCast)
---@param slot number
---@return boolean canEngrave
function C_Engraving.IsInventorySlotEngravableByCurrentRuneCast(slot) end

---Checks if the rune spell corresponding to a given spell ID is known.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsKnownRuneSpell)
---@param spellID number
---@return boolean isKnown
function C_Engraving.IsKnownRuneSpell(spellID) end

---Check if a rune is equipped for a specific rune type.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsRuneEquipped)
---@param runeType number
---@return boolean isEquipped
function C_Engraving.IsRuneEquipped(runeType) end

---Refreshes the list of runes.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.RefreshRunesList)
function C_Engraving.RefreshRunesList() end

---Sets the engraving mode to be enabled or disabled.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.SetEngravingModeEnabled)
---@param enabled boolean
function C_Engraving.SetEngravingModeEnabled(enabled) end

---Sets the search filter for engravings.
---@param searchText string
---@return boolean success
function C_Engraving.SetSearchFilter(searchText) end