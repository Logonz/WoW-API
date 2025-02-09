---@meta

---Buys a stable slot if the stable window is open and you have sufficient funds. Removed in Patch 4.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BuyStableSlot)
function BuyStableSlot() end


---Closes the pet stable window. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_ClosePetStables)
function ClosePetStables() end


---Selects a stable pet by its index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ClickStablePet)
---@param index number The index of the pet to select in the stable.
function ClickStablePet(index) end


---Confirms unlearning the current pet's skills in World of Warcraft. 
---This function was added in Patch 1.7.0 and removed in Patch 3.1.0.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConfirmPetUnlearn)
function ConfirmPetUnlearn() end


---Returns the next stable slot's cost in copper.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNextStableSlotCost)
---@return number nextSlotCost The cost of the next stable slot in copper.
function GetNextStableSlotCost() end


---Returns the amount of stable slots available to the player. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumStableSlots)
---@return number numSlots
function GetNumStableSlots() end


---Returns pet loyalty flavor text.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetLoyalty)
---@return string petLoyaltyText The localized pet loyalty level, i.e. "(Loyalty Level 6) Best Friend".
function GetPetLoyalty() end


---Gets the training point information for the current pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetTrainingPoints)
---@return number totalPoints The total of points spent and points available.
---@return number spent The number of points spent.
function GetPetTrainingPoints() end


---Returns the pet's happiness, damage percentage, and loyalty gain rate. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPetHappiness)
---@return number happiness The numerical happiness value (1 = unhappy, 2 = content, 3 = happy)
---@return number damagePercentage Damage modifier percentage based on happiness (75% unhappy, 100% content, 125% happy)
---@return number loyaltyRate The rate of loyalty gain (>0 gaining, <0 losing)
function GetPetHappiness() end


---Gets the index of the currently selected pet in the stable. Returns 0 for the current pet, 1 and 2 for the left and right slots, and -1 if no pet is selected.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSelectedStablePet)
---@return number selectedPet The index of the selected pet slot
function GetSelectedStablePet() end


---Returns info for a specific stabled pet. 
---The function returns the pet's icon, name, level, type, and talents based on the provided index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetStablePetInfo)
---@param index number The index of the pet slot, 1 through 5 are the hunter's active pets, 6 through 25 are the hunter's stabled pets.
---@return string petIcon The path to texture to use as the icon for the pet.
---@return string petName The name of the pet.
---@return number petLevel The level of the pet.
---@return string petType The localized family of the pet.
---@return string petTalents The talent group of the pet.
function GetStablePetInfo(index) end


---Returns the food types the specified stabled pet can eat.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetStablePetFoodTypes)
---@param index number The stable slot index of the pet: 0 for the current pet, 1 for the pet in the left slot, and 2 for the pet in the right slot.
---@return string[] A list of the pet food type names.
function GetStablePetFoodTypes(index) end


---Returns the number of available abilities for the player's combat pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_HasPetSpells)
---@return number numSpells The number of pet abilities available, or nil if no pet with a spell book
---@return string petToken Pet type, can be "DEMON" or "PET"
function HasPetSpells() end


---Permanently abandons your pet.
---This action has no confirmation prompt. Use with caution.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetAbandon)
function PetAbandon() end


---Renames your pet. Only hunters and frost mages can rename their pets. Each pet can be renamed once. Using this function when the pet has already been renamed results in an error message.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetRename)
---@param name string - The new name of the pet
function PetRename(name) end


---Returns true if the player's pet can be renamed.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PetCanBeRenamed)
---@return boolean canRename True if the pet can be renamed.
function PetCanBeRenamed() end


---Attaches a pet in the stable to your cursor.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupStablePet)
---@param index number The index of the pet, where 1 refers to the pet in the slot on the left and 2 for the slot on the right.
function PickupStablePet(index) end


---Sets the paperdoll model in the pet stable to a new player model.
---This method does not cause the model to be shown. The model still needs its Show() method called afterward.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetPetStablePaperdoll)
---@param modelObject PlayerModel The model of the pet to display.
function SetPetStablePaperdoll(modelObject) end

