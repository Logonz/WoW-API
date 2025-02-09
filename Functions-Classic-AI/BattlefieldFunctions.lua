---@meta

---Returns the position coordinates of specified battlefield flag. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBattlefieldFlagPosition)
---@return number|nil flagX
---@return number|nil flagY
function GetBattlefieldFlagPosition() end

---Returns detailed info about a specific battlefield instance.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBattlefieldInstanceInfo)
---@param instanceIndex number
---@return string battlefieldName
---@return string instanceID
---@return number levelRangeMin
---@return number levelRangeMax
---@return number teamSize
---@return boolean registeredMatch
---@return number playTime
---@return string battlefieldType
function GetBattlefieldInstanceInfo(instanceIndex) end

---! DRAFT - NEEDS REVIEW
---Returns information about a specific battleground statistic.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBattlefieldStatInfo)
---@param index number
---@param battlegroundID number
---@return string statName
---@return number statValue
function GetBattlefieldStatInfo(index, battlegroundID) end


---Returns the number of statistics available for a battlefield.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumBattlefieldStats)
---@return number numStats
function GetNumBattlefieldStats() end


---Returns the number of battlefields. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumBattlefields)
---@return number numBattlefields
function GetNumBattlefields() end


---Returns information about the selected battlefield.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSelectedBattlefield)
---@return number index
---@return boolean isActive
---@return boolean isQueue
function GetSelectedBattlefield() end


---! DRAFT - NEEDS REVIEW
---Checks if the player is currently in an inactive battlefield.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_InActiveBattlefield)
---@return boolean isActive
function InActiveBattlefield() end


---Sets the selected battlefield index. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSelectedBattlefield)
---@param index number The index of the battlefield to select
---@param isParty boolean Whether to select for the entire party
function SetSelectedBattlefield(index, isParty) end
