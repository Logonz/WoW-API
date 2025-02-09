---@meta

---Determines if a spell exists for a given spell ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_DoesSpellExist)
---@param spellID number
---@return boolean doesExist
function DoesSpellExist(spellID) end

---! DRAFT - NEEDS REVIEW    
---Returns the current level spells available to the player.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrentLevelSpells)  
---@return number[] spellIDs  
function GetCurrentLevelSpells() end


---Returns the total number of tabs in the player's spellbook and the number currently visible.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumSpellTabs)
---@return integer numTabs
---@return integer numVisibleTabs
function GetNumSpellTabs() end


---Toggles autocast for a specified spell. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellAutocast)
---@param spellID number
---@return boolean autocastEnabled
---@return boolean isAutocastable
function GetSpellAutocast(spellID) end

---Returns information about a spell book item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellBookItemInfo)
---@param slotID number
---@param bookType string
---@return string texture
---@return string spellID
---@return integer spellIndex
---@return string spellName
---@return string subSpellName
---@return boolean isPassive
---@return boolean isCancelled
---@return number slotNumber
---@return boolean isIgnored
function GetSpellBookItemInfo(slotID, bookType) end

---Returns the name of a spell or item in the spellbook.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellBookItemName)
---@param index number
---@param bookType string
---@return string spellName
---@return string spellSubName
function GetSpellBookItemName(index, bookType) end

---Returns the fileID of the texture for a spell or item in the player's spellbook.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellBookItemTexture)
---@param spellIndex number
---@param bookType string
---@return number textureFileID
function GetSpellBookItemTexture(spellIndex, bookType) end


---Returns information about the charges of a spell, including the current, maximum charges, and charge cooldown.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellCharges)
---@param spellID number
---@return number currentCharges
---@return number maxCharges
---@return number cooldownStart
---@return number cooldownDuration
function GetSpellCharges(spellID) end


---Returns information about the cooldown status of a specified spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellCooldown)
---@param spellID number|string
---@return number startTime
---@return number duration
---@return number enable
function GetSpellCooldown(spellID) end

---Returns the number of times a spell can be cast based on its remaining charges or remaining reagents.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellCount)
---@param spellID number|string
---@return number count
function GetSpellCount(spellID) end


---Returns the description of a spell by its spellID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellDescription)
---@param spellID number
---@return string description
function GetSpellDescription(spellID) end


---Returns detailed information about a specified spell by its ID. 
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetSpellInfo)
---@param spellID number|string
---@return string name
---@return string rank
---@return string icon
---@return number castingTime
---@return number minRange
---@return number maxRange
function GetSpellInfo(spellID) end

---Returns a hyperlink for a spell, which can be used in chat or tooltips.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellLink)
---@param spellID number
---@param spellRank? number
---@return string spellLink
function GetSpellLink(spellID, spellRank) end


---Returns the cooldown data of a spell's loss of control.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellLossOfControlCooldown)
---@param spellID number
---@return number start
---@return number duration
---@return number enabled
function GetSpellLossOfControlCooldown(spellID) end


---Returns information about the power cost of a spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellPowerCost)
---@param spellId number
---@return table costs
function GetSpellPowerCost(spellId) end

---Retrieves detailed information about a specified spell tab.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetSpellTabInfo)
---@param tabIndex number The index of the spell tab.
---@return string name The name of the Tab.
---@return number texture The texture of the Tab.
---@return number offset The offset in the spell book to the first spell under this tab.
---@return number numEntries The number of spells in this tab.
---@return boolean isGuild Is this a guild spell tab?
function GetSpellTabInfo(tabIndex) end

---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellTexture)
---@param spellID number
---@return string texture
function GetSpellTexture(spellID) end

---Returns whether the specified index corresponds to an attack spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsAttackSpell)
---@param index number|string
---@return boolean isAttackSpell
function IsAttackSpell(index) end

---Checks if a specified spell is currently active, such as being cast.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsCurrentSpell)
---@param spellID number|string 
---@return boolean isCurrent
function IsCurrentSpell(spellID) end

---Checks if the specified spell is passive. 
---[Documentation](https://wowpedia.fandom.com/wiki/API_IsPassiveSpell)
---@param spellID number|string
---@return boolean isPassive
function IsPassiveSpell(spellID) end

---Returns whether a spell is in range of the specified unit or location.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsSpellInRange)
---@param spellName string
---@param unit string | nil
---@return number|nil isInRange 0 if out of range, 1 if in range, nil if invalid input
function IsSpellInRange(spellName, unit) end

---Checks whether a spell can be used (e.g., enough mana, not on cooldown).
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsUsableSpell)
---@param spellID number|string
---@return boolean isUsable
---@return boolean notEnoughMana
function IsUsableSpell(spellID) end


---Picks up a spell from the spell book and puts it on the cursor. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupSpell)
---@param spellID number The unique identifier of the spell to be picked up.
function PickupSpell(spellID) end


---Picks up a spell book item, placing it on the cursor.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupSpellBookItem)
---@param spellBookItemIndex number The index of the spell in the spellbook.
---@param bookType string The type of book ("spell" or "pet").
function PickupSpellBookItem(spellBookItemIndex, bookType) end