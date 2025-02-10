---@meta
--* GENERATED BY gemini-2.0-flash

---Buys the next stable slot if the stable window is open and you can afford it.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_BuyStableSlot)
function BuyStableSlot() end

---Selects a stable pet.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_ClickStablePet)
---@param index number
function ClickStablePet(index) end

---Closes the pet stable window.<br>
---This function was deprecated in patch 10.2.7 and will be removed in patch 11.0.2.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ClosePetStables)
function ClosePetStables() end

---Confirms unlearning the current pet's skills.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConfirmPetUnlearn)
function ConfirmPetUnlearn() end

---Returns the next stable slot's cost in copper.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 4.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNextStableSlotCost)
---@return number nextSlotCost The cost of the next stable slot in copper.
function GetNextStableSlotCost() end

---Returns the amount of stable slots.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 4.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumStableSlots)
---@return number numSlots
function GetNumStableSlots() end

---Returns the pet's happiness, damage percentage, and loyalty gain rate.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 4.1.0.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetHappiness)
---@return number happiness the numerical happiness value of the pet (1 = unhappy, 2 = content, 3 = happy)
---@return number damagePercentage damage modifier, happiness affects this (unhappy = 75%, content = 100%, happy = 125%)
---@return number loyaltyRate the rate at which your pet is currently gaining loyalty (< 0, losing loyalty, > 0, gaining loyalty)
function GetPetHappiness() end

---Returns pet loyalty flavor text.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 3.0.2.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetLoyalty)
---@return string petLoyaltyText The localized pet loyalty level, i.e. "(Loyalty Level 6) Best Friend".
function GetPetLoyalty() end

---Gets the training point information about the current pet.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 3.0.2.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetTrainingPoints)
---@return number totalPoints The total of points spent and points available.
---@return number spent The number of points spent.
function GetPetTrainingPoints() end

---Gets the index of the currently selected pet in the stable.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 4.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSelectedStablePet)
---@return number The index of the currently selected pet slot, 0 being the current pet, 1 and 2 being the left and right slots, and -1 for when no pet is selected.
function GetSelectedStablePet() end

---Returns the food types the specified stabled pet can eat.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetStablePetFoodTypes)
---@param index number The stable slot index of the pet: 0 for the current pet, 1 for the pet in the left slot, and 2 for the pet in the right slot.
---@return string ... A list of the pet food type names, see GetPetFoodTypes().
function GetStablePetFoodTypes(index) end

---Returns info for a specific stabled pet.<br>
---This function was deprecated in patch 10.2.7 and will be removed in patch 11.0.2.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetStablePetInfo)
---@param index number The index of the pet slot, 1 through 5 are the hunter's active pets, 6 through 25 are the hunter's stabled pets.
---@return string petIcon The path to texture to use as the icon for the pet.
---@return string petName The pet name.
---@return number petLevel The pet level.
---@return string petType The localized pet family.
---@return string petTalents The pet's talent group.
function GetStablePetInfo(index) end

---Returns the number of available abilities for the player's combat pet.<br>
---This numSpells return value is not the number that are on the pet bar, but the number of entries in the pet's spell book.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_HasPetSpells)
---@return number? numSpells The number of pet abilities available, or nil if you do not have a pet with a spell book.
---@return string petToken Pet type, can be "DEMON" or "PET".
function HasPetSpells() end

---Permanently abandons your pet.<br>
---Opposed to abandoning via pet portrait menu, THERE IS NO CONFIRMATION before abandoning the pet. Use with caution.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetAbandon)
function PetAbandon() end

---Returns true if the pet can be renamed.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 10.2.7.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetCanBeRenamed)
---@return boolean canRename # true if the player's pet can be renamed.
function PetCanBeRenamed() end

---Renames your pet.<br>
---Only hunters and frost mages can rename their pets.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetRename)
---@param name string The new name of the pet
function PetRename(name) end

---Attaches a pet in your stable to your cursor.<br>
---This function was deprecated in patch 10.2.7 and will be removed in patch 11.0.2.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupStablePet)
---@param index number 1 for the pet in the slot on the left, and 2 for the pet in the slot on the right.
function PickupStablePet(index) end

---Sets the paperdoll model in the pet stable to a new player model.<br>
---This method does not cause the model to be shown. The model still needs its Show() method called afterward.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetPetStablePaperdoll)
---@param modelObject UIOBJECT_PlayerModel The model of the pet to display.
function SetPetStablePaperdoll(modelObject) end

