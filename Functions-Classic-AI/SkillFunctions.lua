---@meta

---Collapses a header in the trainer window, hiding all spells below it.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CollapseTrainerSkillLine)
---@param index number The index of a line in the trainer window (if not a header, an error is produced). Index 0 ("All") collapses all headers.
function CollapseTrainerSkillLine(index) end


---Collapses a header in the skills window.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CollapseSkillHeader)
---@param index number The index of a line in the skills window, can be a header or skill line belonging to a header. Index 0 ("All") will collapse all headers.
function CollapseSkillHeader(index) end


---Expands a header in the skills window using the specified index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandSkillHeader)
---@param index number The index of a line in the skills window. Index 0 ("All") will expand all headers.
function ExpandSkillHeader(index) end


---Expands a header in the trainer window, showing all spells below it.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandTrainerSkillLine)
---@param index number The index of a line in the trainer window. An error is produced if the index is not a header.
function ExpandTrainerSkillLine(index) end


---! DRAFT - NEEDS REVIEW
---Returns the number of skill lines in the skill window, including headers.
---Removed in Patch 4.0.1.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumSkillLines)
---@return number numSkills
function GetNumSkillLines() end


---Returns the currently selected skill line if available in Cata Classic and Classic Era.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSelectedSkill)
---@return number skillIndex
function GetSelectedSkill() end


---Returns information on a skill line or header.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSkillLineInfo)
---@param index number The index of a line in the skills window, can be a header or skill line.
---@return string skillName Name of the skill line.
---@return number|nil header Returns 1 if the line is a header, nil otherwise.
---@return number|nil isExpanded Returns 1 if the line is a header and expanded, nil otherwise.
---@return number skillRank The current rank for the skill, 0 if not applicable.
---@return number numTempPoints Temporary points for the current skill.
---@return number skillModifier Skill modifier value for the current skill.
---@return number skillMaxRank The maximum rank for the current skill.
---@return number|nil isAbandonable Returns 1 if this skill can be unlearned, nil otherwise.
---@return number|nil stepCost Returns 1 if skill can be learned, nil otherwise.
---@return number|nil rankCost Returns 1 if skill can be trained, nil otherwise.
---@return number minLevel Minimum level required to learn this skill.
---@return number skillCostType 
---@return string skillDescription Localized skill description text.
function GetSkillLineInfo(index) end

---! DRAFT - NEEDS REVIEW
---Sets the selected skill for a given parameter.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSelectedSkill)
---@param param1 unknown
---@return unknown
function SetSelectedSkill(param1) end
