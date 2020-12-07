import { ListItemSecondaryAction } from "@material-ui/core"
import ListItemIcon from "@material-ui/core/ListItemIcon"
import ListItemText from "@material-ui/core/ListItemText"
import BuildIcon from "@material-ui/icons/Build"
import LocalOfferIcon from "@material-ui/icons/LocalOffer"
import RemoveCircleIcon from "@material-ui/icons/RemoveCircle"
import RemoveCircleOutlineIcon from "@material-ui/icons/RemoveCircleOutline"
import { ItemListContentFragment } from "client/types"
import React from "react"

const typeIconMap = {
  Item: LocalOfferIcon,
  Tool: BuildIcon,
  Consumable: RemoveCircleIcon,
  TrackedConsumable: RemoveCircleOutlineIcon,
  fallback: LocalOfferIcon
}

export type ItemListContentProps = {
  entity: ItemListContentFragment
}

const ItemListContent: React.FC<ItemListContentProps> = ({
  entity,
  children
}) => {
  const { id, irn, name, spaceParents, __typename, qr } = entity
  const labelId = `item-list-label-${id}`
  const Icon = typeIconMap[__typename ?? "fallback"]

  const bread =
    spaceParents?.map((space) => space?.name ?? "Space").join(" > ") ?? null

  return (
    <>
      <ListItemIcon>
        <Icon />
      </ListItemIcon>
      <ListItemText id={labelId} primary={name} secondary={bread} />
      {children}
      <ListItemSecondaryAction>
        <img src={qr} width={80} alt="qr code" />
      </ListItemSecondaryAction>
    </>
  )
}

export default ItemListContent
