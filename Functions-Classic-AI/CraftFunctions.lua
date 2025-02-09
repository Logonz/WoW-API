---@meta

---Returns a string description of what the current craft does.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftDescription)
---@param index number Number from 1 to X number of total crafts, where 1 is the top-most craft listed.
---@return string craftDescription Example: "Permanently enchant a two handed melee weapon to grant +25 Agility."
function GetCraftDescription(index) end


---Returns the name displayed on the craft window.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftName)
---@return string craftName It appears to return the localized name of Enchanting, Poisons for Rogues, and Cooking?
function GetCraftName() end


---Returns an itemLink for a specified trade skill item in the current active trade skill.
---@param index number The index of the item in the current active trade skill.
---@return string|nil itemLink The corresponding item link or nil if invalid.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftItemLink)
function GetCraftItemLink(index) end


---Retrieves displayable information for the current craft in WoW.
---Returns the name, rank, and max rank for the active craft, or nil if unavailable.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftDisplaySkillLine)
---@return string|nil name The name of the active craft, or nil if not displayable
---@return number|nil rank The player's current rank for the craft
---@return number|nil maxRank The maximum rank for the craft
function GetCraftDisplaySkillLine() end


---Returns the number of reagents required for a specified craft.
---[Documentation](https://warcraft.wiki.gg/wiki/GetCraftNumReagents)
---@param index number Number from 1 to X, where X is the total number of possible crafts.
---@return integer numRequiredReagents The number of required reagents for the craft.
function GetCraftNumReagents(index) end


---Returns details about a specific craft, including its name, type, availability, and requirements.
---Only applies to headers, indicating expanded or contracted state. Nil for non-header crafts.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftInfo)
---@param index number - 1 to GetNumCrafts()
---@return string craftName Name of the item you can craft
---@return string craftSubSpellName
---@return string craftType "header" or difficulty level such as trivial, easy, medium, or optimal
---@return number numAvailable Number of crafts possible with current reagents
---@return boolean? isExpanded Indicates if headers are expanded
---@return number? trainingPointCost Training points required at a trainer
---@return number? requiredLevel Required level if at a trainer
function GetCraftInfo(index) end


---Returns information about a crafting reagent including its name, texture path, quantity required, and quantity owned. 
---[Documentation](https://warcraft.wiki.gg/wiki/GetCraftReagentInfo)
---@param index number The starting index of the crafts, where 1 is the top-most listed craft.
---@param n number The specific reagent index for the selected craft.
---@return string name Name of the reagent required.
---@return string texturePath Path to the item texture.
---@return number numRequired Number of total required reagents.
---@return number numHave Number of reagents currently in possession.
function GetCraftReagentInfo(index, n) end


---Returns a required reagent as an itemLink for a specific craftable item from the currently visible tradeskill window.
---If an invalid index or no visible tradeskill window is specified, nil is returned.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftReagentItemLink)
---@param index number The index of the requested craft recipe, starting from 1.
---@param n number The index of the Nth reagent for the recipe, starting from 1.
---@return string reagentLink The itemLink for the requested reagent.
function GetCraftReagentItemLink(index, n) end


---! DRAFT - NEEDS REVIEW
---Returns which rod is required when enchanting, if any.
---Returns the rod name and the number "1" when a rod is needed; else returns `nil`.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftSpellFocus)
---@param index number Index from 1 to GetNumCrafts()
---@return string|nil catalystName The name of the required rod
---@return number? number1 Always returns the number "1" if a rod is required
function GetCraftSpellFocus(index) end


---Returns the name of the currently opened crafting window or nil.
---This command reveals which crafting window, such as "Enchanting" or "Beast Training", is open.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftSkillLine)
---@param n number Any non-zero number behaves the same. Zero always returns nil.
---@return string|nil currentCraftingWindow The name of the open crafting window or nil if none.
function GetCraftSkillLine(n) end


---Returns the EnchantLink for a craft, allowing it to be included in chat messages to show the reagents and the items the craft creates.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetCraftRecipeLink)
---@param index number The index of the item in the current active trade skill.
---@return string link An EnchantLink with color coding and href.
function GetCraftRecipeLink(index) end


---Returns the number of crafts in the currently opened crafting window. Usually used to loop through available crafts.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumCrafts)
---@return number numberOfCrafts
function GetNumCrafts() end

