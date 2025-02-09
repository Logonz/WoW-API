---@meta

---Closes the trade skill window if it's currently open.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CloseTradeSkill)
function CloseTradeSkill() end

---Performs a trade skill action.
---[Documentation](https://wowpedia.fandom.com/wiki/API_DoTradeSkill)
---@param recipeID number The ID of the recipe to be crafted
---@param numCasts number The number of times to craft the recipe
function DoTradeSkill(recipeID, numCasts) end

---! DRAFT - NEEDS REVIEW  
---Expands a trade skill class specified by its index.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_ExpandTradeSkillSubClass)  
---@param subclassIndex number  
function ExpandTradeSkillSubClass(subclassIndex) end

---! DRAFT - NEEDS REVIEW
---Returns the index of the first skill in the current trade skill window. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetFirstTradeSkill)
---@return number? firstSkillIndex
function GetFirstTradeSkill() end

---Returns the total number of trade skills.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumTradeSkills)
---@return number numTradeSkills
function GetNumTradeSkills() end

---Returns a description of a specified trade skill.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetTradeSkillDescription)
---@param skillID number
---@return string description
function GetTradeSkillDescription(skillID) end

---Returns information about a specific trade skill.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetTradeSkillInfo)
---@param index number
---@return string skillName
---@return string skillType
---@return number numAvailable
---@return number isExpanded
---@return? number altVerb
---@return? boolean isLearned
---@return? boolean altVerbOnOtherChat
function GetTradeSkillInfo(index) end

---! DRAFT - NEEDS REVIEW
---Returns the inventory slot filter for trade skills. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillInvSlotFilter)
---@return string filterName
function GetTradeSkillInvSlotFilter() end

---Returns the available inventory slots for a trade skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillInvSlots)
---@return number numSlots
---@return string[] invSlotsNames
---@return number[] invSlotsIDs
function GetTradeSkillInvSlots() end

---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillItemLink)
---@param tradeSkillIndex number
---@return string? itemLink
function GetTradeSkillItemLink(tradeSkillIndex) end

---Returns detailed statistics for a trade skill item associated with a specific trade skill.
---! DRAFT - NEEDS REVIEW
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetTradeSkillItemStats)
---@param skillID number
---@return table itemStats
function GetTradeSkillItemStats(skillID) end

---! DRAFT - NEEDS REVIEW
---Returns the name and rank of the currently selected trade skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillLine)
---@return string? skillName
---@return number? skillRank
---@return number? maxSkillRank
function GetTradeSkillLine() end

---! DRAFT - NEEDS REVIEW
---Returns the hyperlink for a trade skill list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillListLink)
---@param skillID number
---@return string? link
function GetTradeSkillListLink(skillID) end


---Returns the number of items that a crafting recipe will create.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetTradeSkillNumMade)
---@param tradeskillIndex number
---@return number numMins
---@return number numMaxs
function GetTradeSkillNumMade(tradeskillIndex) end


---Returns the number of different reagents required by a specific trade skill recipe.  
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetTradeSkillNumReagents)  
---@param recipeID number
---@return number numReagents
function GetTradeSkillNumReagents(recipeID) end

---! DRAFT - NEEDS REVIEW
---Returns information for a specific reagent required by a trade skill recipe.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetTradeSkillReagentInfo)
---@param skillIndex number
---@param reagentIndex number
---@return string reagentName
---@return string reagentTexture
---@return number reagentCount
---@return boolean playerHasReagent
function GetTradeSkillReagentInfo(skillIndex, reagentIndex) end

---! DRAFT - NEEDS REVIEW  
---Returns the item link for a reagent used in a trade skill.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillReagentItemLink)  
---@param tradeSkillIndex number  
---@param reagentIndex number  
---@return string? itemLink  
function GetTradeSkillReagentItemLink(tradeSkillIndex, reagentIndex) end

---Returns the hyperlink for the specified trade skill recipe. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillRecipeLink)
---@param recipeID number
---@return string recipeLink
function GetTradeSkillRecipeLink(recipeID) end

---Retrieves the selection index of the current trade skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillSelectionIndex)
---@return number selectionIndex
function GetTradeSkillSelectionIndex() end

---! DRAFT - NEEDS REVIEW
---Gets the status of a subclass filter in a trade skill.
---@param filterIndex number The index of the subclass filter.
---@return boolean isChecked The status of the specified subclass filter.
function GetTradeSkillSubClassFilter(filterIndex) end

---! DRAFT - NEEDS REVIEW
---Retrieves the list of available trade skill subclasses.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillSubClasses)
---@return string[] tradeSubClasses
function GetTradeSkillSubClasses() end

---! DRAFT - NEEDS REVIEW  
---Returns the tools required for a specific trade skill.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeSkillTools)  
---@param skillIndex number  
---@return string neededTools  
function GetTradeSkillTools(skillIndex) end

---! DRAFT - NEEDS REVIEW
---Retrieves the number of times the current tradeskill operation will be repeated.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTradeskillRepeatCount)
---@return number repeatCount
function GetTradeskillRepeatCount() end

---Checks if the trade skill window is showing a linked skill. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsTradeSkillLinked)
---@return boolean isLinked
function IsTradeSkillLinked() end

---Sets the trade skill inventory slot filter.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetTradeSkillInvSlotFilter)
---@param slotIndex number
---@param enable boolean
function SetTradeSkillInvSlotFilter(slotIndex, enable) end


---Sets the item level filter for trade skills.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetTradeSkillItemLevelFilter)
---@param minLevel number Minimum item level
---@param maxLevel number Maximum item level
function SetTradeSkillItemLevelFilter(minLevel, maxLevel) end



---Sets the filter for a specific trade skill subclass.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetTradeSkillSubClassFilter)
---@param subclassID number
---@param filterOn boolean
function SetTradeSkillSubClassFilter(subclassID, filterOn) end


---Stops repeating the current trade skill action.
function StopTradeSkillRepeat() end