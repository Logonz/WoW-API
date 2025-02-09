---@meta

---Provides information about a specific game account of a Battle.net friend.<br>[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetFriendGameAccountInfo)
---@param friendIndex number
---@param accountIndex number
---@return boolean hasFocus
---@return string clientProgram
---@return number realmID
---@return string realmName
---@return number faction
---@return string raceName
---@return string className
---@return string areaName
---@return number characterLevel
---@return string characterName
---@return boolean isOnline
---@return number? realmAddress
---@return number? actorID
function BNGetFriendGameAccountInfo(friendIndex, accountIndex) end

---Returns information about a Battle.net friend.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetFriendInfo)
---@param friendIndex number
---@return string givenName
---@return string battleTag
---@return number bnetIDAccount
---@return number client
---@return boolean isOnline
---@return boolean isAFK
---@return boolean isDND
---@return string messageText
---@return number noteText
---@return string presenceName
---@return number lastOnline
function BNGetFriendInfo(friendIndex) end


---! DRAFT - NEEDS REVIEW
---Returns information for a Real ID friend by their ID.
---@param friendID number
---@return string accountName
---@return BNetAccountID bnetAccountID
---@return number client
---@return (unknown) isOnline
---@return (unknown) lastOnline
---@return string noteText
---@return (unknown) isAFK
---@return (unknown) isDND
---@return (unknown) broadcastText
---@return string broadcastTime
function BNGetFriendInfoByID(friendID) end


---Retrieves information about another player's game account by their Battle.net friend game account ID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetGameAccountInfo)
---@param accountID number
---@return number gameAccountID
---@return number clientProgram
---@return string? realmName
---@return string? realmID
---@return string? factionName
---@return string characterName
---@return number? raceID
---@return number? classID
---@return number? guildID
---@return number? zoneID
---@return number? level
---@return boolean canSoR
---@return boolean restricted
---@return boolean toonID
function BNGetGameAccountInfo(accountID) end

---Returns the game account info for a specified GUID.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetGameAccountInfoByGUID)
---@param guid string
---@return unknown token
---@return unknown hasFocus
---@return unknown characterName
---@return unknown clientProgram
---@return unknown realmName
---@return unknown realmID
---@return unknown faction
---@return unknown race
---@return unknown class
---@return unknown zoneName
---@return unknown level
---@return unknown gameText
---@return unknown broadcastText
---@return unknown unknown1
---@return unknown unknown2
---@return unknown unknown3
function BNGetGameAccountInfoByGUID(guid) end

---Returns the number of game accounts associated with a Battle.net friend.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetNumFriendGameAccounts)
---@param bnetIDAccount number
---@return number numGameAccounts
function BNGetNumFriendGameAccounts(bnetIDAccount) end


---Checks if high-resolution textures are installed on the system. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BattleNet.AreHighResTexturesInstalled)
---@return boolean isInstalled
function C_BattleNet.AreHighResTexturesInstalled() end
