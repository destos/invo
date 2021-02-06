import {
  Container,
  CssBaseline,
  LinearProgress,
  Theme
} from "@material-ui/core"
import { createStyles } from "@material-ui/core/styles"
import { makeStyles } from "@material-ui/styles"
import { ErrorBoundary } from "@sentry/react"
import { useAuth } from "client/auth"
import clsx from "clsx"
import SearchDialog from "components/dialogs/SearchDialog"
import ShortcutDialog from "components/dialogs/ShortcutDialog"
import { ActiveSituProvider } from "context/SituationContext"
import { bindPopover, usePopupState } from "material-ui-popup-state/hooks"
import { default as React, Suspense, useCallback } from "react"
import { renderRoutes, RouteConfig } from "react-router-config"
import { Redirect } from "react-router-dom"
import Header from "./Header"
import SituationDrawer from "./SituationDrawer"

const drawerWidth = 420

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      display: "flex"
    },
    appBar: {
      transition: theme.transitions.create(["margin", "width"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen
      })
    },
    appBarShift: {
      width: `calc(100% - ${drawerWidth}px)`,
      transition: theme.transitions.create(["margin", "width"], {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen
      }),
      marginRight: drawerWidth
    },
    drawer: {
      width: drawerWidth,
      flexShrink: 0
    },
    drawerPaper: {
      width: drawerWidth
    },
    drawerHeader: {
      display: "flex",
      alignItems: "center",
      padding: theme.spacing(0, 1),
      // necessary for content to be below app bar
      ...theme.mixins.toolbar,
      justifyContent: "flex-start"
    },
    content: {
      flexGrow: 1,
      padding: theme.spacing(3),
      transition: theme.transitions.create("margin", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen
      }),
      marginRight: -drawerWidth
    },
    contentShift: {
      transition: theme.transitions.create("margin", {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen
      }),
      marginRight: 0
    }
  })
)

export interface RootProps {
  route?: RouteConfig | undefined
}

const Root: React.FC<RootProps> = ({ route }) => {
  const classes = useStyles()
  const auth = useAuth()

  const searchPopupState = usePopupState({
    variant: "popover",
    popupId: "searchDialog"
  })

  const shortcutsPopupState = usePopupState({
    variant: "popover",
    popupId: "shortcutDialog"
  })

  const situDrawerState = usePopupState({
    variant: "popover",
    popupId: "situDrawer"
  })

  const openShortcuts = useCallback(
    (e) => {
      shortcutsPopupState.open(e)
    },
    [shortcutsPopupState]
  )

  if (auth.user === null) {
    return <Redirect to="/auth/login" />
  }

  const handlers = {
    SHOW_DIALOG: openShortcuts
  }

  return (
    <div className={classes.root}>
      <ActiveSituProvider interactions={{ searchPopupState, situDrawerState }}>
        <CssBaseline />
        <Header
          position="fixed"
          color="primary"
          className={clsx(classes.appBar, {
            [classes.appBarShift]: situDrawerState.isOpen
          })}
        />
        <main
          className={clsx(classes.content, {
            [classes.contentShift]: situDrawerState.isOpen
          })}
        >
          <div className={classes.drawerHeader} />
          <Container maxWidth="xl">
            <ErrorBoundary fallback={"An error occurred"}>
              <Suspense fallback={<LinearProgress />}>
                {renderRoutes(route?.routes)}
              </Suspense>
            </ErrorBoundary>
          </Container>
        </main>
        <SituationDrawer
          {...bindPopover(situDrawerState)}
          className={classes.drawer}
          variant="persistent"
          anchor="right"
          classes={{
            paper: classes.drawerPaper
          }}
        />
        <SearchDialog {...bindPopover(searchPopupState)} title="Search" />
        <ShortcutDialog {...bindPopover(shortcutsPopupState)} title="Search" />
      </ActiveSituProvider>
    </div>
  )
}

export default Root
