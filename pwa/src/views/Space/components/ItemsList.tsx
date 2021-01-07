// Show the top level spaces in your invo app
import { List, ListItem } from "@material-ui/core"
import { ItemListContentFragment } from "client/types"
import ItemListContent from "components/listItems/ItemListContent"
import React, { FC } from "react"

// TODO: this becomes the filterable nested list of items on the space view
// Use existing patterns for filtering and forms from job

type ItemsListProps = {
  itemData: Array<ItemListContentFragment>
}

// This doesn't FIX THE FUCKING ISSUE
const ItemsList: FC<ItemsListProps> = ({ itemData }) => (
  <List>
    {itemData?.map((item) => (
      <ListItem key={item.irn}>
        <ItemListContent key={item.irn} entity={item} />
      </ListItem>
    ))}
  </List>
)

export default ItemsList
