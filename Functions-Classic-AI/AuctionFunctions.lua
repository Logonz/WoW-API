---@meta

---Stops the process of listing multiple stacks of an item on the auction house.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CancelSell)
function CancelSell() end


---Closes the AuctionFrame if it is open. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_CloseAuctionHouse)
function CloseAuctionHouse() end


---Determines if a new auction house query can be sent.
---Returns whether a normal or full ("getall") auction house query is possible.
---[Documentation](https://warcraft.wiki.gg/wiki/API_CanSendAuctionQuery)
---@return boolean canQuery True if a normal auction house query can be made
---@return boolean canQueryAll True if a full "getall" auction house query can be made
function CanSendAuctionQuery() end


---Puts the currently 'picked up' item into the 'create auction' slot.
---Works while the 'auction' window is up, allowing item placement in the auction house interface.
---[Documentation](https://warcraft.wiki.gg/wiki/API_ClickAuctionSellItemButton)
---@param frame Frame The UI frame where the action occurs
---@param button string|integer The mouse button used, e.g., a string like "LeftButton" or a button number
---@param isDown boolean Whether the mouse button is held down
function ClickAuctionSellItemButton(frame, button, isDown) end


---Retrieves info about a Battle Pet from the Auction House's current listing.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionItemBattlePetInfo)
---@param type string One of "list", "bidder", "owner".
---@param index number The index of the item in the list to retrieve info from (usually 1-50).
---@return number creatureID The indexing value Blizzard uses to number NPCs.
---@return number displayID An indexing value Blizzard uses to number model/skin combinations.
function GetAuctionItemBattlePetInfo(type, index) end


---Retrieves the itemLink of an item from the Auction House list based on the specified type and index.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionItemLink)
---@param type string One of "list", "bidder", or "owner"
---@param index number The index of the item in the list to retrieve, typically between 1 and 50
---@return string|nil itemLink The itemLink for the specified item, or nil if the type or index is invalid
function GetAuctionItemLink(type, index) end


---Gets a list of the sub-classes for an Auction House item class.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionItemSubClasses)
---@param classID number The ID of the item class.
---@return number[] subClasses The valid subclasses for an item class.
function GetAuctionItemSubClasses(classID) end


---Retrieves the time left for an item in the Auction House.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionItemTimeLeft)
---@param type string One of the following: "list", "bidder", "owner".
---@param index number The index of the item (1-50, inclusive).
---@return number timeleft A number between 1 and 4 where 1 is short, 2 is medium, 3 is long, and 4 is very long.
function GetAuctionItemTimeLeft(type, index) end


---Retrieves information about the current item being set for auction in the seller's auction window.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionSellItemInfo)
---@return string name
---@return string texture
---@return number count
---@return number quality
---@return boolean canUse
---@return number price
---@return number pricePerUnit
---@return number stackCount
---@return number totalCount
---@return number itemID
function GetAuctionSellItemInfo() end


---Retrieves info about one item in the current retrieved list of items from the Auction House.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetAuctionItemInfo)
---@param type string One of the following: "list", "bidder", or "owner".
---@param index number The index of the item in the list to retrieve info from (normally 1-50, inclusive).
---@return string name The name of the item.
---@return number texture The fileID of the texture of the item.
---@return number count The number of items in the auction item, zero if sold.
---@return Enum.ItemQuality quality The item quality.
---@return boolean canUse True if the user can use the item.
---@return number level The level required to use the item.
---@return string levelColHeader Specifies the meaning of level: "REQ_LEVEL_ABBR", "SKILL_ABBR", "ITEM_LEVEL_ABBR", "SLOT_ABBR".
---@return number minBid The starting bid price.
---@return number minIncrement The minimum amount for the next bid.
---@return number buyoutPrice Zero if no buy out, otherwise the buyout price.
---@return number bidAmount The current highest bid.
---@return string? highBidder Name of highest bidder, nil if none.
---@return string? bidderFullName Bidder's full name if from virtual realm.
---@return string owner The player selling the item.
---@return string? ownerFullName Owner's full name if from virtual realm.
---@return number saleStatus 1 for sold, 0 for unsold.
---@return number itemId The item ID.
---@return boolean hasAllInfo Was everything returned.
function GetAuctionItemInfo(type, index) end


