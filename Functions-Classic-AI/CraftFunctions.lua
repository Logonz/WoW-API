---@meta

---Returns the description for a specific craft index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftDescription)
---@param craftIndex number
---@return string craftDescription
function GetCraftDescription(craftIndex) end

---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftDisplaySkillLine)
---@return string skillLineName
function GetCraftDisplaySkillLine() end


---Returns details about a specific craft item.
---@param recipe number The index of the recipe to query.
---@return string craftName The name of the craft item.
---@return string craftSubSpellName The sub-spell of the craft item.
---@return number craftType The type or category of the craft item.
---@return boolean numAvailable The number of times the craft can be performed with available materials.
---@return boolean isExpanded Whether the craft is expanded in the UI.
---@return boolean trainingPointCost The cost in training points for the craft item.
---@return boolean progressionCost The progression cost of the craft item.
function GetCraftInfo(recipe) end


---Needs summary.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftItemLink)
---@param craftIndex number
---@return string? link
function GetCraftItemLink(craftIndex) end


---Returns the name of a specified crafting skill.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftName)
---@param index number
---@return string craftName
function GetCraftName(index) end


---Returns the number of reagents required for crafting a specific recipe.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftNumReagents)
---@param recipeIndex number
---@return number reagentCount
function GetCraftNumReagents(recipeIndex) end

---Returns information about a crafting reagent, such as its name, texture, and quantity required.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftReagentInfo)
---@param craftIndex number
---@param reagentIndex number
---@return string reagentName
---@return string reagentTexture
---@return number reagentCount
---@return number playerReagentCount
function GetCraftReagentInfo(craftIndex, reagentIndex) end

---Returns the item link string for a crafting reagent.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftReagentItemLink)
---@param craftIndex number
---@param reagentIndex number
---@return string? itemLink
function GetCraftReagentItemLink(craftIndex, reagentIndex) end

---! DRAFT - NEEDS REVIEW
---Returns a link to the specified craft recipe.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftRecipeLink)
---@param craftIndex number
---@return string craftRecipeLink
function GetCraftRecipeLink(craftIndex) end

---Retrieves the craft skill line name.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetCraftSkillLine)
---@return string skillLineName
function GetCraftSkillLine() end

---Returns the spell focus required for a specific craft, if any.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftSpellFocus)
---@return string? spellFocus
function GetCraftSpellFocus() end

---Returns the number of crafts the player can perform.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetNumCrafts)
---@return number numCrafts
function GetNumCrafts() end