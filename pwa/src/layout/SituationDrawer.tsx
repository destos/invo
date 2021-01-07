import { Drawer, DrawerProps, List, ListItem } from "@material-ui/core"
import ItemListContent from "components/listItems/ItemListContent"
import SpaceListContent from "components/listItems/SpaceListContent"
import useSitu from "hooks/useSitu"
import React from "react"

interface SituationDrawerProps extends DrawerProps {}

// Contents for the situation drawer are the same used by the mobile situation drawer

const SituationDrawer: React.FC<SituationDrawerProps> = ({
  ...drawerProps
}) => {
  const { situation } = useSitu()
  return (
    <Drawer {...drawerProps}>
      {situation ? (
        <List>
          {situation.spaces.map((space) => (
            <ListItem key={space.irn}>
              <SpaceListContent key={space.irn} entity={space} />
            </ListItem>
          ))}
          {situation.items.map((item) => (
            <ListItem key={item.irn}>
              <ItemListContent entity={item} />
            </ListItem>
          ))}
        </List>
      ) : (
        "No situation"
      )}
    </Drawer>
  )
}

export default SituationDrawer
