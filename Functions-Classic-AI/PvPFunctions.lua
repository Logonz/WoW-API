---@meta

C_PvP = {}

---Returns the loss rewards for a Holiday Battleground.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetHolidayBGLossRewards)
---@return boolean hasRewards
---@return number honor
---@return number experience
function C_PvP.GetHolidayBGLossRewards() end

---Returns the holiday battleground rewards that are currently active. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetHolidayBGRewards)
---@return boolean hasRewards
---@return string rewardDetails
function C_PvP.GetHolidayBGRewards() end

---! DRAFT - NEEDS REVIEW  
---Retrieves the rewards for losing a random battleground.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetRandomBGLossRewards)  
---@return number honor  
---@return number experience  
function C_PvP.GetRandomBGLossRewards() end

---Returns the wait time for World PvP queues.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PvP.GetWorldPvPWaitTime)
---@param worldPvPID number
---@return number waitTime
function C_PvP.GetWorldPvPWaitTime(worldPvPID) end

---! DRAFT - NEEDS REVIEW
---Returns the rank progress of a player's PvP rank. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetInspectPVPRankProgress)
---@return number progress
function GetInspectPVPRankProgress() end

---Returns statistics from the previous week for the player in PvP.
---@return number honorableKills
---@return number dishonorableKills
---@return number honorPoints
---@return number factionStanding
function GetPVPLastWeekStats() end

---! DRAFT - NEEDS REVIEW  
---Returns information about a player's PVP rank. 
---@param rankIndex number
---@return string rankName
---@return string rankNumber
---@return number rankProgress
function GetPVPRankInfo(rankIndex) end

---Get the player's progress within their current PvP rank.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPVPRankProgress)
---@return number currentProgress
function GetPVPRankProgress() end

---Returns the player's PvP stats for the current week.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPVPThisWeekStats)
---@return number honorableKills
---@return number dishonorableKills
---@return number contributionPoints
function GetPVPThisWeekStats() end

---! DRAFT - NEEDs REVIEW
---Checks if the honor data for a unit is available.
---@return boolean hasData
function HasInspectHonorData() end

---Returns whether the current battleground is rated.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsRatedBattleground)
---@return boolean isRated
function IsRatedBattleground() end

---Requests honor data for a unit.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RequestInspectHonorData)
---@param unit Unit
function RequestInspectHonorData(unit) end

---! DRAFT - NEEDS REVIEW
---Returns the PVP rank of the specified unit. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_UnitPVPRank)
---@param unitID string
---@return number rank
function UnitPVPRank(unitID) end