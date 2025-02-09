---@meta

---Returns the index of the current active talent group.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetActiveTalentGroup)
---@param isInspect boolean If true returns the information for the inspected unit instead of the player.
---@param isPet boolean If true returns the information for the inspected pet.
---@return number index The index of the current active talent group (1 for primary / 2 for secondary).
function GetActiveTalentGroup(isInspect, isPet) end


---Returns the next level at which your character will gain a talent point. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNextTalentLevel)
---@param level? number The level to consider; defaults to the character's current level.
---@return number nextLevel The level at which the next talent point is gained.
function GetNextTalentLevel(level) end


---Returns the total number of talent groups for the player. Defaults to one talent group, two if Dual Talent Specialization is purchased. Requires NotifyInspect() and INSPECT_READY for inspecting others.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumTalentGroups)
---@param isInspect? boolean False by default, to check talent groups of another player.
---@return number num The number of talent groups.
function GetNumTalentGroups(isInspect) end


---Returns the amount of talents for a specialization. This function is only available in Cata Classic and Classic Era.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumTalents)
---@param tabIndex number Ranging from 1 to GetNumTalentTabs()
---@return number numTalents The amount of talents offered by a specialization.
function GetNumTalents(tabIndex) end


---Returns the total number of talent tabs for the player.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumTalentTabs)
---@param isInspect? boolean Will return the number of talent tabs for the current inspect target if true.
---@return number numTabs The number of talent tabs available.
function GetNumTalentTabs(isInspect) end


---Returns the index of your primary talent tree.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetPrimaryTalentTree)
---@param isInspect? boolean If true, returns information for the inspected unit instead of the player.
---@param isPet? boolean If true, returns information for the inspected pet.
---@param talentGroup? number The number of the talent group to look at, e.g., 1 for Primary, 2 for Secondary.
---@return number|nil primaryTabId Returns the index of the tab with the most talents, i.e., the primary talent tree (1, 2, or 3), or nil if no primary tree is selected.
function GetPrimaryTalentTree(isInspect, isPet, talentGroup) end


---Returns the currently selected role for a player's talent group (primary or secondary).
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTalentGroupRole)
---@param groupIndex number Ranging from 1 to 2 (primary/secondary talent group).
---@return string role Can be "DAMAGER", "TANK", or "HEALER".
function GetTalentGroupRole(groupIndex) end


---Returns the roles which a particular talent tree is designed for.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTalentTreeRoles)
---@param talentTreeId number The ID of the talent tree, 1-3 as returned by GetPrimaryTalentTree and similar functions.
---@param isInspect? boolean If true, returns the information for the inspected unit instead of the player.
---@param isPet? boolean If true, returns the information for the inspected pet.
---@return string tabRole1 The primary role this tree is designed for.
---@return string tabRole2? The secondary role if applicable.
function GetTalentTreeRoles(talentTreeId, isInspect, isPet) end


---Returns information for a talent tab (tree).
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTalentTabInfo)
---@param index number - Ranging from 1 to GetNumTalentTabs()
---@param isInspect boolean? - Optional, will return talent tab info for the current inspect target if true.
---@param isPet boolean? - Optional, will return talent tab info for the player's pet if true.
---@param talentGroup number? - Optional talent group to query for Dual Talent Specialization. Defaults to 1.
---@return number id
---@return string name
---@return string description
---@return number icon
---@return number pointsSpent - Number of points put into the tab.
---@return number background - File name of the background image.
---@return number previewPointsSpent
---@return boolean isUnlocked
function GetTalentTabInfo(index, isInspect, isPet, talentGroup) end


---Returns the tier and column of a talent's prerequisite, and if the talent is learnable.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetTalentPrereqs)
---@param tabIndex number Ranging from 1 to GetNumTalentTabs()
---@param talentIndex number Ranging from 1 to GetNumTalents(tabIndex)
---@param isInspect? boolean Whether the talent is for the currently inspected player.
---@param isPet? boolean
---@param talentGroup? number Probably the dual spec group index.
---@return number tier The row/tier that the prerequisite talent sits on.
---@return number column The column that the prerequisite talent sits on.
---@return number? isLearnable Returns 1 if you have learned the prerequisite talents, nil otherwise.
function GetTalentPrereqs(tabIndex, talentIndex, isInspect, isPet, talentGroup) end


---Returns the number of unspent talent points for the player, player's pet, or an inspected unit. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetUnspentTalentPoints)
---@param isInspected boolean If true, returns the information for the inspected unit instead of the player.
---@param isPet boolean If true, returns the information for the pet instead of the player (only valid for hunter with a pet active).
---@param talentGroup number The index of the talent group (1 for primary / 2 for secondary).
---@return number talentPoints Number of unspent talent points.
function GetUnspentTalentPoints(isInspected, isPet, talentGroup) end


---Sets the active talent group of the player. This triggers a 5-second cast when clicking the "Activate These Talents" button in the talent pane.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetActiveTalentGroup)
---@param groupIndex number Ranging from 1 to 2 (primary/secondary talent group).
function SetActiveTalentGroup(groupIndex) end


---Sets your primary talent tree.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetPrimaryTalentTree)
---@param talentTabId number The ID of the tab to make your primary tree.
function SetPrimaryTalentTree(talentTabId) end

