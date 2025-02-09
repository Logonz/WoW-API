---@meta

---! DRAFT - NEEDS REVIEW
---Returns detailed information about a specific chat channel.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ChannelInfo)
---@param channelIndex number The index of the channel.
---@return string? name The name of the channel.
---@return number? index The index of the channel.
---@return number? id The channel ID.
---@return boolean? isLocal Indicates if the channel is local.
---@return boolean? isZone Indicates if the channel is zone-specific.
---@return boolean? isMuted Indicates if the channel is muted.
---@return boolean? isSilenced Indicates if the channel is silenced.
---@return boolean? isTargeted Indicates if the channel is targeted.
---@return boolean? isCommunity Indicates if the channel is a community channel.
---@return number? category The category of the channel.
---@return boolean? isVoice Indicates if the channel has voice capabilities.
function ChannelInfo(channelIndex) end