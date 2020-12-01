import { ListItemSecondaryAction, SvgIcon } from "@material-ui/core"
import ListItem, { ListItemProps } from "@material-ui/core/ListItem"
import ListItemIcon from "@material-ui/core/ListItemIcon"
import ListItemText from "@material-ui/core/ListItemText"
import BuildIcon from "@material-ui/icons/Build"
import LocalOfferIcon from "@material-ui/icons/LocalOffer"
import RemoveCircleIcon from "@material-ui/icons/RemoveCircle"
import RemoveCircleOutlineIcon from "@material-ui/icons/RemoveCircleOutline"
import React from "react"
import { ItemBitFragment } from "../../client/types"

const typeIconMap = {
  Item: LocalOfferIcon,
  Tool: BuildIcon,
  Consumable: RemoveCircleIcon,
  TrackedConsumable: RemoveCircleOutlineIcon,
  fallback: LocalOfferIcon
}

export type ItemListItemProps = ListItemProps & {
  entity: ItemBitFragment
}

const ItemListItem: React.FunctionComponent<ItemListItemProps> = ({
  entity,
  children,
  ...listItemProps
}) => {
  const { id, irn, name, spaceParents, __typename, qr } = entity
  const labelId = `item-list-label-${id}`
  const Icon = typeIconMap[__typename ?? "fallback"]

  const bread =
    spaceParents?.map((space) => space?.name ?? "Space").join(" > ") ?? null

  return (
    // @ts-ignore
    <ListItem {...listItemProps}>
      <ListItemIcon>
        <Icon />
      </ListItemIcon>
      <ListItemText id={labelId} primary={name} secondary={bread} />
      {children}
      <ListItemSecondaryAction>
        <img src={qr} width={80}/>
      </ListItemSecondaryAction>
    </ListItem>
  )
}

export default ItemListItem
