---@meta

---Checks if the player is allowed to send an auction query.
---@return boolean canSendQuery
function CanSendAuctionQuery() end

---! DRAFT - NEEDS REVIEW
---Cancels a pending sale of an item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CancelSell)
function CancelSell() end

---! DRAFT - NEEDS REVIEW
---Handles the selling of an item in the auction house.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ClickAuctionSellItemButton)
function ClickAuctionSellItemButton() end

---Closes the auction house interface. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_CloseAuctionHouse)
function CloseAuctionHouse() end

---Returns additional information for an auctioned battle pet.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionItemBattlePetInfo)
---@param type string The type of the auction (either "list", "bidder", or "owner").
---@param index number The index of the auction item in the list.
---@return string speciesID
---@return string level
---@return string breedQuality
---@return number maxHealth
---@return number power
---@return number speed
---@return string name
function GetAuctionItemBattlePetInfo(type, index) end

---Returns various details about a specific auction item.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetAuctionItemInfo)
---@param type string Auction type
---@param index number Auction index
---@return string name
---@return string texture
---@return number count
---@return number quality
---@return number canUse
---@return number level
---@return string levelColHeader
---@return boolean isFullScan
---@return boolean isHighBidder
---@return boolean isOwner
---@return number bidAmount
---@return number minIncrement
---@return number buyoutPrice
---@return number duration
---@return string[5] itemLink
function GetAuctionItemInfo(type, index) end

---Returns the item link for a specific item in the auction house.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetAuctionItemLink)
---@param type string The type of auction ("list", "owner", "bidder").
---@param index number The index of the auction item.
---@return string? itemLink The item link, or nil if not available.
function GetAuctionItemLink(type, index) end

---Returns a list of available item sub-classes for a given auction item class.
---[Documentation](https://wowpedia.fandom.com/wiki/API_GetAuctionItemSubClasses)
---@param classID number The ID of the item class.
---@return string[] subClasses A list of sub-class names.
function GetAuctionItemSubClasses(classID) end

---Returns the time left for an auction item.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionItemTimeLeft)
---@param type string
---@param index number
---@return number timeLeft
function GetAuctionItemTimeLeft(type, index) end

---Returns information about the item currently set in the auction sell frame.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionSellItemInfo)
---@return string name
---@return string texture
---@return number count
---@return boolean quality
---@return number canUse
---@return number price
function GetAuctionSellItemInfo() end

---Returns the number of auction items for a given type.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumAuctionItems)
---@param type string The type of auction items to query. Can be "list", "bidder", or "owner".
---@return number numAuctions The total number of auctions.
---@return number totalAuctions The total number of auctions for the given type.
function GetNumAuctionItems(type) end

---Returns a table of AuctionDetails for the player's owned auctions.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetOwnerAuctionItems)
---@return AuctionDetails[] auctions
function GetOwnerAuctionItems() end

---Checks if the auction sort is reversed for the specified sort type.
---@param auctionSortType AuctionSortType The type of auction sort (e.g., "item", "time", "price").
---@return boolean isReversed Returns true if the sort type is reversed; otherwise, false.
function IsAuctionSortReversed(auctionSortType) end

---Places a bid on an auction.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PlaceAuctionBid)
---@param auctionType number
---@param index number
---@param bidAmount number
function PlaceAuctionBid(auctionType, index, bidAmount) end


---Posts an item for auction.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PostAuction)
---@param auctionID number The unique identifier for the auction.
---@param bidAmount number The starting bid amount for the auction.
---@param buyoutAmount? number The immediate purchase price for the auction.
---@param auctionDuration Enum.AuctionDuration The duration for which to list the auction.
---@return boolean success Indicates if the auction was successfully posted.
function PostAuction(auctionID, bidAmount, buyoutAmount, auctionDuration) end



---Queries the auction house for items based on specified parameters.
---[Documentation](https://warcraft.wiki.gg/wiki/API_QueryAuctionItems)
---@param name? string The name of the item.
---@param minLevel? number The minimum item level.
---@param maxLevel? number The maximum item level.
---@param page? number The auction house page.
---@param isUsable? boolean Filters items usable by the player.
---@param qualityIndex? number The item quality filter.
---@param getAll? boolean If true, disregards other filter parameters and returns all results.
---@return boolean success Indicates if the query was successful.
function QueryAuctionItems(name, minLevel, maxLevel, page, isUsable, qualityIndex, getAll) end


---Sets the selected auction item.  
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSelectedAuctionItem)
---@param auctionType string
---@param index number
function SetSelectedAuctionItem(auctionType, index) end

---Sorts auction house items based on specified criteria.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SortAuctionItems)
---@param sortType number
---@param reverse boolean
function SortAuctionItems(sortType, reverse) end


---! DRAFT - NEEDS REVIEW
---Sorts the current set of auction items according to a specified sorting order.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SortAuctionSetSort)
---@param sortType string The type of sort, e.g., "price", "quantity".
---@param sortOrder boolean If true, sorts in ascending order; otherwise descending.
function SortAuctionSetSort(sortType, sortOrder) end


---Starts an auction using specified item and auction parameters.
---[Documentation](https://warcraft.wiki.gg/wiki/API_StartAuction)
---@param startPrice number The starting price for the auction.
---@param duration number The duration of the auction (in hours).
---@param itemIndex number The index of the item in the bag.
---@param stackSize number The size of the item stack.
---@param numStacks number The number of stacks being auctioned.
function StartAuction(startPrice, duration, itemIndex, stackSize, numStacks) end