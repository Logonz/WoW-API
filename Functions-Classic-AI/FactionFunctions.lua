---@meta

---Collapses a faction header row.
---Specifying a non-header row may produce unpredictable results. Triggers the UPDATE_FACTION event as faction indexes are adjusted.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CollapseFactionHeader)
---@param rowIndex number The row index of the header to collapse
function CollapseFactionHeader(rowIndex) end


---Expands a faction header row. The UPDATE_FACTION event is fired after expanding since faction indexes might shift.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandFactionHeader)
---@param rowIndex number The row index of the header to expand (Specifying a non-header row can have unpredictable results).
function ExpandFactionHeader(rowIndex) end


---Toggles the At War status for a faction.
---The UPDATE_FACTION event will be fired after the change.
---[Documentation](https://warcraft.wiki.gg/wiki/API_FactionToggleAtWar)
---@param rowIndex number The row index of the faction to toggle the At War status for. The row must have a true canToggleAtWar value.
function FactionToggleAtWar(rowIndex) end


---Returns the guild name and faction standing of the player.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetGuildFactionInfo)
---@return string guildName The name of the guild or the localized "Guild"
---@return string description A localized faction description
---@return number standingID Player's faction standing
---@return number barMin
---@return number barMax
---@return number barValue
function GetGuildFactionInfo() end


---Returns info for a faction by its index in the player's reputation pane.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetFactionInfo)
---@param factionIndex number Index from the currently displayed row in the player's reputation pane.
---@return string name Name of the faction.
---@return string description Description as shown in the detail pane for the faction.
---@return number standingID StandingId representing the current standing (e.g., 4 for Neutral).
---@return number barMin Minimum reputation since the beginning of Neutral to reach the current standing.
---@return number barMax Maximum reputation since the beginning of Neutral before advancing to the next standing.
---@return number barValue Total reputation earned with the faction.
---@return boolean atWarWith True if the player is at war with the faction.
---@return boolean canToggleAtWar True if the player can toggle the "At War" checkbox.
---@return boolean isHeader True if the faction is a header (collapsible group title).
---@return boolean isCollapsed True if the faction is a header and is currently collapsed.
---@return boolean hasRep True if the faction is a header and has its own reputation.
---@return boolean isWatched True if the "Show as Experience Bar" checkbox for the faction is checked.
---@return boolean isChild True if the faction is a second-level header or a child of one.
---@return number factionID Unique FactionID.
---@return boolean hasBonusRepGain True if bonus reputation gains with this faction are unlocked.
---@return boolean canSetInactive
function GetFactionInfo(factionIndex) end

---Returns the number of lines in the faction display. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumFactions)  
---@return number numFactions The number of lines in your faction display (based on known factions and expanded/collapsed faction lines).
function GetNumFactions() end

---Returns information for a faction based on its index or ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetFactionInfo)
---@param factionIndex number # The index from the currently displayed row in the player's reputation pane.
---@return string name # Name of the faction.
---@return string description # Description of the faction.
---@return number standingID # Current standing (e.g., 4 for Neutral).
---@return number barMin # Minimum reputation to reach the current standing.
---@return number barMax # Maximum reputation before advancing to the next standing.
---@return number barValue # Total reputation earned with the faction.
---@return boolean atWarWith # True if the player is at war with the faction.
---@return boolean canToggleAtWar # True if the "At War" checkbox can be toggled.
---@return boolean isHeader # True if the faction is a header.
---@return boolean isCollapsed # True if the header faction is collapsed.
---@return boolean hasRep # True if the faction is a header and has its own reputation.
---@return boolean isWatched # True if the faction is watched (shows as an experience bar).
---@return boolean isChild # True if a second-level header or its child.
---@return number factionID # Unique faction ID.
---@return boolean hasBonusRepGain # True if bonus reputation gains are available.
---@return boolean canSetInactive
function GetFactionInfo(factionIndex) end


---Returns info for the currently watched faction.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetWatchedFactionInfo)
---@return string? name The name of the faction currently being watched, nil if no faction is being watched.
---@return number standing The StandingId with the faction.
---@return number min The minimum bound for the current standing.
---@return number max The maximum bound for the current standing.
---@return number value The current faction level, within the bounds.
---@return number factionID Unique numeric identifier for the faction.
function GetWatchedFactionInfo() end


---Checks if a specified faction is marked as inactive.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsFactionInactive)
---@param index number @Index of the faction within the faction list, starting from 1.
---@return boolean? inactive @True if the faction is flagged as inactive, nil otherwise.
function IsFactionInactive(index) end


---Flags the specified faction as active in the reputation window.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetFactionActive)
---@param index number The index of the faction to mark active, ascending from 1.
function SetFactionActive(index) end


---Flags the specified faction as inactive in the reputation window.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetFactionInactive)
---@param index number The index of the faction to mark inactive, ascending from 1.
function SetFactionInactive(index) end


---! DRAFT - NEEDS REVIEW
---Sets the watched faction index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetWatchedFactionIndex)
---@param factionIndex number The index of the faction to watch.
function SetWatchedFactionIndex(factionIndex) end

