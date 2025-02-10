---@meta
--* GENERATED BY gemini-2.0-flash

---Converts a raid group with 5 or less members to a party.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_ConvertToParty)
function ConvertToParty() end

---Needs summary.<br>
---Usually this will convert to raid immediately. In some cases (e.g. PartySync) the user will be prompted to confirm converting to raid, because it's potentially destructive.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PartyInfo.ConvertToRaid)
function ConvertToRaid() end

---Invites a player to join your party.<br>
---Do not prehook this function in Classic Wrath as the LFG/Group Finder uses it directly. Only Secure Hook it.
---[Documentation](https://warcraft.wiki.gg/wiki/API_InviteUnit)
---@param playerName string The name of the player you would like to invite to a group.
function InviteUnit(playerName) end

---Leaves the current party.<br>
---[Documentation](https://warcraft.wiki.gg/wiki/API_LeaveParty)
function LeaveParty() end

---Attempts to request an invite into the target party.<br>
---Replaces `RequestInviteFromUnit`.
---[Documentation](https://warcraft.wiki.gg/wiki/API_C_PartyInfo.RequestInviteFromUnit)
---@param targetName string
function C_PartyInfo.RequestInviteFromUnit(targetName) end

