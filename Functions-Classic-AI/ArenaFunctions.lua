---@meta

---Leaves an arena team at the specified index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamLeave)
---@param index number
function ArenaTeamLeave(index) end

---Accepts a pending arena team invitation.<br>[Documentation](https://warcraft.wiki.gg/wiki/API_AcceptArenaTeam)
function AcceptArenaTeam() end

---Sets the leader of an arena team by specifying the name.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamSetLeaderByName)
---@param index number
---@param target string
function ArenaTeamSetLeaderByName(index, target) end


---Disbands an Arena Team if the player is the team captain.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamDisband)
---@param index number Index of the arena team to delete, can be a value of 1 through 3.
function ArenaTeamDisband(index) end


---Invites a player to an arena team by their name.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamInviteByName)
---@param index number The arena team index.
---@param target string The name of the player to invite.
function ArenaTeamInviteByName(index, target) end


---! DRAFT - NEEDS REVIEW
---Uninvites a player from an arena team by name.
---[Documentation](https://warcraft.wiki.gg/wiki/ArenaTeamUninviteByName)
---@param index number
---@param target string
function ArenaTeamUninviteByName(index, target) end


---Requests the arena team information from the server.
---Because this sends a request to the server, data is not received instantly. You must register and watch for the ARENA_TEAM_ROSTER_UPDATE event.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ArenaTeamRoster)
---@param index number Index of the arena team to request information from, 1 through 3.
function ArenaTeamRoster(index) end


---Declines a pending arena team invitation. Only one arena invitation may be pending at any time.
---[Documentation](https://warcraft.wiki.gg/wiki/API_DeclineArenaTeam)
function DeclineArenaTeam() end


---Returns the index of an arena team for the specified team size.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetArenaTeamIndexBySize)
---@param size number # Team size (number of people), i.e. 2, 3, or 5
---@return number? index # Arena team index for the specified team size, or nil if not in a team of that size
function GetArenaTeamIndexBySize(size) end


---Requests information regarding the arena team that the player is in.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetArenaTeam)
---@param index number Index of the team (1 to 3)
---@return string? teamName Teams name; nil if not on a team or data not received
---@return number teamSize Team size (2, 3, or 5)
---@return number teamRating Teams rating, defaults to 1500 if no games played
---@return number weekPlayed Total games played this week
---@return number weekWins Total games won this week
---@return number seasonPlayed Total games played in current season
---@return number seasonWins Total games won in current season
---@return number playerPlayed Total games player participated in this week
---@return number seasonPlayerPlayed Total games player participated in this season
---@return number teamRank Teams current ranking, typically updated weekly
---@return number personalRating Players personal rating with this team
---@return number backgroundRed Amount of red in the team's banner background
---@return number backgroundGreen Amount of green in the team's banner background
---@return number backgroundBlue Amount of blue in the team's banner background
---@return number emblem Emblem graphic name
---@return number emblemRed Amount of red in the team's emblem color
---@return number emblemGreen Amount of green in the team's emblem color
---@return number emblemBlue Amount of blue in the team's emblem color
---@return number border Border graphic name
---@return number borderRed Amount of red in the team's border color
---@return number borderGreen Amount of green in the team's border color
---@return number borderBlue Amount of blue in the team's border color
function GetArenaTeam(index) end


---Requests information regarding a specific arena team member, returning various stats such as games played, wins, and personal rating.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetArenaTeamRosterInfo)
---@param teamindex number @Index of the team (1-3).
---@param playerindex number @Index of the team member, starting at 1.
---@return string name @Name of the player.
---@return number rank @Rank of the player (0 for captain, 1 for member).
---@return number level @Player's level.
---@return string class @Player's class.
---@return number|nil online @Online status (1 for online, nil for offline).
---@return number played @Games played this week.
---@return number win @Games won this week.
---@return number seasonPlayed @Games played in the current season.
---@return number seasonWin @Games won in the current season.
---@return number personalRating @Player's personal rating with this team.
function GetArenaTeamRosterInfo(teamindex, playerindex) end

