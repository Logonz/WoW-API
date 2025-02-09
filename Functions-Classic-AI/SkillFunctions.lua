---@meta

---! DRAFT - NEEDS REVIEW
---Collapses a skill header in the skill window, hiding its sub-skills.
---@param skillHeaderID number
function CollapseSkillHeader(skillHeaderID) end

---Collapses the specified skill line in the trainer skill list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CollapseTrainerSkillLine)
---@param skillLine number
function CollapseTrainerSkillLine(skillLine) end


---Expands the skill header to show its contained skills. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandSkillHeader)
---@param skillHeaderID number
function ExpandSkillHeader(skillHeaderID) end


---Expands a trainer skill line.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandTrainerSkillLine)
---@param index number
function ExpandTrainerSkillLine(index) end

---Returns the number of skill lines.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumSkillLines)
---@return number numSkillLines
function GetNumSkillLines() end

---! DRAFT - NEEDS REVIEW
---Returns details about the currently selected skill. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSelectedSkill)
---@return number skillIndex
function GetSelectedSkill() end


---Returns information about a specified skill line.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetSkillLineInfo)
---@param skillLineID number
---@return string name
---@return number headerType
---@return number rank
---@return number maxRank
---@return boolean isAbandonable
---@return boolean isHeader
---@return number skillIndex
---@return boolean isExpanded
---@return boolean isGuild
---@return number numSkillUps
function GetSkillLineInfo(skillLineID) end



---Sets the currently selected skill index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSelectedSkill)
---@param skillIndex number
function SetSelectedSkill(skillIndex) end
