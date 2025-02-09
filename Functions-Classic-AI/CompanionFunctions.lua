---@meta

---! DRAFT - NEEDS REVIEW
---Returns the cooldown details for a specified companion type.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCompanionCooldown)
---@param type string The type of companion ("MOUNT" or "CRITTER").
---@param index number The index of the companion.
---@return number start Start time of the cooldown.
---@return number duration Duration of the cooldown.
---@return boolean enable Indicates whether the cooldown is enabled.
function GetCompanionCooldown(type, index) end