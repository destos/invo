import { Badge, Button, Link, Menu, MenuItem, MenuList } from "@material-ui/core"
import AppBar, { AppBarProps } from "@material-ui/core/AppBar"
import IconButton from "@material-ui/core/IconButton"
import { fade, makeStyles } from "@material-ui/core/styles"
import Toolbar from "@material-ui/core/Toolbar"
import Typography from "@material-ui/core/Typography"
import AppsIcon from "@material-ui/icons/Apps"
import MenuIcon from "@material-ui/icons/Menu"
import SearchIcon from "@material-ui/icons/Search"
import { SearchItemFragment } from "client/types"
import ItemSearchAutocomplete from "components/autocompletes/ItemSearchAutocomplete"
import useSitu from "hooks/useSitu"
import {
  bindMenu,
  bindToggle,
  usePopupState
} from "material-ui-popup-state/hooks"
import React from "react"
import { Link as RouterLink, useHistory } from "react-router-dom"
import { spaceItemDetailUrl } from "routes"

const useStyles = makeStyles((theme) => ({
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1,
    display: "none",
    [theme.breakpoints.up("sm")]: {
      display: "block"
    }
  },
  search: {
    position: "relative",
    borderRadius: theme.shape.borderRadius,
    backgroundColor: fade(theme.palette.common.white, 0.15),
    "&:hover": {
      backgroundColor: fade(theme.palette.common.white, 0.25)
    },
    marginLeft: 0,
    width: "100%",
    [theme.breakpoints.up("sm")]: {
      marginLeft: theme.spacing(1),
      width: "auto"
    }
  },
  searchIcon: {
    padding: theme.spacing(0, 2),
    height: "100%",
    position: "absolute",
    pointerEvents: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }
}))

export interface HeaderProps extends AppBarProps {}

const Header: React.FC<HeaderProps> = ({ ...appBarProps }) => {
  const history = useHistory()
  const classes = useStyles()
  const { situation, site, sites, searchPopup, situDrawer } = useSitu()

  const siteMenuState = usePopupState({
    variant: "popover",
    popupId: "siteMenu"
  })

  const handleSelect = (value: SearchItemFragment) => {
    if (value.space) {
      history.push(spaceItemDetailUrl(value.space.id, value.id))
    }
  }

  return (
    <AppBar {...appBarProps}>
      <Toolbar>
        <IconButton
          {...bindToggle(siteMenuState)}
          edge="start"
          className={classes.menuButton}
          color="inherit"
          aria-label="open drawer"
        >
          <MenuIcon />
        </IconButton>
        <Menu
          {...bindMenu(siteMenuState)}
          getContentAnchorEl={null}
          keepMounted
          anchorOrigin={{
            vertical: "bottom",
            horizontal: "left"
          }}
          transformOrigin={{
            vertical: "top",
            horizontal: "left"
          }}
        >
          <MenuList>
            {sites.map((site)=> (
              <MenuItem component={Link} href={site.domain} color="inherit">{site.name}</MenuItem>
            ))}
          </MenuList>
        </Menu>
        <Typography className={classes.title} variant="h6" noWrap>
          Invo ({site?.name})
        </Typography>
        <ItemSearchAutocomplete onSelect={handleSelect} />
        <IconButton component={RouterLink} to="/">
          <AppsIcon />
        </IconButton>
        <Button component={RouterLink} to="/select">
          Select
        </Button>
        <IconButton onClick={(e) => searchPopup.open(e)}>
          <SearchIcon />
        </IconButton>
        {situation && !situDrawer.isOpen ? (
          <>
            <Badge
              color="secondary"
              badgeContent={situation.spaces.length + situation.items.length}
              overlap="circle"
            >
              <IconButton
                {...bindToggle(situDrawer)}
                edge="end"
                color="inherit"
                aria-label="open situation drawer"
              >
                <MenuIcon />
              </IconButton>
            </Badge>
          </>
        ) : null}
      </Toolbar>
    </AppBar>
  )
}

export default Header
