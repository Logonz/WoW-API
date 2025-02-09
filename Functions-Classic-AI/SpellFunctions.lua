---@meta

---Returns true if the player character knows the specified spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Spell.DoesSpellExist)
---@param spellName string
---@return boolean spellExists
function C_Spell.DoesSpellExist(spellName) end


---Returns the ID of the spell that becomes available at the specified level.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrentLevelSpells)
---@param level number The level to query for a spell ID
---@return number spellID The ID of the spell available for that level
function GetCurrentLevelSpells(level) end


---Returns the number of ability tabs in the player's spellbook. 
---Profession tabs are not included in the count returned by this function.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumSpellTabs)
---@return number numTabs The number of ability tabs (e.g., "General", "Arcane").
function GetNumSpellTabs() end


---Returns the icon texture of a spellbook item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellBookItemTexture)
---@param spell number|string Spell ID or Name. The spell must be in your Spellbook if using a name.
---@return number icon FileID of the icon for the queried entry, or nil if not found.
function GetSpellBookItemTexture(spell) end


---Returns the name, sub-name, and spell ID of a spellbook item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellBookItemName)
---@param index number Spellbook slot index.
---@param bookType string 'BOOKTYPE_SPELL' or 'BOOKTYPE_PET' depending on the spellbook type.
---@return string spellName Name of the spell as it appears in the spellbook.
---@return string spellSubName Spell rank or sub-type, can be an empty string.
---@return number spellID ID of the spell.
function GetSpellBookItemName(index, bookType) end


---Returns the spell description for a given spell ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellDescription)
---@param spellID number
---@return string desc
function GetSpellDescription(spellID) end


---Returns the cooldown info of a spell. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellCooldown)
---@param spell number|string Spell ID or Name. When passing a name, requires the spell to be in your Spellbook.
---@return number startTime The time when the cooldown started; zero if no cooldown; current time if not enabled.
---@return number duration Cooldown duration in seconds, 0 if the spell is ready to be cast.
---@return number enabled 0 if the spell is active and cooldown will begin as soon as the spell is used; 1 otherwise.
---@return number modRate The rate at which the cooldown widget's animation should be updated.
function GetSpellCooldown(spell) end


---Returns info for a spellbook item based on the item name or index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellBookItemInfo)
---@param spellNameOrIndex string|number Either the spell name (string) or spellbook slot index (number).
---@param bookType? string Optional argument: "spell" or "pet" for the spellbook type.
---@return string spellType The type of the spell: "SPELL", "FUTURESPELL", "PETACTION", "FLYOUT".
---@return number id The ID related to the spell type, such as SpellID, ActionID, or FlyoutID.
function GetSpellBookItemInfo(spellNameOrIndex, bookType) end


---Returns the number of times a spell can be cast, mainly for spells limited by item reagents.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellCount)
---@param spell number|string Spell ID or Name; if name, must be in your Spellbook.
---@param index? number Spellbook slot index, ranging 1 to the total count across all tabs.
---@param bookType? string BOOKTYPE_SPELL or BOOKTYPE_PET; defaults to "spell" for non-"pet".
---@return number numCasts
function GetSpellCount(spell, index, bookType) end


---Returns true if a specified (pet) spell is autocastable. 
---As of patch 3.0.3, only spells in the pet spellbook can be autocast. Returns nil if the spell cannot be autocast or does not exist.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellAutocast)
---@param spellNameOrID string|number The spell name or numerical ID within the spellbook.
---@param bookType string Either "spell" for the spellbook or "pet" for pet spells.
---@return number? autocastable 1 if the spell is autocastable, nil otherwise.
---@return number? autostate 1 if the spell is currently set to autocast, nil otherwise.
function GetSpellAutocast(spellNameOrID, bookType) end


---Returns the hyperlink for a spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellLink)
---@param spell number|string - Spell ID or Name. When passing a name requires the spell to be in your Spellbook.
---@return string spellLink
---@return number spellID
function GetSpellLink(spell) end


---Returns info for the specified spellbook tab.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellTabInfo)
---@param tabIndex number The index of the tab, ascending from 1.
---@return string name The name of the spell line (e.g., General, Shadow, Fury).
---@return string texture The texture path for the spell line's icon.
---@return number offset Number of spell book entries before this tab.
---@return number numSlots The number of spell entries in this tab.
---@return boolean isGuild True if the tab is for Guild Perks.
---@return number offspecID Specialization ID for the specialization's spells.
function GetSpellTabInfo(tabIndex) end


---Returns resource cost info for a spell.
---Returns an empty table if the spell has no resource cost and reflects resource discounts provided by auras.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellPowerCost)
---@param spell number|string Spell ID or Name. When passing a name, the spell must be in your Spellbook.
---@return {minCost: number, cost: number, costPercent: number, costPerSec: number, type: Enum.PowerType, name: string, hasRequiredAura: boolean, requiredAuraID: number}[] costs
function GetSpellPowerCost(spell) end


