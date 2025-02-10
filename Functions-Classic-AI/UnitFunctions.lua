---@meta
--* GENERATED BY gemini-2.0-flash

---Returns information about the unit's melee attacks.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 8.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitAttackBothHands)
---@param unit string UnitId - Tested with "player" and "target".
---@return number mainBase The unit's base main hand weapon skill (not rating).
---@return number mainMod Any modifier to the unit's main hand weapon skill (not rating).
---@return number offBase The unit's base offhand weapon skill (not rating)(equal to unarmed weapon skill if unit doesn't dual wield).
---@return number offMod Any modifier to the unit's offhand weapon skill (not rating).
function UnitAttackBothHands(unit) end

---Returns the buffs/debuffs for the unit.<br>
---Replaced by C_UnitAuras.GetAuraDataByIndex in Patch 10.2.5 and will be removed in patch 11.0.2.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitAura)
---@param unit string The unit to query.
---@param index number Index of an aura to query.
---@param filter string? A list of filters, separated by pipe chars or spaces. Otherwise defaults to "HELPFUL".
---@return string name The localized name of the aura, otherwise nil if there is no aura for the index.
---@return number icon The icon texture.
---@return number count The amount of stacks, otherwise 0.
---@return string? dispelType The locale-independent magic type of the aura: Curse, Disease, Magic, Poison, otherwise nil.
---@return number duration The full duration of the aura in seconds.
---@return number expirationTime Time the aura expires compared to GetTime(), e.g. to get the remaining duration: expirationtime - GetTime()
---@return string source The unit that applied the aura.
---@return boolean isStealable True if the aura may be stolen.
---@return boolean nameplateShowPersonal True if this aura should only be shown on nameplates if it was applied by you, i.e. the caster unit id is player, pet or vehicle.
---@return number spellId The spell ID for e.g. GetSpellInfo()
---@return boolean canApplyAura True if the player can apply the aura.
---@return boolean isBossDebuff True if the aura was cast by a boss.
---@return boolean castByPlayer True if the aura was applied by a player.
---@return boolean nameplateShowAll True if this aura should always be shown irrespective of any usual filtering logic.
---@return number timeMod The scaling factor used for displaying time left.
---@return boolean shouldConsolidate Whether to consolidate auras, only exists in Classic Era/Wrath.
---@return any ... Variable returns - Some auras return additional values that typically correspond to something shown in the tooltip, such as the remaining strength of an absorption effect.
function UnitAura(unit, index, filter) end

---Needs summary.<br>
---C_UnitAuras.GetBuffDataByIndex is an alias for C_UnitAuras.GetAuraDataByIndex(unit, index, "HELPFUL"), returning only buffs and ignores any HARMFUL filter.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_UnitAuras.GetBuffDataByIndex)
---@param unitToken string UnitToken
---@param index number
---@param filter string? A list of filters, separated by pipe chars or spaces. Otherwise defaults to "HELPFUL".
---@return AuraData? aura
function C_UnitAuras.GetBuffDataByIndex(unitToken, index, filter) end

---Returns the number of unspent talent points of the player.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 4.0.1.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitCharacterPoints)
---@param unit string UnitId - Only works on the player unit.
---@return number talentPoints - The quantity of unspent talent points the unit has available.
function UnitCharacterPoints(unit) end

---Needs summary.<br>
---C_UnitAuras.GetDebuffDataByIndex is an alias for C_UnitAuras.GetAuraDataByIndex(unit, index, "HARMFUL"), returning only debuffs and ignores any HELPFUL filter.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_UnitAuras.GetDebuffDataByIndex)
---@param unitToken string UnitToken
---@param index number
---@param filter string? A list of filters, separated by pipe chars or spaces. Otherwise defaults to "HARMFUL".
---@return AuraData? aura
function C_UnitAuras.GetDebuffDataByIndex(unitToken, index, filter) end

---Returns the defense of the unit without armor, and defense value of their armor.<br>
---For NPCs and pets, it will return a baseDefense value, though armorDefense will be 0.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitDefense)
---@param unit string The unit to query.
---@return number baseDefense The unit's defense without armor.
---@return number armorDefense The defense gained from the unit's armor.
function UnitDefense(unit) end

---Returns if a unit is in the same phase.<br>
---Replaced with <a href="/wiki/API_UnitPhaseReason" title="API UnitPhaseReason">UnitPhaseReason</a>() in Patch 9.0.1.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitInPhase)
---@param unit string UnitId
---@return boolean inPhase
function UnitInPhase(unit) end

---Determine whether a unit is a civilian (low level enemy faction NPC that counts as a dishonorable kill).<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 2.3.0.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitIsCivilian)
---@param unit string Only works on enemy faction NPCs.
---@return boolean
function UnitIsCivilian(unit) end

---Returns the unit's ranged attack and modifier.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 8.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitRangedAttack)
---@param unit string UnitId - Likely only works for "player" and "pet"
---@return number base - The unit's base ranged attack number (0 if no ranged weapon is equipped)
---@return number modifier - The total effect of all modifiers (positive and negative) to ranged attack.
function UnitRangedAttack(unit) end

---Gets information about a unit's resistance.<br>
---This API only exists in Cata Classic and Classic Era. Removed in Patch 8.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitResistance)
---@param unit string The unit to query.
---@param resistanceIndex number The index of the resistance type to check (0: Armor, 1: Holy, 2: Fire, 3: Nature, 4: Frost, 5: Shadow, 6: Arcane).
---@return number base The base resistance
---@return number total The current total value after all modifiers
---@return number bonus The bonus resistance modifier total from gear and buffs
---@return number minus The negative resistance modifier total from gear and buffs
function UnitResistance(unit, resistanceIndex) end

