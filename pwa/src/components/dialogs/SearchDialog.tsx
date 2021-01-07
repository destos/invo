import { useQuery } from "@apollo/client"
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogProps,
  DialogTitle,
  InputAdornment,
  List,
  ListItem,
  TextField,
  Theme
} from "@material-ui/core"
import IconButton from "@material-ui/core/IconButton"
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction"
import CloseIcon from "@material-ui/icons/Close"
import SearchIcon from "@material-ui/icons/Search"
import { makeStyles } from "@material-ui/styles"
import {
  EntitySearchQuery,
  EntitySearchQueryVariables,
  SearchObjectFragment
} from "client/types"
import ItemListContent from "components/listItems/ItemListContent"
import SpaceListContent from "components/listItems/SpaceListContent"
import possibleTypes from "generated/possibleTypes.json"
import useSitu from "hooks/useSitu"
import { ENTITY_SEARCH } from "queries/search"
import React, { useState } from "react"

const itemTypes = possibleTypes.possibleTypes.ItemTypes
// const spaceTypes = possibleTypes.possibleTypes.SpaceTypes

const listItemType = (type: string) => {
  if (itemTypes.indexOf(type) !== -1) {
    return ItemListContent
  } else {
    return SpaceListContent
  }
}

// Dialog
const useStyles = makeStyles((theme: Theme) => ({
  root: {},
  listSection: {
    // background: theme.palette.grey[300]
    padding: 0
  }
}))

// The idea for this component is it is popped up when making many selections so a batch of irns
// can be scanned and then input into some part of the process.
// They can be removed from the selection before sent to the backend as official selections.
// May act as an alternative interface for when you want to really do batch scans/selections.

interface SearchDialogProps extends DialogProps {
  title: string
  anchorEl: any
  initialSearch?: string
}

const SearchDialog: React.FunctionComponent<SearchDialogProps> = ({
  title,
  anchorEl,
  initialSearch = "",
  ...dialogProps
}) => {
  const { onClose } = dialogProps
  const { select, unselect } = useSitu()

  const [search, setSearch] = useState<string>(initialSearch)
  const classes = useStyles()

  const closeDialog = (e: any, reason?: any) => {
    // TODO: Clear state?
    onClose && onClose(e, reason)
  }

  const { data } = useQuery<EntitySearchQuery, EntitySearchQueryVariables>(
    ENTITY_SEARCH,
    {
      fetchPolicy: "cache-and-network",
      variables: {
        text: search
      },
      skip: search === ""
    }
  )

  const results: EntitySearchQuery["entitySearch"] = data?.entitySearch ?? []

  // const handleToggleSubscription = (et: SubscribedEventTypeFragment) => {
  //   if (et.isObjectSubscribed) {
  //     onUnsubscribe(result.irn)
  //   } else {
  //     onSubscribe(result.irn)
  //   }
  // }

  // TODO: show the defaults that would be toggled and provide buttons that
  // turn those on and off? a toggle button at the top?
  return (
    <Dialog {...dialogProps}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <form>
          <TextField
            id="search"
            size="small"
            variant="outlined"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            autoFocus
            // label=""
            InputProps={{
              autoComplete: "off",
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              )
            }}
          />
        </form>
      </DialogContent>
      <DialogContent className={classes.listSection}>
        <List>
          {results.map((result) => {
            const ResultContent = listItemType(result.object.__typename ?? "")
            return (
              <ListItem
                key={result.irn}
                dense
                button={true}
                onClick={() => select(result.irn)}
              >
                <ResultContent
                  // @ts-ignore
                  entity={(result.object as never) as SearchObjectFragment}
                >
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      aria-label="comments"
                      onClick={() => unselect([result.irn])}
                    >
                      <CloseIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ResultContent>
              </ListItem>
            )
          })}
        </List>
      </DialogContent>
      <DialogActions>
        <Button
          onClick={() => closeDialog(undefined, undefined)}
          variant="outlined"
          startIcon={<CloseIcon />}
        >
          Close
        </Button>
        {/* <Button variant="contained" color="primary">
          Select
        </Button> */}
      </DialogActions>
    </Dialog>
  )
}

export default SearchDialog
