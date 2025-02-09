---@meta

---Cancels a tracked buff.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CancelTrackingBuff)
---@param index number
function CancelTrackingBuff(index) end

---Returns information about the current spell being cast or channeled.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CastingInfo)
---@return string? spellName
---@return string? subText
---@return string? text
---@return number? startTime
---@return number? endTime
---@return boolean? isTradeSkill
---@return string? castID
---@return boolean? notInterruptible
---@return string? spellID
function CastingInfo() end

---Confirms the selection of a new key binding.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConfirmBinder)
function ConfirmBinder() end

---Converts the player's group into a party.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConvertToParty)
function ConvertToParty() end


---Converts the current party to a raid group.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConvertToRaid)
function ConvertToRaid() end


---Determines if the cursor can be placed in a specified equipment slot.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CursorCanGoInSlot)
---@param slotIndex number
---@return boolean canGoInSlot
function CursorCanGoInSlot(slotIndex) end

---Fills a table with class information including localized class names and file names.
---[Documentation](https://warcraft.wiki.gg/wiki/API_FillLocalizedClassList)
---@param classTable table<string, string> Table to be filled with class information
---@param isFemale? boolean If true, returns the female versions of the class names
function FillLocalizedClassList(classTable, isFemale) end

---Allows players to submit a bug report.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GMSubmitBug)
---@param bug string The description of the bug.
function GMSubmitBug(bug) end

---! DRAFT - NEEDS REVIEW
---Submits a suggestion to the game masters.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GMSubmitSuggestion)
---@param suggestion string The suggestion text
function GMSubmitSuggestion(suggestion) end

---! DRAFT - NEEDS REVIEW
---Retrieve the player's armor penetration percentage.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetArmorPenetration)
---@return number armorPenetration
function GetArmorPenetration() end

---Returns the index of the screen resolution currently in use.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrentResolution)
---@return number resolutionIndex
function GetCurrentResolution() end

---Returns the current direction of the eclipse power.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetEclipseDirection)
---@return number|null direction
function GetEclipseDirection() end

---Returns the player's expertise percentage.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetExpertisePercent)
---@return number offhandPercent
---@return number mainhandPercent
function GetExpertisePercent() end

---Retrieves referral information associated with a group or event invitation.
---! DRAFT - NEEDS REVIEW
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetInviteReferralInfo)
---@param inviteID number
---@return string name
---@return number level
---@return string class
---@return string area
---@return string gender
function GetInviteReferralInfo(inviteID) end

---Returns a list of available screen resolutions.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetScreenResolutions)
---@return string[] resolutions
function GetScreenResolutions() end

---Invites a player to the group by name or target.
---[Documentation](https://warcraft.wiki.gg/wiki/API_InviteUnit)
---@param name string
---@param reason? string
function InviteUnit(name, reason) end

---Returns whether the player is currently auto-attacking a target.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsPlayerAttacking)
---@return boolean isAutoAttacking
function IsPlayerAttacking() end

---Leaves the current party.
---[Documentation](https://warcraft.wiki.gg/wiki/API_LeaveParty)
function LeaveParty() end

---Requests to invite the specified unit to a group.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RequestInviteFromUnit)
---@param unit string
function RequestInviteFromUnit(unit) end

---Sets the screen resolution to the specified width and height.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetScreenResolution)
---@param width number The desired screen width
---@param height number The desired screen height
function SetScreenResolution(width, height) end

---! DRAFT - NEEDS REVIEW
---Determines if the player's user interface should display health for a given unit.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShouldKnowUnitHealth)
---@param unitToken string
---@return boolean shouldKnow
function ShouldKnowUnitHealth(unitToken) end

---Toggles the display of the player's cloak.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowCloak)
---@param show boolean
function ShowCloak(show) end

---Sets whether to display the player's helm.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowHelm)
---@param show boolean
function ShowHelm(show) end

---! DRAFT - NEEDS REVIEW
---Checks if the player's cloak is currently displayed.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowingCloak)
---@return boolean isShowing
function ShowingCloak() end

---Toggles the visibility of the player's helm.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowHelm)
---@param show boolean Indicates whether the helm should be shown (true) or hidden (false).
function ShowHelm(show) end

---Returns the attack speed and damage factor for both hands of a unit. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitAttackBothHands)
---@param unit string
---@return number speed
---@return number offhandSpeed
---@return number damageLow
---@return number damageHigh
---@return number offhandLow
---@return number offhandHigh
---@return number posBuff
---@return number negBuff
---@return number percent
function UnitAttackBothHands(unit) end


---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitAura)
---@param unit string
---@param index number
---@param filter string
---@return string name
---@return number icon
---@return number count
---@return string dispelType
---@return number duration
---@return number expirationTime
---@return string unitCaster
---@return boolean isStealable
---@return boolean nameplateShowPersonal
---@return boolean spellId
---@return boolean canApplyAura
---@return boolean isBossDebuff
---@return boolean castByPlayer
---@return boolean nameplateShowAll
---@return boolean timeMod
function UnitAura(unit, index, filter) end


---Returns information about the buffs on a specific unit.
---Only returns buffs that the player can detect.
---@param unit string
---@param index number
---@param filter string
---@return string? name
---@return integer? icon
---@return integer? count
---@return integer? debuffType
---@return integer? duration
---@return integer? expirationTime
---@return string? source
---@return integer? isStealable
---@return integer? nameplateShowPersonal
---@return integer? spellId
---@return boolean? canApplyAura
---@return boolean? isBossDebuff
---@return boolean? castByPlayer
---@return boolean? nameplateShowAll
---@return boolean? timeMod
---@return integer? value1
---@return integer? value2
---@return integer? value3
function UnitBuff(unit, index, filter) end

---Returns the total number of character points spent, used, and available.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitCharacterPoints)
---@param unit string
---@return number numPointsSpent
---@return number numPointsUsed
---@return number numPointsAvailable
function UnitCharacterPoints(unit) end

---Provides detailed information about a specific debuff on a unit.
---@param unitId string
---@param index number
---@param filter string
---@return string name
---@return string icon
---@return number count
---@return string debuffType
---@return number duration
---@return number expirationTime
---@return string unitCaster
---@return boolean canStealOrPurge
---@return boolean nameplateShowPersonal
---@return number spellId
---@return boolean canApplyAura
---@return boolean isBossAura
---@return boolean castByPlayer
---@return boolean nameplateShowAll
---@return number timeMod
---@return boolean value1
---@return boolean value2
---@return boolean value3
function UnitDebuff(unitId, index, filter) end

---! DRAFT - NEEDS REVIEW
---Returns a unit's defense-related statistics.
---[Documentation](https://wowpedia.fandom.com/wiki/API_UnitDefense)
---@param unit string
---@return number baseDefense
---@return number armorDefense
---@return number bonusDefense
---@return number bonusDefensePercent
function UnitDefense(unit) end

---Checks if the unit is in the same phase as the player.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitInPhase)
---@param unit string
---@return boolean inSamePhase
function UnitInPhase(unit) end

---Returns whether the specified unit is considered a civilian.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitIsCivilian)
---@param unit string
---@return boolean isCivilian
function UnitIsCivilian(unit) end

---Returns the ranged attack power for the unit.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitRangedAttack)
---@param unit string
---@return number attackPower
function UnitRangedAttack(unit) end

---Returns the resistance information for a specified unit and type.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitResistance)
---@param unit string
---@param school number
---@return number base
---@return number total
---@return number bonus
---@return number penalty
function UnitResistance(unit, school) end