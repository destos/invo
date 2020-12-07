import { Container, CssBaseline, Theme } from "@material-ui/core"
import { makeStyles } from "@material-ui/styles"
import React from "react"
import { renderRoutes, RouteConfig } from "react-router-config"
import Header from "./Header"
import {
  usePopupState,
  bindPopover
} from "material-ui-popup-state/hooks"
import SearchDialog from "components/dialogs/SearchDialog"
import { ActiveSituProvider } from "context/SituationContext"
import ShortcutDialog from "components/dialogs/ShortcutDialog"
// import globalKeyMap from "globalKeyMap"

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    paddingTop: 88
  }
}))

export interface IDashboardProps {
  route?: RouteConfig | undefined
}

const Root: React.FC<IDashboardProps> = ({ route }) => {
  const classes = useStyles()

  const searchPopupState = usePopupState({
    variant: "popover",
    popupId: "searchDialog"
  })

  const shortcutsPopupState = usePopupState({
    variant: "popover",
    popupId: "shortcutDialog"
  })

  const openShortcuts = React.useCallback(
    (e) => {
      shortcutsPopupState.open(e)
    },
    [shortcutsPopupState]
  )

  const handlers = {
    SHOW_DIALOG: openShortcuts
  }

  return (
    <ActiveSituProvider searchPopupState={searchPopupState}>
      <CssBaseline />
      <Header />
      <Container className={classes.root} maxWidth="xl" fixed>
        {renderRoutes(route?.routes)}
      </Container>
      <SearchDialog {...bindPopover(searchPopupState)} title="Search" />
      <ShortcutDialog {...bindPopover(shortcutsPopupState)} title="Search" />
    </ActiveSituProvider>
  )
}

export default Root
