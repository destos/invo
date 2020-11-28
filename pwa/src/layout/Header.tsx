import React from "react"
import AppBar from "@material-ui/core/AppBar"
import Toolbar from "@material-ui/core/Toolbar"
import IconButton from "@material-ui/core/IconButton"
import Typography from "@material-ui/core/Typography"
import { fade, makeStyles } from "@material-ui/core/styles"
import MenuIcon from "@material-ui/icons/Menu"
import SearchIcon from "@material-ui/icons/Search"
import { Badge, Button, Chip } from "@material-ui/core"
import { Link as RouterLink } from "react-router-dom"
import useSitu from "../hooks/useSitu"

const useStyles = makeStyles((theme) => ({
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
    display: "none",
    [theme.breakpoints.up("sm")]: {
      display: "block",
    },
  },
  search: {
    position: "relative",
    borderRadius: theme.shape.borderRadius,
    backgroundColor: fade(theme.palette.common.white, 0.15),
    "&:hover": {
      backgroundColor: fade(theme.palette.common.white, 0.25),
    },
    marginLeft: 0,
    width: "100%",
    [theme.breakpoints.up("sm")]: {
      marginLeft: theme.spacing(1),
      width: "auto",
    },
  },
  searchIcon: {
    padding: theme.spacing(0, 2),
    height: "100%",
    position: "absolute",
    pointerEvents: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
}))

export default function Header() {
  const classes = useStyles()
  const { situation, searchPopup } = useSitu()

  return (
    <AppBar position="fixed">
      <Toolbar>
        <IconButton
          edge="start"
          className={classes.menuButton}
          color="inherit"
          aria-label="open drawer"
        >
          <MenuIcon />
        </IconButton>
        <Typography className={classes.title} variant="h6" noWrap>
          Invo
        </Typography>
        { situation ? (
          <>
          <Badge color="secondary" badgeContent={situation.spaces.length} overlap="circle">
            <Chip label="Spaces"/>
          </Badge>
          <Badge color="secondary" badgeContent={situation.items.length} overlap="circle">
            <Chip label="Items"/>
          </Badge>
          </>
        ): null}
        <Button component={RouterLink} to="/select">Select</Button>
        <Button component={RouterLink} to="/">Spaces</Button>
        <IconButton onClick={(e) => searchPopup.open(e)}>
          <SearchIcon/>
        </IconButton>
      </Toolbar>
    </AppBar>
  )
}
