---@meta

---Used to position the flag icon on the world map and the battlefield minimap.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBattlefieldFlagPosition)
---@param index number Index to get the flag position from
---@return number flagX Position of the flag on the map
---@return number flagY Position of the flag on the map
---@return string flagToken Name of flag texture in Interface\WorldStateFrame\
function GetBattlefieldFlagPosition(index) end


---Returns the battlefield instance ID for an index in the battlemaster listing. The function is used within Cata Classic and Classic Era.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBattlefieldInstanceInfo)
---@param index number The battlefield instance index, from 1 to GetNumBattlefields().
---@return number instanceID The battlefield instance ID.
function GetBattlefieldInstanceInfo(index) end


---Gets the list of battleground-specific columns on the scoreboard.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetBattlefieldStatInfo)
---@param index number Column to get data for
---@return string name Name of the column (e.g., Flags Captured)
---@return string icon Icon displayed on the scoreboard (e.g., Horde flag icon)
---@return string tooltip Tooltip displayed when hovering over a column's name
function GetBattlefieldStatInfo(index) end


---Returns the number of custom columns in the battleground scoreboard.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumBattlefieldStats)
---@return number numStats Number of columns available for the battleground.
function GetNumBattlefieldStats() end


---Returns the number of available instances for the selected battleground at the battlemaster.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumBattlefields)
---@return number numBattlefields
function GetNumBattlefields() end


---Returns the currently selected battlefield instance index at the battlemaster.
---The zeroth index refers to "First Available".
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSelectedBattlefield)
---@return number selectedIndex The index of the selected battlefield instance.
function GetSelectedBattlefield() end


---Returns whether the player is currently in an active battlefield.
---[Documentation](https://warcraft.wiki.gg/wiki/API_InActiveBattlefield)
---@return boolean inBattlefield True if the player is in an active battlefield, false otherwise.
function InActiveBattlefield() end

---! DRAFT - NEEDS REVIEW
---Sets the selected battlefield by index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSelectedBattlefield)
---@param battlefieldIndex number The index of the battlefield to select.
function SetSelectedBattlefield(battlefieldIndex) end
