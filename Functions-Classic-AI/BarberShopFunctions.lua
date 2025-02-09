---@meta

C_BarberShop = {}

---Cycles through character customization options in the Barber Shop.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.CycleCharCustomization)
---@param optionID number
---@param forward boolean
function C_BarberShop.CycleCharCustomization(optionID, forward) end

---Retrieves the cost of the player's choices in the Barber Shop.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.GetBarbersChoiceCost)
---@return number cost
function C_BarberShop.GetBarbersChoiceCost() end

---Gets information about a specific customization type in the barber shop.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.GetCustomizationTypeInfo)
---@param id number The ID of the customization type.
---@return BarberShopAlternateFormData data
function C_BarberShop.GetCustomizationTypeInfo(id) end

---Checks if the customization type is valid.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.IsValidCustomizationType)
---@param customizationType number
---@return boolean isValid
function C_BarberShop.IsValidCustomizationType(customizationType) end

---Determines if the character is viewing their original sex in the Barber Shop.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.IsViewingNativeSex)
---@return boolean isViewingNativeSex
function C_BarberShop.IsViewingNativeSex() end

---Checks if the currently viewed character sex in the BarberShop is visible.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.IsViewingVisibleSex)
---@return boolean isViewingVisibleSex
function C_BarberShop.IsViewingVisibleSex() end

---Sets the portrait texture for the barber shop interface.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BarberShop.SetPortraitTexture)
---@param textureObject table
---@return boolean success 
function C_BarberShop.SetPortraitTexture(textureObject) end

---Confirms the selected choices at the barber.
---[Documentation](https://wowpedia.fandom.com/wiki/API_ConfirmBarbersChoice)
function ConfirmBarbersChoice() end