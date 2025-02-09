---@meta

---! DRAFT - NEEDS REVIEW
---Adds a category filter for engraving.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.AddCategoryFilter)
---@param category number
function C_Engraving.AddCategoryFilter(category) end


---! DRAFT - NEEDS REVIEW  
---Clears all category filters in the C_Engraving module.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.ClearAllCategoryFilters)
function C_Engraving.ClearAllCategoryFilters() end


---! DRAFT - NEEDS REVIEW
---Adds an exclusive category filter for engraving.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.AddExclusiveCategoryFilter)
---@param category number The category to add as an exclusive filter.
function C_Engraving.AddExclusiveCategoryFilter(category) end


---! DRAFT - NEEDS REVIEW
---Casts a rune using the provided skill line ability ID. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.CastRune)
---@param skillLineAbilityID number
function C_Engraving.CastRune(skillLineAbilityID) end


---Clears the exclusive category filter for engravings.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.ClearExclusiveCategoryFilter)
function C_Engraving.ClearExclusiveCategoryFilter() end


---Clears the category filter for engraving.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.ClearCategoryFilter)
---@param category number
function C_Engraving.ClearCategoryFilter(category) end


---! DRAFT - NEEDS REVIEW
---Enables or disables the equipped filter for engraving.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.EnableEquippedFilter)
---@param enabled boolean
function C_Engraving.EnableEquippedFilter(enabled) end


---! DRAFT - NEEDS REVIEW
---Retrieves the current rune cast information in the engineering interface.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetCurrentRuneCast)
---@return EngravingData? engravingInfo
function C_Engraving.GetCurrentRuneCast() end


---! DRAFT - NEEDS REVIEW
---Checks if the engraving mode is enabled.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetEngravingModeEnabled)
---@return boolean enabled
function C_Engraving.GetEngravingModeEnabled() end


---! DRAFT - NEEDS REVIEW
---Determines the exclusive category filter. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetExclusiveCategoryFilter)
---@return number? category
function C_Engraving.GetExclusiveCategoryFilter() end


---! DRAFT - NEEDS REVIEW
---Returns the number of runes known and the maximum possible runes for an optional equipment slot.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetNumRunesKnown)
---@param equipmentSlot? number
---@return number known
---@return number max
function C_Engraving.GetNumRunesKnown(equipmentSlot) end


---! DRAFT - NEEDS REVIEW
---Retrieves the rune information for a specific inventory slot. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRuneForInventorySlot)
---@param containerIndex number
---@param slotIndex number
---@return EngravingData? engravingInfo
function C_Engraving.GetRuneForInventorySlot(containerIndex, slotIndex) end


---Gets rune information associated with a specific equipment slot. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRuneForEquipmentSlot)
---@param equipmentSlot number
---@return EngravingData? engravingInfo
function C_Engraving.GetRuneForEquipmentSlot(equipmentSlot) end


---Returns rune category IDs based on filtering options.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRuneCategories)
---@param shouldFilter boolean
---@param ownedOnly boolean
---@return number[] categories
function C_Engraving.GetRuneCategories(shouldFilter, ownedOnly) end


---Determines if engraving is enabled.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsEngravingEnabled)
---@return boolean value
function C_Engraving.IsEngravingEnabled() end


---! DRAFT - NEEDS REVIEW
---Fetches runes for a given category, with an option to filter by ownership.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.GetRunesForCategory)
---@param category number
---@param ownedOnly boolean
---@return EngravingData[] engravingInfo
function C_Engraving.GetRunesForCategory(category, ownedOnly) end


---! DRAFT - NEEDS REVIEW
---Checks if a category filter exists for engraving. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.HasCategoryFilter)
---@param category number
---@return boolean result
function C_Engraving.HasCategoryFilter(category) end


---! DRAFT - NEEDS REVIEW
---Checks if the equipped filter is enabled.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsEquippedFilterEnabled)
---@return boolean enabled
function C_Engraving.IsEquippedFilterEnabled() end


---! DRAFT - NEEDS REVIEW
---Determines if an equipment slot is engravable.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsEquipmentSlotEngravable)
---@param equipmentSlot number
---@return boolean result
function C_Engraving.IsEquipmentSlotEngravable(equipmentSlot) end


---Checks if a rune is equipped for a given skill line ability ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsRuneEquipped)
---@param skillLineAbilityID number
---@return boolean result
function C_Engraving.IsRuneEquipped(skillLineAbilityID) end


---! DRAFT - NEEDS REVIEW
---Determines if a specific inventory slot can be engraved using the current rune.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsInventorySlotEngravableByCurrentRuneCast)
---@param containerIndex number
---@param slotIndex number
---@return boolean result
function C_Engraving.IsInventorySlotEngravableByCurrentRuneCast(containerIndex, slotIndex) end


---Enables or disables the engraving mode. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.SetEngravingModeEnabled)
---@param enabled boolean
function C_Engraving.SetEngravingModeEnabled(enabled) end


---! DRAFT - NEEDS REVIEW
---Refreshes the list of runes.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.RefreshRunesList)
function C_Engraving.RefreshRunesList() end


---Determines if an engraving can be applied to a given inventory slot.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsInventorySlotEngravable)
---@param containerIndex number
---@param slotIndex number
---@return boolean result
function C_Engraving.IsInventorySlotEngravable(containerIndex, slotIndex) end


---! DRAFT - NEEDS REVIEW
---Checks if a rune spell with the given spellID is known. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.IsKnownRuneSpell)
---@param spellID number
---@return boolean result
function C_Engraving.IsKnownRuneSpell(spellID) end


---! DRAFT - NEEDS REVIEW
---Sets the search filter for engraving searches.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Engraving.SetSearchFilter)
---@param filter string The filter to be set for engraving.
function C_Engraving.SetSearchFilter(filter) end

