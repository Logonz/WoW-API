---@meta

---Purchases an additional stable slot for your pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BuyStableSlot)
function BuyStableSlot() end

---! DRAFT - NEEDS REVIEW
---Activates a stable pet by index.
---@param index number The index of the pet to be activated.
function ClickStablePet(index) end

---Closes the pet stables.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ClosePetStables)
function ClosePetStables() end

---! DRAFT - NEEDS REVIEW  
---Confirms the unlearning of a pet's skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConfirmPetUnlearn)
function ConfirmPetUnlearn() end

---Returns the cost required to buy the next pet stable slot.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNextStableSlotCost)
---@return number cost
function GetNextStableSlotCost() end

---Returns the number of stable slots available to the player.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetNumStableSlots)
---@return number numSlots
function GetNumStableSlots() end

---Returns the happiness level of the player's pet.  
---! DRAFT - NEEDS REVIEW
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetHappiness)
---@return number happiness
---@return string icon
---@return string mood
function GetPetHappiness() end

---Returns the current loyalty level and relative loyalty value of the player's pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetLoyalty)
---@return string loyaltyLevel
---@return number loyaltyPercentage
function GetPetLoyalty() end

---! DRAFT - NEEDS REVIEW
---Returns the number of training points the player's pet currently has. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetTrainingPoints)
---@return number trainingPoints
function GetPetTrainingPoints() end

---Returns the currently selected pet index in the stable.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSelectedStablePet)
---@return number? selectedPetIndex
function GetSelectedStablePet() end

---Returns the types of pet food for a given stable slot.  
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetStablePetFoodTypes)
---@param stableSlot number
---@return string foods
function GetStablePetFoodTypes(stableSlot) end

---Returns information about a stable pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetStablePetInfo)
---@param index number The stable slot index.
---@return string name
---@return string icon
---@return number level
---@return string family
---@return string talent
---@return boolean isActive
function GetStablePetInfo(index) end


---Returns whether the pet has any spells and the first pet spell ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_HasPetSpells)
---@return boolean hasSpells
---@return number firstSpellID
function HasPetSpells() end


---Abandons the specified pet, removing it permanently from the player's pet list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetAbandon)
---@param index number The index of the pet to abandon, starting from 1.
function PetAbandon(index) end

---Determines if a pet can be renamed.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetCanBeRenamed)
---@return boolean flag
function PetCanBeRenamed() end

---Renames a specified pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetRename)
---@param petId string The ID of the pet to rename
---@param name string The new name for the pet
function PetRename(petId, name) end

---Picks up the specified stable pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupStablePet)
---@param index number The index of the pet to be picked up.
function PickupStablePet(index) end

---Sets the stable paperdoll for the pet.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetPetStablePaperdoll)
---@param stableSlot number
function SetPetStablePaperdoll(stableSlot) end