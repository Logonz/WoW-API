---@meta

---Returns cooldown information about a specific companion type like "CRITTER" or "MOUNT".
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCompanionCooldown)
---@param companionType string Companion type, either "CRITTER" or "MOUNT".
---@param id number Slot ID to query starting from 1.
---@return number startTime The time the cooldown period began.
---@return number duration The duration of the cooldown period.
---@return number isEnabled 1 if the companion has a cooldown, otherwise 0.
function GetCompanionCooldown(companionType, id) end

