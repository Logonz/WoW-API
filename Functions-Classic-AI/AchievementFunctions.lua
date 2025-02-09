---@meta

---Tracks an achievement in the UI.
---[Documentation](https://warcraft.wiki.gg/wiki/API_AddTrackedAchievement)
---@param achievementID number The ID of the achievement to track.
function AddTrackedAchievement(achievementID) end

---Returns the number of achievements currently being tracked.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetNumTrackedAchievements)
---@return number numTracked The number of achievements currently tracked.
function GetNumTrackedAchievements() end

---Returns a list of IDs for the player's tracked achievements.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_AchievementInfo.GetTrackedAchievements)
---@return number[] trackedAchievementIDs
function C_AchievementInfo.GetTrackedAchievements() end


---Returns whether an achievement is being tracked.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsTrackedAchievement)
---@param achievementID number
---@return boolean isTracked
function IsTrackedAchievement(achievementID) end



---Removes an achievement from the tracked achievements list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RemoveTrackedAchievement)
---@param achievementID number
function RemoveTrackedAchievement(achievementID) end
