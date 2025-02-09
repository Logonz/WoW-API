---@meta


---! DRAFT - NEEDS REVIEW
---Accepts an invitation to join an arena team.
---[Documentation](https://warcraft.wiki.gg/wiki/API_AcceptArenaTeam)
function AcceptArenaTeam() end



---Disbands the arena team with the given team ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamDisband)
---@param teamID number
function ArenaTeamDisband(teamID) end


---! DRAFT - NEEDS REVIEW  
---Invites a player to an arena team by their name.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamInviteByName)  
---@param teamID number  
---@param name string  
function ArenaTeamInviteByName(teamID, name) end

---Leaves the arena team of the specified team type.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamLeave)
---@param teamType number
function ArenaTeamLeave(teamType) end

---! DRAFT - NEEDS REVIEW
---Retrieves a member's information from an arena team roster.
---@param type number
---@param memberIndex number
---@return string name
---@return number level
---@return number class
---@return number online
---@return number? played
---@return number? won
---@return number? seasonPlayed
---@return number? seasonWon
---@return number? rating
function ArenaTeamRoster(type, memberIndex) end

---! DRAFT - NEEDS REVIEW
---Sets the leader of an arena team by name.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamSetLeaderByName)
---@param teamID number
---@param newLeader string
function ArenaTeamSetLeaderByName(teamID, newLeader) end


---! DRAFT - NEEDS REVIEW
---Uninvites a player by name from the arena team.
---[Documentation](https://wowpedia.fandom.com/wiki/API_ArenaTeamUninviteByName)
---@param teamName string
---@param playerName string
function ArenaTeamUninviteByName(teamName, playerName) end


---Declines an invitation to join an arena team.
---[Documentation](https://warcraft.wiki.gg/wiki/API_DeclineArenaTeam)
function DeclineArenaTeam() end

---! DRAFT - NEEDS REVIEW
---Returns information about an arena team.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetArenaTeam)
---@param index number
---@return string teamName
---@return number teamSize
---@return number teamRating
---@return number gamesPlayed
---@return number gamesWon
---@return number seasonGamesPlayed
---@return number seasonGamesWon
function GetArenaTeam(index) end

---! DRAFT - NEEDS REVIEW  
---Returns the index of an arena team based on its size.  
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetArenaTeamIndexBySize)  
---@param size number The size of the arena team (e.g., 2 for 2v2, 3 for 3v3, etc.)
---@return number index The index of the arena team
function GetArenaTeamIndexBySize(size) end

---Returns information about a player in the arena team roster.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetArenaTeamRosterInfo)
---@param teamIndex number
---@param memberIndex number
---@return string name
---@return number rank
---@return number level
---@return number classLocalized
---@return number online
---@return number played
---@return number wons
---@return number seasonPlayed
---@return number seasonWon
function GetArenaTeamRosterInfo(teamIndex, memberIndex) end