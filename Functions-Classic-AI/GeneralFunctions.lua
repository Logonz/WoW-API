---@meta

---Cancels the current tracking buff, such as Find Minerals or Track Humanoids.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CancelTrackingBuff)
function CancelTrackingBuff() end


---Confirms the binding setting.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConfirmBinder)
function ConfirmBinder() end


---Returns the player's currently casting spell.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CastingInfo)
---@return string name The name of the spell
---@return string text The name to be displayed
---@return number texture FileID of the spell texture
---@return number startTime Specifies when casting began in milliseconds
---@return number endTime Specifies when casting will end in milliseconds
---@return boolean isTradeSkill Indicates if the spell is related to a trade skill
---@return string castID Cast identifier, e.g., "Cast-3-4479-0-1318-2053-000014AD63"
---@return boolean? notInterruptible Always nil
---@return number spellID The spell's ID
function CastingInfo() end


---Converts the current party into a raid group. 
---Usually converts immediately unless in certain conditions like PartySync, where user confirmation is needed due to potential consequences. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PartyInfo.ConvertToRaid)
function C_PartyInfo.ConvertToRaid() end


---Converts a raid group with 5 or fewer members to a party. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConvertToParty)
function ConvertToParty() end


---Returns true if the item held by the cursor can be equipped in the specified inventory slot.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CursorCanGoInSlot)
---@param invSlot number @Inventory slot to query
---@return boolean? fitsInSlot @True if the cursor item can go into the specified slot, nil otherwise.
function CursorCanGoInSlot(invSlot) end


---Submits a user suggestion feedback.
---Replaces the function `GMSubmitSuggestion`.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_UserFeedback.SubmitSuggestion)
---@param suggestion string
---@return boolean success
function C_UserFeedback.SubmitSuggestion(suggestion) end


---Submits a bug report to the user feedback system.
---Replaces `GMSubmitBug`.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_UserFeedback.SubmitBug)
---@param bugInfo string The description of the bug
---@param suppressNotification? boolean Optional, whether to suppress notification; defaults to false
---@return boolean success Returns true if the submission was successful
function C_UserFeedback.SubmitBug(bugInfo, suppressNotification) end


---Fills a table with localized male or female class names.
---The function takes a table and optionally a boolean to specify if female class names should be used.
---[Documentation](https://warcraft.wiki.gg/wiki/API_FillLocalizedClassList)
---@param classTable table The table to be filled with data.
---@param isFemale? boolean If true, fills the table with female class names.
---@return table classTable The same table that was passed in.
function FillLocalizedClassList(classTable, isFemale) end


---Returns the percentage of target's armor your physical attacks ignore due to armor penetration.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetArmorPenetration)
---@return number armorPen Percent of armor ignored by your physical attacks.
function GetArmorPenetration() end


---Returns the index of the current screen resolution. This index corresponds to one of the resolutions provided by GetScreenResolutions().
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCurrentResolution)
---@return number index The index of the current resolution
function GetCurrentResolution() end


---Returns your current expertise reduction to chance to be dodged or parried, in percent.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetExpertisePercent)
---@return number expertisePercent Percentage reduction in dodge and parry chances for swings with your main hand weapon.
---@return number offhandExpertisePercent Percentage reduction in dodge and parry chances for swings with your offhand weapon.
function GetExpertisePercent() end


---Indicates which Eclipse state the player is moving towards.
---@return '"moon"'|'"sun"'|'"none"' direction Which Eclipse state the player is moving towards.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetEclipseDirection)
function GetEclipseDirection() end


---Returns info for Quick join invites.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PartyInfo.GetInviteReferralInfo)
---@param inviteGUID string
---@return string outReferredByGuid
---@return string outReferredByName
---@return Enum.PartyRequestJoinRelation outRelationType
---@return boolean outIsQuickJoin
---@return string outClubId
function C_PartyInfo.GetInviteReferralInfo(inviteGUID) end


---Returns a list of available preset windowed screen resolutions.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetScreenResolutions)
---@return string resolutionN An available screen resolution as ___x___ (width "x" height).
function GetScreenResolutions() end


---Invites a player to join your party.
---[Documentation](https://warcraft.wiki.gg/wiki/API_InviteUnit)
---@param playerName string The name of the player you would like to invite to a group.
function InviteUnit(playerName) end


---Returns if the player is melee attacking the specified unit.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsPlayerAttacking)
---@param unit string The UnitId of the unit to check.
---@return boolean isAttacking If the player is attacking the specified unit.
function IsPlayerAttacking(unit) end


---Leaves the current party.
---[Documentation](https://warcraft.wiki.gg/wiki/API_LeaveParty)
function LeaveParty() end


---Attempts to request an invite into the target party.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RequestInviteFromUnit)
---@param targetName string
function RequestInviteFromUnit(targetName) end


---Sets the screen resolution to the specified index.
---Passing nil defaults to the lowest resolution available.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetScreenResolution)
---@param index number? Specifies the new screen resolution as the index of a value from GetScreenResolutions().
function SetScreenResolution(index) end

---! DRAFT - NEEDS REVIEW
---Checks if the unit health is known. 
---[Documentation Unavailable]
---@param unit string
---@return boolean isKnown
function ShouldKnowUnitHealth(unit) end
---! DRAFT - NEEDS REVIEW  
---The function ShowHelm likely controls the visibility of the player's helm in the game.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowHelm)  
---@param show boolean Indicates whether the helm should be shown or not  
function ShowHelm(show) end

