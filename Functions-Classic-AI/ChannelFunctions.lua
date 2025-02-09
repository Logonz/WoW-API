---@meta

---Returns the player's currently channeling spell details.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ChannelInfo)
---@return string|nil name The name of the spell, or nil if no spell is being channeled.
---@return string text The name to be displayed.
---@return number texture FileID of the spell's texture.
---@return number startTime When channeling began in milliseconds.
---@return number endTime When channeling will end in milliseconds.
---@return boolean isTradeSkill Whether it's a trade skill spell.
---@return boolean? notInterruptible Always nil.
---@return number spellID The ID of the spell.
function ChannelInfo() end

