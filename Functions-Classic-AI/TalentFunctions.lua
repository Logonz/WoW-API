---@meta

---Returns the index of the active specialization group.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetActiveTalentGroup)
---@param isInspect boolean
---@param isPet boolean
---@return number groupIndex
function GetActiveTalentGroup(isInspect, isPet) end

---! DRAFT - NEEDS REVIEW  
---Returns the next level at which a talent point is gained.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNextTalentLevel)
---@return number nextTalentLevel
function GetNextTalentLevel() end

---Returns the number of available talent groups (specializations or sets) for a character.
---@return number numTalentGroups The total number of talent groups available for the character.
function GetNumTalentGroups() end

---Returns the number of talent tabs available for the player.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumTalentTabs)
---@return number numTalentTabs
function GetNumTalentTabs() end

---! DRAFT - NEEDS REVIEW
---Retrieves the number of talents available for a specific talent tab.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetNumTalents)
---@param tabIndex number The index of the talent tab.
---@param isInspect boolean Optional. If true, gets the number of talents of the inspected unit.
---@param isPet boolean Optional. If true, gets the number of talents of the pet.
---@return number numTalents The number of talents available.
function GetNumTalents(tabIndex, isInspect, isPet) end

---Returns the primary talent tree for a given class.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPrimaryTalentTree)
---@param isInspect boolean
---@param isPet boolean
---@param talentGroup number
---@param inspectUnit string
---@return number primaryTalentTree
function GetPrimaryTalentTree(isInspect, isPet, talentGroup, inspectUnit) end

---! DRAFT - NEEDS REVIEW
---Retrieves the role associated with the specified talent specialization group.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTalentGroupRole)
---@param talentGroupIndex number
---@param isInspect boolean
---@return string role
function GetTalentGroupRole(talentGroupIndex, isInspect) end


---Returns the prerequisites for a specified talent tab and talent index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTalentPrereqs)
---@param tabIndex number
---@param talentIndex number
---@return boolean meetsPrereqs
---@return string prerreq1
---@return string prerreq2
---@return string prerreq3
function GetTalentPrereqs(tabIndex, talentIndex) end


---Retrieves information about a specific talent tab.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTalentTabInfo)
---@param tabIndex number The index of the talent tab.
---@param inspect? boolean If true, returns info for the inspected target.
---@param pet? boolean If true, returns info for the player's pet.
---@param talentGroup? number The talent group number.
---@return string name Name of the talent tab.
---@return string iconTexture Path to the icon texture for the talent tab.
---@return number pointsSpent Number of talent points spent in this tab.
---@return number backgroundTexture File ID of the background texture.
---@return number previewPointsSpent Number of preview points spent.
---@return number isUnlocked Whether the tab is unlocked.
function GetTalentTabInfo(tabIndex, inspect, pet, talentGroup) end

---Returns the roles associated with a specified talent tree.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetTalentTreeRoles)
---@param treeID number
---@return string[] roles
function GetTalentTreeRoles(treeID) end

---Returns the number of unspent talent points a character has.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetUnspentTalentPoints)
---@return number unspentPoints
function GetUnspentTalentPoints() end

---! DRAFT - NEEDS REVIEW
---Sets the specified talent group as active.
---@param talentGroup number The talent group to activate (1 for primary, 2 for secondary).
function SetActiveTalentGroup(talentGroup) end

---Sets the player's primary talent tree.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetPrimaryTalentTree)
---@param primaryTreeID number
---@param isInspectTalentTree? boolean
function SetPrimaryTalentTree(primaryTreeID, isInspectTalentTree) end