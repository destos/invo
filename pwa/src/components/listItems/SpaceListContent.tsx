import { ListItemSecondaryAction } from "@material-ui/core"
import ListItemIcon from "@material-ui/core/ListItemIcon"
import ListItemText from "@material-ui/core/ListItemText"
import CheckBoxOutlineBlankIcon from "@material-ui/icons/CheckBoxOutlineBlank"
import GridOnIcon from "@material-ui/icons/GridOn"
import { SpaceListContentFragment } from "client/types"
import React from "react"

const typeIconMap = {
  SpaceNode: CheckBoxOutlineBlankIcon,
  GridSpaceNode: GridOnIcon,
  fallback: CheckBoxOutlineBlankIcon
}

export type SpaceListContentProps = {
  entity: SpaceListContentFragment
}

const SpaceListContent: React.FunctionComponent<SpaceListContentProps> = ({
  entity,
  children
}) => {
  const { id, irn, name, __typename, qr } = entity
  const labelId = `space-list-label-${id}`
  const Icon = typeIconMap[__typename ?? "fallback"]

  return (
    <>
      <ListItemIcon>
        <Icon />
      </ListItemIcon>
      <ListItemText id={labelId} primary={name} secondary={irn} />
      {children}
      <ListItemSecondaryAction>
        <img src={qr} width={80} />
      </ListItemSecondaryAction>
    </>
  )
}

export default SpaceListContent
