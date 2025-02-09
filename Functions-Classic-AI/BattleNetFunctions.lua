---@meta

---Returns the specified Battle.net friend's number of accounts. 
---This function returns the number of accounts a player has associated with a given battletag.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetNumFriendGameAccounts)
---@param friendIndex number The Battle.net friend's index on the friendslist
---@return number numGameAccounts The number of accounts or 0 if the friend is not online.
function BNGetNumFriendGameAccounts(friendIndex) end


---Returns information on the game the Battle.net friend is playing.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BattleNet.GetFriendGameAccountInfo)
---@param friendIndex number Index ranging from 1 to BNGetNumFriends()
---@param accountIndex number Index ranging from 1 to C_BattleNet.GetFriendNumGameAccounts()
---@return BNetGameAccountInfo? gameAccountInfo
function C_BattleNet.GetFriendGameAccountInfo(friendIndex, accountIndex) end


---Check if high resolution textures are installed.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_BattleNet.AreHighResTexturesInstalled)
---@return boolean installed
function C_BattleNet.AreHighResTexturesInstalled() end


---Returns information about the specified RealID friend.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetFriendInfo)
---@param friendIndex number The index on the friends list for this RealID friend.
---@return number bnetAccountID A temporary ID for the friend's battle.net account during this session.
---@return string accountName Escape sequence representing the friend's name.
---@return string battleTag Unique string that identifies the friend.
---@return boolean isBattleTagPresence Whether the friend is known by their BattleTag.
---@return string characterName The name of the logged in character.
---@return number bnetIDGameAccount A unique numeric identifier for the friend's game account.
---@return string client The client the friend is using.
---@return boolean isOnline Whether the friend is online.
---@return number|nil lastOnline Time since the friend was last online.
---@return boolean isAFK Whether the friend is flagged as Away.
---@return boolean isDND Whether the friend is flagged as Busy.
---@return string messageText The friend's Battle.Net broadcast message.
---@return string noteText Player's note about this friend.
---@return boolean isRIDFriend True for RealID friends, false for BattleTag friends.
---@return number messageTime Seconds elapsed since broadcast message was sent.
---@return boolean canSoR Whether this friend can receive a Scroll of Resurrection.
---@return boolean isReferAFriend 
---@return boolean canSummonFriend 
function BNGetFriendInfo(friendIndex) end


---Returns information about the specified RealID friend.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetFriendInfo)
---@param friendIndex number The index on the friends list for this RealID friend.
---@return number bnetAccountID A temporary ID for the friend's battle.net account during this session.
---@return string accountName An escape sequence representing the friend's full name or BattleTag name.
---@return string battleTag The unique BattleTag string (e.g., "Nickname#0001").
---@return boolean isBattleTagPresence Whether the friend is known by their BattleTag.
---@return string characterName The name of the logged in character.
---@return number bnetIDGameAccount A unique identifier for the friend's game account during this session.
---@return string client The client used, see BNET_CLIENT.
---@return boolean isOnline Whether the friend is online.
---@return number? lastOnline The seconds elapsed since last online or nil if currently online.
---@return boolean isAFK Whether the friend is flagged as Away.
---@return boolean isDND Whether the friend is flagged as Busy.
---@return string messageText The friend's Battle.Net broadcast message.
---@return string noteText The note added about this friend.
---@return boolean isRIDFriend Returns true for RealID friends and false for BattleTag friends.
---@return number messageTime seconds elapsed since the current broadcast message was sent.
---@return boolean canSoR Whether this friend can receive a Scroll of Resurrection.
---@return boolean isReferAFriend
---@return boolean canSummonFriend
function BNGetFriendInfo(friendIndex) end


---Returns information about the specified toon of a RealID friend.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetFriendGameAccountInfo)
---@param friendIndex number Ranges from 1 to BNGetNumFriendGameAccounts().
---@return boolean hasFocus Whether this toon is displayed in Blizzard's FriendFrame.
---@return string characterName The name of the toon.
---@return string client The client type (e.g., "WoW", "S2").
---@return string realmName The realm the toon is logged in.
---@return number realmID The ID of the realm.
---@return string faction Alliance or Horde.
---@return string race Localized race name (e.g., "Blood Elf").
---@return string class Localized class name (e.g., "Death Knight").
---@return string guild Guild of the toon, returns "" if no guild.
---@return string zoneName Localized zone name (e.g., "The Undercity").
---@return string level Current level of the toon.
---@return string gameText For WoW, returns "zoneName - realmName".
---@return string broadcastText Battle.Net broadcast message.
---@return number broadcastTime Seconds since the broadcast message was sent.
---@return boolean canSoR If the friend can receive a Scroll of Resurrection.
---@return number toonID Unique identifier for the friend's character.
---@return number bnetIDAccount Battle.net account ID.
---@return boolean isGameAFK If the player is AFK.
---@return boolean isGameBusy If the player is busy.
function BNGetFriendGameAccountInfo(friendIndex) end


---Returns information about the specified toon of a RealID friend.
---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetFriendGameAccountInfo)
---@param friendIndex number Ranging from 1 to BNGetNumFriendGameAccounts()
---@return boolean hasFocus Whether or not this toon is the one currently being displayed in Blizzard's FriendFrame.
---@return string characterName The name of the logged in toon/character.
---@return string client Either "WoW", "S2", "WTCG", "App", "Hero", "Pro", "CLNT", or "D3".
---@return string realmName The name of the logged in realm.
---@return number realmID The ID for the logged in realm.
---@return string faction The faction name (e.g., "Alliance" or "Horde").
---@return string race The localized race name (e.g., "Blood Elf").
---@return string class The localized class name (e.g., "Death Knight").
---@return string guild Seems to return "" even if the player is in a guild.
---@return string zoneName The localized zone name (e.g., "The Undercity").
---@return string level The current level (e.g., "90").
---@return string gameText For WoW, returns "zoneName - realmName". For StarCraft 2 and Diablo 3, returns the location or activity the player is currently engaged in.
---@return string broadcastText The Battle.Net broadcast message.
---@return number broadcastTime The number of seconds elapsed since the current broadcast message was sent.
---@return boolean canSoR Whether or not this friend can receive a Scroll of Resurrection.
---@return number toonID A unique numeric identifier for the friend's character during this session.
---@return number bnetIDAccount 
---@return boolean isGameAFK 
---@return boolean isGameBusy 
function BNGetFriendGameAccountInfo(friendIndex) end

