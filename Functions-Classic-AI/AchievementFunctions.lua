---@meta

---Tracks an achievement.
---A maximum of 10 tracked achievements can be displayed by the WatchFrame at a time.
---[Documentation](https://warcraft.wiki.gg/wiki/API_AddTrackedAchievement)
---@param achievementID number # ID of the achievement to add to tracking.
function AddTrackedAchievement(achievementID) end


---Returns the number of achievements you are currently tracking, up to 10.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumTrackedAchievements)
---@return number numTracked
function GetNumTrackedAchievements() end


---Returns the currently tracked achievements. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTrackedAchievements)
---@return number ... List of achievement IDs currently being tracked, up to a maximum of 10.
function GetTrackedAchievements() end


---Returns if an achievement is currently being tracked.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsTrackedAchievement)
---@param achievementID number Uniquely identifies each achievement
---@return boolean eligible
function IsTrackedAchievement(achievementID) end


---Untracks an achievement from the WatchFrame.
---[Documentation](https://warcraft.wiki.gg/wiki/API_RemoveTrackedAchievement)
---@param achievementID number ID of the achievement to be removed from tracking.
function RemoveTrackedAchievement(achievementID) end