---Retrieves the number of auction items of a certain type.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetNumAuctionItems)
---@param list string The type of auction items ("list", "bidder", or "owner")
---@return number batch The size of the batch being viewed
---@return number count The total number of items in the query
function GetNumAuctionItems(list) end


---Updates the owned auction list.
---[Documentation](https://warcraft.wiki.gg/wiki/API_GetOwnerAuctionItems)
function GetOwnerAuctionItems() end


---Returns the sorting order for a specified column in the auction house display.
---[Documentation](https://warcraft.wiki.gg/wiki/API_IsAuctionSortReversed)
---@param type string One of the following: "list", "bidder", "owner"
---@param sort string One of the following: "quality", "level", "status", "duration", "bid", "name", "buyout"
---@return number|nil sorted 1 if the column is sorted in reverse order, nil otherwise
function IsAuctionSortReversed(type, sort) end


---Places a bid on a selected auction item.
---The function can only be successfully called after a hardware event since patch 2.0.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PlaceAuctionBid)
---@param type string One of the following: "list", "bidder", "owner"
---@param index number The index of the item in the list to bid on (normally 1-50, inclusive)
---@param bid number The amount of money to bid in copper
function PlaceAuctionBid(type, index, bid) end


---Starts the auction you have created in the Create Auction panel.
---[Documentation](https://warcraft.wiki.gg/wiki/API_PostAuction)
---@param minBid number The minimum bid price for this auction in copper.
---@param buyoutPrice number The buyout price for this auction in copper.
---@param runTime number The duration for which the auction should be posted.
---@param stackSize number The size of each stack to be posted.
---@param numStacks number The number of stacks to post.
function PostAuction(minBid, buyoutPrice, runTime, stackSize, numStacks) end


---Queries the server for information about current auctions when CanSendAuctionQuery() is true.
---[Documentation](https://warcraft.wiki.gg/wiki/API_QueryAuctionItems)
---@param text string A part of the item's name, or an empty string; limited to 63 bytes.
---@param minLevel? number Minimum usable level requirement for items.
---@param maxLevel? number Maximum usable level requirement for items.
---@param page number What page in the auction house this shows up. Note that pages start at 0.
---@param usable boolean Restricts items to those usable by the current character.
---@param rarity? Enum.ItemQuality Restricts the quality of the items found.
---@param getAll boolean Download the entire auction house as a single page.
---@param exactMatch boolean Will only find items whose whole name matches the search string.
---@param filterData? table Table of additional filtering data.
function QueryAuctionItems(text, minLevel, maxLevel, page, usable, rarity, getAll, exactMatch, filterData) end


---Selects a specific item in the auction house.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SetSelectedAuctionItem)
---@param type string One of "list" (auction items), "bidder" (items bid on), or "owner" (items up for auction).
---@param index number The index of the item in the list (typically between 1 and 50 inclusive).
function SetSelectedAuctionItem(type, index) end

---! DRAFT - NEEDS REVIEW
---**Unable to retrieve function details from the provided URL**  
---Please ensure the webpage is accessible and try again with the correct content.

---! DRAFT - NEEDS REVIEW
---Sorts auctions based on specified parameters.
---[Documentation](https://warcraft.wiki.gg/wiki/API_SortAuctionSetSort)
---@param sortType string The type of sorting to apply
---@param sortAscending boolean Whether to sort in ascending order
---@return boolean success Indicates if the sorting operation was successful
function SortAuctionSetSort(sortType, sortAscending) end

---! DRAFT - NEEDS REVIEW
---Starts an auction based on the provided parameters. 
---[Documentation](https://warcraft.wiki.gg/wiki/API_StartAuction)
---@param itemID number The ID of the item to start auctioning.
---@param quantity number The quantity of the item.
---@param startingBid number The initial bid amount.
---@param buyoutPrice number The buyout price, if any.
---@param auctionTime number The auction duration in hours.
---@return boolean success True if the auction was successful, false otherwise.
function StartAuction(itemID, quantity, startingBid, buyoutPrice, auctionTime) end
