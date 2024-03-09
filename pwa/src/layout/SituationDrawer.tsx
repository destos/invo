import {
  AppBar,
  Box,
  Button,
  Divider,
  Drawer,
  DrawerProps,
  Grid,
  IconButton,
  List,
  ListItem,
  Toolbar,
  Typography,
  useTheme
} from "@material-ui/core"
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft"
import ChevronRightIcon from "@material-ui/icons/ChevronRight"
import SearchDialog from "components/dialogs/SearchDialog"
import ItemListContent from "components/listItems/ItemListContent"
import SpaceListContent from "components/listItems/SpaceListContent"
import useSitu from "hooks/useSitu"
import { bindPopover, usePopupState } from "material-ui-popup-state/hooks"
import React from "react"

interface SituationDrawerProps extends DrawerProps {}

// TODO: Contents for the situation drawer are the same used by the mobile situation dialog (swap to a dialog on small sizes)

const SituationDrawer: React.FC<SituationDrawerProps> = ({
  ...drawerProps
}) => {
  const theme = useTheme()

  const { situation, situDrawer } = useSitu()

  const searchPopupState = usePopupState({
    variant: "popover",
    popupId: "selectionSearchDialog"
  })

  return (
    <>
      <Drawer {...drawerProps}>
        <AppBar color="transparent" position="static" elevation={0}>
          <Toolbar>
            <IconButton onClick={situDrawer.close}>
              {theme.direction === "rtl" ? (
                <ChevronLeftIcon />
              ) : (
                <ChevronRightIcon />
              )}
            </IconButton>
            <Typography variant="h6">Selected</Typography>
            <Typography variant="h6">{situation?.state}</Typography>
          </Toolbar>
        </AppBar>
        <Divider />
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
        <Box p={2}>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Button
                fullWidth
                color="primary"
                variant="contained"
                {...bindPopover(searchPopupState)}
              >
                Select Space
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                fullWidth
                color="primary"
                variant="contained"
                {...bindPopover(searchPopupState)}
              >
                Select Item
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Drawer>
      <SearchDialog {...bindPopover(searchPopupState)} title="Select" />
    </>
  )
}

export default SituationDrawer
