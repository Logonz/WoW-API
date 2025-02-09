---@meta

C_ChatInfo = {}

---Determines if a player can be reported for inappropriate behavior.
---@param playerName string
---@param reason string The reason for reporting
---@return boolean canReport
function C_ChatInfo.CanReportPlayer(playerName, reason) end


---! DRAFT - NEEDS REVIEW
---Reports the current server lag. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_ChatInfo.ReportServerLag)
function C_ChatInfo.ReportServerLag() end