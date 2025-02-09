---@meta

---Returns the cost of the barber's choice in the game. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.GetBarbersChoiceCost)
---@return number cost
function C_BarberShop.GetBarbersChoiceCost() end


---! DRAFT - NEEDS REVIEW
---Cycles through character customization options in the barber shop.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.CycleCharCustomization)
---@param type Enum.CharCustomizationType
---@param forward boolean
function C_BarberShop.CycleCharCustomization(type, forward) end


---! DRAFT - NEEDS REVIEW
---Retrieves information about a customization type in the BarberShop.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.GetCustomizationTypeInfo)
---@param type Enum.CharCustomizationType
---@return string customizationName
---@return string name
---@return boolean isCurrent
function C_BarberShop.GetCustomizationTypeInfo(type) end


---! DRAFT - NEEDS REVIEW
---Validates if a given type is a valid customization type in the BarberShop.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.IsValidCustomizationType)
---@param type Enum.CharCustomizationType
---@return boolean isValid
function C_BarberShop.IsValidCustomizationType(type) end


---Returns whether the currently visible body type at the barber shop is different from the character's original body type.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.IsViewingNativeSex)
---@return boolean isNativeSex True if the character hasn't changed body type in the barber shop UI, otherwise false
function C_BarberShop.IsViewingNativeSex() end


---Returns whether the currently visible body type at the barber shop matches the specified sex ID.
---The sex parameter ranges from 0 (masculine/male) to 1 (feminine/female).
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.IsViewingVisibleSex)
---@param sex number
---@return boolean isVisibleSex
function C_BarberShop.IsViewingVisibleSex(sex) end


---! DRAFT - NEEDS REVIEW
---Sets the portrait texture for a specific race and gender.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.SetPortraitTexture)
---@param texture Texture
---@param raceID number
---@param sex number
function C_BarberShop.SetPortraitTexture(texture, raceID, sex) end


--- Confirms the player's choice in the barber shop. 
--- This API only exists in Cata Classic and Classic Era.
--- [Documentation](https://warcraft.wiki.gg/wiki/API_ConfirmBarbersChoice)
function ConfirmBarbersChoice() end

