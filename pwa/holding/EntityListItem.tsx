import { ListItem, ListItemText } from "@material-ui/core"
import SpaceListContent from "../src/components/ListItems/SpaceListContent"
import ItemListContent from "../src/components/ListItems/ItemListContent"
import React from "react"
import possibleTypes from "../src/generated/possibleTypes.json"

const itemTypes = possibleTypes.possibleTypes.ItemTypes
const spaceTypes = possibleTypes.possibleTypes.SpaceTypes

// For when you need to dynamically load the entity details

type FallbackListItemProps = {
  irn: string
}

const FallbackListItem: React.FC<FallbackListItemProps> = ({ irn }) => {
  return (
    <ListItem>
      <ListItemText primary={irn} />
    </ListItem>
  )
}

type IRNListItemProps = {
  irn: string
}

const IRNListItem: React.FC<IRNListItemProps> = ({ irn }) => {
  // switch the list item display after the irn resolves
  // Use the cache to quickly resolve the irn query
  // When the real data comes back it should update with any new data.
  // swaps to the
  return <FallbackListItem irn={irn} />
}

export default IRNListItem
