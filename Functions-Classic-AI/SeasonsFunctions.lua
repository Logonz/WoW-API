---@meta

---Returns true if the player is on a seasonal realm.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Seasons.HasActiveSeason)
---@return boolean active True if the player is on a seasonal realm, otherwise false.
function C_Seasons.HasActiveSeason() end


---Returns the ID of the season that is active on the current realm.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_Seasons.GetActiveSeason)
---@return Enum.SeasonID? seasonID The currently active season ID, if one is active.
function C_Seasons.GetActiveSeason() end

