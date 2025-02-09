---@meta

---Closes an open trade skill window.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CloseTradeSkill)
function CloseTradeSkill() end


---Performs the tradeskill a specified number of times.
---[Documentation](https://warcraft.wiki.gg/wiki/API_DoTradeSkill)
---@param index number The index of the tradeskill recipe.
---@param repeat number The number of times to repeat the creation of the specified recipe.
function DoTradeSkill(index, repeat) end


---Expands a header within a tradeskill window in World of Warcraft.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandTradeSkillSubClass)
---@param index number — Index within the tradeskill window
function ExpandTradeSkillSubClass(index) end


---Returns the index of the first non-header trade skill entry.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetFirstTradeSkill)
---@return number skillId The ID of the first visible non-header trade skill entry.
function GetFirstTradeSkill() end


---Returns the number of trade skill entries, including headers.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumTradeSkills)
---@return number numSkills - The number of trade skills which are available, including headers.
function GetNumTradeSkills() end


---Returns the description for a given recipe.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillDescription)
---@param recipeID number
---@return string description
function GetTradeSkillDescription(recipeID) end


---Returns the visibility status of a trade skill inventory slot.
---Whether the slot for slotIndex is visible (1) or not (nil).
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillInvSlotFilter)
---@param slotIndex number
---@return number|nil isVisible
function GetTradeSkillInvSlotFilter(slotIndex) end


---Returns the item link string for a specified trade skill item.
---Requires the Trade Skill window to be open, and indexes start at 1. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillItemLink)
---@param skillId number The ID specifying which trade skill's link to get.
---@return string link An item link string representing the trade skill item.
function GetTradeSkillItemLink(skillId) end


---Gets the link string for a trade skill item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillItemStats)
---@param skillId number The row of the tradeskill listbox containing the item.
---@return string[] itemStats Table containing item stats as strings.
function GetTradeSkillItemStats(skillId) end


---Returns the hyperlink for the currently opened tradeskill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillListLink)
---@return string? tradeLink
function GetTradeSkillListLink() end


---Returns information about the current tradeskill including its name, current level, maximum level, and skill line modifier.
---If the Trade Skill frame isn't open, it returns 'UNKNOWN' for 'tradeSkillName' and zero for all other values.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillLine)
---@return string tradeskillName Name of the current tradeskill
---@return number currentLevel Current skill level in the current tradeskill
---@return number maxLevel Current maximum skill level for the current tradeskill
---@return number skillLineModifier Skill modifier from racial abilities etc.
function GetTradeSkillLine() end


---Returns the number of distinct reagents required by the specified recipe.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillNumReagents)
---@param tradeSkillRecipeId number The id of the trade skill recipe.
---@return number reagentCount The number of distinct reagents required to create the item.
function GetTradeSkillNumReagents(tradeSkillRecipeId) end


---Retrieves information about a specific trade skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillInfo)
---@param skillIndex number The id of the skill you want to query.
---@return string skillName The name of the skill.
---@return string skillType The type of the skill (e.g., "trivial", "easy").
---@return number numAvailable The number of items the player can craft.
---@return boolean isExpanded If the skill header is expanded.
---@return string? altVerb Alternative verb for the skill's action.
---@return number numSkillUps The number of skill ups obtainable.
---@return number indentLevel Indicates indentation level for the skill.
---@return boolean showProgressBar If a sub-progress bar should be displayed.
---@return number currentRank The current rank for the specialty.
---@return number maxRank The maximum rank for the specialty.
---@return number startingRank The starting rank of the specialty.
function GetTradeSkillInfo(skillIndex) end


---Returns the EnchantLink for a trade skill, including details about the reagents and items created by the skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillRecipeLink)
---@param index number The row number of the tradeskill list, including category headers. It reflects the current state of the tradeskill window.
---@return string link An EnchantLink that can be used in chat messages.
function GetTradeSkillRecipeLink(index) end


---Returns the link string for a specified trade skill reagent.
---This function is broken as of patch 5.2.0 build 16650 and always returns nil.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillReagentItemLink)
---@param skillId number The ID specifying which trade skill's reagent to link.
---@param reagentId number The ID specifying which of the skill's reagents to link.
---@return string link An item link string for the reagent, color-coded with href.
function GetTradeSkillReagentItemLink(skillId, reagentId) end


---Returns the index of the currently selected trade skill or 0 if none is selected.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillSelectionIndex)
---@return number tradeSkillIndex The index of the currently selected trade skill.
function GetTradeSkillSelectionIndex() end


---Returns a list of valid trade skill subclasses.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillSubClasses)
---@return string[] subClasses The valid subclasses
function GetTradeSkillSubClasses() end


---Checks the visibility status of items corresponding to a trade skill subclass filter index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillSubClassFilter)
---@param filterIndex number
---@return boolean isVisible True if items are visible, otherwise false.
function GetTradeSkillSubClassFilter(filterIndex) end


---Get the number of items made in each use of a tradeskill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillNumMade)
---@param skillId number Which tradeskill to query.
---@return number minMade The minimum number of items that will be made.
---@return number maxMade The maximum number of items that will be made.
function GetTradeSkillNumMade(skillId) end


---Returns the number of times the current tradeskill item is being crafted.
---The repeat count is initially set by the optional repeat parameter of DoTradeSkill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeskillRepeatCount)
---@return number repeatCount The number of times the current tradeskill item is being crafted.
function GetTradeskillRepeatCount() end


---Returns the required tools for a specific trade skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillTools)
---@param skillIndex number
---@return string[] tools The tools required for the tradeskill
function GetTradeSkillTools(skillIndex) end


---Returns true if the tradeskill being viewed is from a link along with the player's name, nil otherwise.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsTradeSkillLinked)
---@return number|nil isLink 1 if the tradeskill shown in the UI is from a link, nil otherwise
---@return string|nil playerName The name of the player the tradeskill link is for, if isLink is 1, nil otherwise
function IsTradeSkillLinked() end

---! DRAFT - NEEDS REVIEW
---Sets the filter for inventory slots in the TradeSkillUI.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetTradeSkillInvSlotFilter)
---@param slotID number The slot ID to filter
---@param enable boolean Whether to enable the filter
---@return void
function SetTradeSkillInvSlotFilter(slotID, enable) end

---! DRAFT - NEEDS REVIEW
function SetTradeSkillSubClassFilter() end

---! DRAFT - NEEDS REVIEW
---Sets the trade skill item level filter. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetTradeSkillItemLevelFilter)
---@param minLevel number Minimum item level to filter
---@param maxLevel number Maximum item level to filter
function SetTradeSkillItemLevelFilter(minLevel, maxLevel) end

---! DRAFT - NEEDS REVIEW
---Stops any currently repeating trade skill cast.
---[Documentation](https://warcraft.wiki.gg/wiki/API_StopTradeSkillRepeat)
function StopTradeSkillRepeat() end


---Returns a list of the available inventory slot types.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillInvSlots)
---@return string[] invSlots The available inventory slot types
function GetTradeSkillInvSlots() end


---Returns information on reagents for the specified trade skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillReagentInfo)
---@param tradeSkillRecipeId number The ID of the tradeskill recipe
---@param reagentId number The ID of the reagent
---@return string reagentName The name of the reagent
---@return string reagentTexture The texture for the reagent's icon
---@return number reagentCount The quantity of this reagent required
---@return number playerReagentCount The quantity of this reagent in player's inventory
function GetTradeSkillReagentInfo(tradeSkillRecipeId, reagentId) end