---Returns information about the charges of a charge-accumulating player ability.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellCharges)
---@param spell number|string Spell ID or Name. Requires the spell to be in the Spellbook if passing a name.
---@param index number Spellbook slot index, ranging from 1 through the total number of spells across all tabs and pages.
---@param bookType string BOOKTYPE_SPELL or BOOKTYPE_PET depending on whether to query the player or pet spellbook.
---@return number currentCharges The number of charges currently available.
---@return number maxCharges The maximum number of charges available.
---@return number cooldownStart Time when the last charge cooldown began.
---@return number cooldownDuration Time required to gain a charge.
---@return number chargeModRate The rate at which the charge cooldown widget's animation updates.
function GetSpellCharges(spell, index, bookType) end


---Returns the icon texture of a spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellTexture)
---@param spell number|string - Spell ID or Name, requires the spell to be in your Spellbook when passing a name.
---@return number icon - fileID representing the icon texture used by the spell.
function GetSpellTexture(spell) end

---Returns the icon texture of a spell from the spellbook.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellTexture)
---@param index number - Spellbook slot index, ranging from 1 through the total number of spells across all tabs and pages.
---@param bookType string - Could be "spell" for player or "pet" for pet spellbook.
---@return number icon - fileID representing the icon texture used by the spell.
function GetSpellTexture(index, bookType) end


---Returns information about a loss-of-control cooldown affecting a spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellLossOfControlCooldown)
---@param spellSlot number Spell book slot index, ascending from 1.
---@param bookType? string Spell book type token, e.g., "spell" from player's spell book.
---@param spellName? string Name of a spell in the player's spell book.
---@param spellID? number Spell ID of a spell accessible to the player.
---@return number start The time when the loss-of-control cooldown began, per GetTime.
---@return number duration The duration of the loss-of-control cooldown in seconds; 0 if the spell is not currently affected.
function GetSpellLossOfControlCooldown(spellSlot, bookType, spellName, spellID) end


---Returns spell info including its name, icon, cast time, range, and more. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSpellInfo)
---@param spell number|string  # Spell ID or Name, which requires the spell to be in your Spellbook.
---@overload fun(index: number, bookType: string): string, string?, number, number, number, number, number, number
---@return string name  # The localized name of the spell.
---@return string? rank  # Always returns `nil`.
---@return number icon  # The spell icon texture (FileID).
---@return number castTime  # Cast time in milliseconds, or 0 for instant spells.
---@return number minRange  # Minimum range of the spell, or 0 if not applicable.
---@return number maxRange  # Maximum range of the spell, or 0 if not applicable.
---@return number spellID  # The ID of the spell.
---@return number originalIcon  # The original icon texture (FileID) for this spell.
function GetSpellInfo(spell) end


---Returns true if a spellbook item is the "Auto Attack" spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsAttackSpell)
---@param spellName string The spell name to test.
---@return boolean? isAttack Flag - Returns 1 if the spell is the "Attack" spell, nil otherwise.
function IsAttackSpell(spellName) end


---Returns true if the specified spell ID is currently being casted or queued.
---If the spell is current, the action bar indicates its slot with a highlighted frame.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsCurrentSpell)
---@param spellID number Spell ID to query.
---@return boolean isCurrent True if currently being casted or queued, false otherwise.
function IsCurrentSpell(spellID) end


---Returns true if the specified spell is a passive ability.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsPassiveSpell)
---@param spellId_or_index number Spell ID or spellbook slot index.
---@param bookType string Either "spell" for General Spellbook tab or "pet".
---@return boolean? isPassive 1 if the spell is passive, nil otherwise.
function IsPassiveSpell(spellId_or_index, bookType) end


---Returns 1 if the player is in range to use the specified spell on the target unit, otherwise returns 0 or nil if invalid.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsSpellInRange)
---@param spellName string The localized spell name, known by the player.
---@param unit string The UnitId of the target for the spell.
---@return number? inRange 1 if in range, 0 if not, nil if invalid.
function IsSpellInRange(spellName, unit) end


---Determines whether a spell can be used by the player character. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsUsableSpell)
---@param spell number|string Specifies the spell ID or name; name must be in your Spellbook.
---@return boolean usable Whether the spell is usable.
---@return boolean noMana Whether the spell cannot be cast due to low mana.
function IsUsableSpell(spell) end


---Places a spell onto the cursor. This function will put a spell on the mouse cursor using the spell ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupSpell)
---@param spellID number - The spell ID of the spell to pick up.
function PickupSpell(spellID) end


---Picks up a skill from the spellbook to place on an action bar. Cannot be used in combat.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PickupSpellBookItem)
---@param spell number|string The spell ID or name, requires the spell to be in your Spellbook.
---@overload fun(index: number, bookType: string)
function PickupSpellBookItem(spell) end

