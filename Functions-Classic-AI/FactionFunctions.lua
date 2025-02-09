---@meta

---Collapses a faction header in the reputation interface.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CollapseFactionHeader)
---@param rowIndex number The index of the faction header to collapse.
function CollapseFactionHeader(rowIndex) end

---Expands a collapsible faction header in the reputation interface.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandFactionHeader)
---@param rowIndex number The index of the faction header to expand
function ExpandFactionHeader(rowIndex) end

---! DRAFT - NEEDS REVIEW  
---Toggles the "At War" status with a faction.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_FactionToggleAtWar)  
---@param factionIndex number  
function FactionToggleAtWar(factionIndex) end

---Provides information about a faction.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetFactionInfo)
---@param factionIndex number
---@return string name
---@return string description
---@return number standingID
---@return number barMin
---@return number barMax
---@return number barValue
---@return string atWarWith
---@return string canToggleAtWar
---@return boolean isHeader
---@return boolean isCollapsed
---@return number hasRep
---@return boolean isWatched
function GetFactionInfo(factionIndex) end

---Returns information about a faction by its ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetFactionInfoByID)
---@param factionID number
---@return string name
---@return string description
---@return string standingText
---@return number barMin
---@return number barMax
---@return number barValue
---@return number atWarWith
---@return number canToggleAtWar
---@return boolean isHeader
---@return boolean isCollapsed
---@return boolean hasRep
---@return boolean isWatched
---@return number isChild
function GetFactionInfoByID(factionID) end


---Returns faction info of the player's guild.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetGuildFactionInfo)
---@return number standingID
---@return number barMin
---@return number barMax
---@return number barValue
function GetGuildFactionInfo() end


---Returns the number of factions the player has encountered.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumFactions)
---@return number numFactions The total number of factions.
function GetNumFactions() end

---Returns information about the faction that is currently being watched for reputation gains.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetWatchedFactionInfo)
---@return string? name
---@return number? standingID
---@return number? barMin
---@return number? barMax
---@return number? barValue
function GetWatchedFactionInfo() end

---Checks if a faction is marked as inactive. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsFactionInactive)
---@param factionIndex number
---@return boolean isInactive
function IsFactionInactive(factionIndex) end

---Sets the specified faction as active.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetFactionActive)
---@param factionIndex number
function SetFactionActive(factionIndex) end


---Sets a faction as inactive.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetFactionInactive)
---@param factionIndex number
function SetFactionInactive(factionIndex) end



---Sets the watched faction by its index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetWatchedFactionIndex)
---@param factionIndex number The index of the faction to watch
function SetWatchedFactionIndex(factionIndex) end
