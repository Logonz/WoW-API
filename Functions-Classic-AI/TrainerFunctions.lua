---@meta

---Returns the type of trainer spell in the trainer window.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsTrainerServiceLearnSpell)
---@param index number The index of the spell in the trainer window.
---@return number isLearnSpell Returns 1 if the spell is a class spell or a learnable profession spell, nil otherwise.
---@return number isPetLearnSpell Returns 1 if a pet spell, nil otherwise.
function IsTrainerServiceLearnSpell(index) end

