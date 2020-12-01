import { ListItemSecondaryAction } from "@material-ui/core"
import ListItem, { ListItemProps } from "@material-ui/core/ListItem"
import ListItemIcon from "@material-ui/core/ListItemIcon"
import ListItemText from "@material-ui/core/ListItemText"
import CheckBoxOutlineBlankIcon from "@material-ui/icons/CheckBoxOutlineBlank"
import GridOnIcon from "@material-ui/icons/GridOn"
import React from "react"
import { SpaceBitFragment } from "../../client/types"

const typeIconMap = {
  SpaceNode: CheckBoxOutlineBlankIcon,
  GridSpaceNode: GridOnIcon,
  fallback: CheckBoxOutlineBlankIcon
}

export type SpaceListItemProps = ListItemProps & {
  entity: SpaceBitFragment
}

const SpaceListItem: React.FunctionComponent<SpaceListItemProps> = ({
  entity,
  children,
  ...listItemProps
}) => {
  const { id, irn, name, __typename, qr } = entity
  const labelId = `space-list-label-${id}`
  const Icon = typeIconMap[__typename ?? "fallback"]

  return (
    // @ts-ignore
    <ListItem {...listItemProps}>
      <ListItemIcon>
        <Icon />
      </ListItemIcon>
      <ListItemText id={labelId} primary={name} secondary={irn} />
      {children}
      <ListItemSecondaryAction>
        <img src={qr} width={80}/>
      </ListItemSecondaryAction>
    </ListItem>
  )
}

export default SpaceListItem
