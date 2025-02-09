---@meta

---! DRAFT - NEEDS REVIEW  
---Returns the rewards for losing a Holiday Battleground. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetHolidayBGLossRewards)
---@return number honor
---@return number experience
---@return BattlefieldItemReward[]? itemRewards
---@return BattlefieldCurrencyReward[]? currencyRewards
---@return RoleShortageReward? roleShortageBonus
function C_PvP.GetHolidayBGLossRewards() end


---Retrieves rewards for the Holiday Battleground event. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetHolidayBGRewards)
---@return number honor
---@return number experience
---@return BattlefieldItemReward[]? itemRewards
---@return BattlefieldCurrencyReward[]? currencyRewards
---@return RoleShortageReward? roleShortageBonus
function C_PvP.GetHolidayBGRewards() end


---! DRAFT - NEEDS REVIEW
---Returns various rewards for losing a random Battleground match.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetRandomBGLossRewards)
---@return number honor
---@return number experience
---@return BattlefieldItemReward[]? itemRewards
---@return BattlefieldCurrencyReward[]? currencyRewards
---@return RoleShortageReward? roleShortageBonus
function C_PvP.GetRandomBGLossRewards() end


---! DRAFT - NEEDS REVIEW
---Returns the world PvP wait time for a specified index.
---This function is available in Cata Classic and Classic Era versions only.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetWorldPvPWaitTime)
---@param index number
---@return number pvpWaitTime
function C_PvP.GetWorldPvPWaitTime(index) end


---Gets the inspected unit's progress towards the next PvP rank.
---Requires inspecting a unit and calling GetInspectHonorData() for accurate results.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetInspectPVPRankProgress)
---@return number rankProgress The progress towards the next PVP rank, normalized between 0 and 1
function GetInspectPVPRankProgress() end


---Returns the player's progress towards the next PvP rank, normalized between 0 and 1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPVPRankProgress)
---@return number progress Progress towards the next rank
function GetPVPRankProgress() end


---Gets your PVP contribution statistics for the current week.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPVPThisWeekStats)
---@return number hk The number of honorable kills.
---@return number contribution The estimated honor points made.
function GetPVPThisWeekStats() end


---Returns information about a specific PvP rank. Only available in Cata Classic and Classic Era.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPVPRankInfo)
---@param rankID number - The PvP rank ID as returned by UnitPVPRank()
---@param faction? number - 0 for Horde, 1 for Alliance. Defaults to the player's faction.
---@return string rankName - The localized name of the PvP rank.
---@return number rankNumber - The PvP rank number.
function GetPVPRankInfo(rankID, faction) end


---Gets the player's PVP contribution statistics for the previous week.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPVPLastWeekStats)
---@return number hk The number of honorable kills.
---@return number dk The number of dishonorable kills.
---@return number contribution The estimated number of honor contribution points.
---@return number rank The honor rank the player had.
function GetPVPLastWeekStats() end


---Determine if the inspected unit's honor data has been loaded.
---[Documentation](https://warcraft.wiki.gg/wiki/API_HasInspectHonorData)
---@return boolean hasData Whether the currently inspected unit's honor data has been loaded.
function HasInspectHonorData() end


---Determines if the current battleground is a rated battleground.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.IsRatedBattleground)
---@return boolean isRatedBattleground
function C_PvP.IsRatedBattleground() end


---Requests PvP participation information for the currently inspected target.
---INSPECT_HONOR_UPDATE fires when the requested information is available.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RequestInspectHonorData)
function RequestInspectHonorData() end


---Returns the specified unit's PvP rank ID. The ID starts at 5 for the first rank and returns 0 if the unit has no rank. This can be used in GetPVPRankInfo() to retrieve rank details.
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitPVPRank)
---@param unit string
---@return number rankID
function UnitPVPRank(unit) end