---! DRAFT - NEEDS REVIEW
---Toggles the visibility of the player's cloak.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowCloak)
---@param show boolean
function ShowCloak(show) end

---! DRAFT - NEEDS REVIEW
---This function displays or hides the character's helm in World of Warcraft.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowingHelm)
---@param toggle boolean Determines whether to show or hide the helm
---@return boolean success Indicates if the operation was successful
function ShowingHelm(toggle) end
---! DRAFT - NEEDS REVIEW
---Returns information if the cloak is being shown for a player.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ShowingCloak)
---@param unit string The unit identifier (e.g., player or target).
---@return boolean isShowing true if the cloak is shown, false otherwise.
function ShowingCloak(unit) end
---! DRAFT - NEEDS REVIEW
---Performs an attack with both hands of a unit, but further details are not provided.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitAttackBothHands)
---@param unit string The unit to attack with both hands.
---@return boolean success True if the attack was successful, false otherwise.
function UnitAttackBothHands(unit) end
---! DRAFT - NEEDS REVIEW
---Representation of unit character points.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitCharacterPoints)
---@param unit string
---@return number total
---@return number spent
---@return number available
function UnitCharacterPoints(unit) end
---! DRAFT - NEEDS REVIEW
---Determines if a unit is currently in a different phase.
---[Documentation Unavailable](https://warcraft.wiki.gg/wiki/API_UnitInPhase)
---@param unit string
---@return boolean inPhase
function UnitInPhase(unit) end

---! DRAFT - NEEDS REVIEW
---Checks if a unit is a civilian. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitIsCivilian)
---@param unit string
---@return boolean isCivilian
function UnitIsCivilian(unit) end

---! DRAFT - NEEDS REVIEW
---Retrieves the defense stats of a specified unit.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitDefense)
---@param unit string The target unit to query defense stats from
---@return number defenseValue The total defense value of the unit
---@return number effectiveArmor The effective armor value contributing to defense
---@return number baseValue The base defense value of the unit
---@return number bonusValue The bonus defense value of the unit
function UnitDefense(unit) end
---! DRAFT - NEEDS REVIEW
---Provides details about a unit's debuff.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitDebuff)
---@param unit string The unit's ID
---@param index number The index of the debuff
---@param filter string? (optional) A filter to apply to the debuff list
---@return string name
---@return string icon
---@return number count
---@return string debuffType
---@return number duration
---@return number expirationTime
---@return string sourceUnit
---@return boolean isStealable
---@return boolean nameplateShowPersonal
---@return number spellId
---@return boolean canApplyAura
---@return boolean isBossDebuff
---@return boolean castByPlayer
---@return boolean nameplateShowAll
---@return boolean timeMod
function UnitDebuff(unit, index, filter) end
---! DRAFT - NEEDS REVIEW
---Encounters a web request handling issue with the Warcraft Wiki.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitResistance)
function UnitResistance() end
---! DRAFT - NEEDS REVIEW
---Retrieves the details of a specified unit's buff.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitBuff)
---@param unit string The unit to query.
---@param index number The index of the buff to retrieve.
---@param filter string? A filter to apply to the buff list.
---@return string name The name of the buff.
---@return string icon The icon path of the buff.
---@return number count The number of stacks of the buff.
---@return number debuffType The debuff type, if applicable.
---@return number duration The duration of the buff in seconds.
---@return number expirationTime The time at which the buff will expire, in seconds since the epoch.
---@return string unitCaster The unit that cast the buff.
---@return boolean isStealable Whether the buff is stealable.
---@return boolean shouldConsolidate Whether the buff should be consolidated.
---@return boolean spellID The spell ID of the buff.
---@return boolean canApplyAura Whether the buff can be applied to the aura.
---@return boolean isBossDebuff Whether the buff is a boss debuff.
function UnitBuff(unit, index, filter) end
---! DRAFT - NEEDS REVIEW
---Gets the aura details for a specified unit.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitAura)
---@param unit string The unit ID to inspect.
---@param index number The aura index to fetch.
---@param filter string Optional filter to apply to the aura search.
---@return string name The name of the aura.
---@return number icon The icon ID of the aura.
---@return number count The number of stacks of the aura.
---@return string debuffType The type of debuff (if any).
---@return number duration The total duration of the aura.
---@return number expirationTime The time at which the aura will expire.
---@return string source The unit that applied the aura.
---@return boolean isStealable If the aura can be stolen.
---@return boolean nameplateShowPersonal Whether it shows on personal nameplates.
---@return boolean spellId The spell ID of the aura.
---@return boolean canApplyAura If you can apply this aura.
---@return boolean isBossDebuff If this is a boss debuff.
---@return boolean castByPlayer If the aura was cast by a player.
---@return number nameplateShowAll If aura shows on nameplate.
---@return number timeMod The time modification applied to the aura.
function UnitAura(unit, index, filter) end

---Returns the unit's ranged attack base and its modifier.
---This API is only available in Cata Classic and Classic Era.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitRangedAttack)
---@param unit string A UnitId, likely only works for "player" and "pet".
---@return number base The unit's base ranged attack number (0 if no ranged weapon is equipped).
---@return number modifier The total effect of all modifiers (positive and negative) to ranged attack.
function UnitRangedAttack(unit) end

