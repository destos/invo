import { useLazyQuery } from "@apollo/client"
import {
  fade,
  InputBase,
  ListSubheader,
  makeStyles,
  Theme
} from "@material-ui/core"
import CircularProgress from "@material-ui/core/CircularProgress"
import SearchIcon from "@material-ui/icons/Search"
import Autocomplete from "@material-ui/lab/Autocomplete"
import {
  ItemSearchQuery,
  ItemSearchQueryVariables,
  SearchItemFragment
} from "client/types"
import { ITEM_SEARCH } from "queries/search"
import { FC, useCallback, useState } from "react"

// Omit<AutocompleteProps<false, false, false false>, "options" | "loading" | "renderInput" >
// size: AutocompleteProps["size"]
interface ItemSearchProps {
  onSelect?: (value: SearchItemFragment) => void
}

const useStyles = makeStyles((theme: Theme) => ({
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
    padding: theme.spacing(0, 1),
    height: "100%",
    position: "absolute",
    pointerEvents: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
  inputRoot: {
    color: "inherit"
  },
  inputInput: {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(0.4em + ${theme.spacing(4)}px)`,
    transition: theme.transitions.create("width"),
    width: "100%"
    // [theme.breakpoints.up("sm")]: {
    //   width: "12ch",
    //   "&:focus": {
    //     width: "20ch"
    //   }
    // }
  },
  listbox: {
    margin: 0,
    padding: 0,
    zIndex: 1,
    position: "absolute",
    listStyle: "none",
    backgroundColor: theme.palette.background.paper,
    overflow: "auto",
    border: "1px solid rgba(0,0,0,.25)",
    '& li[data-focus="true"]': {
      backgroundColor: "#4a8df6",
      color: "white",
      cursor: "pointer"
    },
    "& li:active": {
      backgroundColor: "#2977f5",
      color: "white"
    }
  },
  /* Styles applied to the group's label elements. */
  groupLabel: {
    backgroundColor: theme.palette.background.paper,
    top: -8
  },
  /* Styles applied to the group's ul elements. */
  groupUl: {
    padding: 0,
    "& $option": {
      paddingLeft: 24
    }
  }
}))

const ItemSearchAutocomplete: FC<ItemSearchProps> = ({ onSelect }) => {
  const classes = useStyles()
  const [open, setOpen] = useState(false)
  const [options, setOptions] = useState<Array<SearchItemFragment>>([])

  const [doSearch, { data, loading }] = useLazyQuery<
    ItemSearchQuery,
    ItemSearchQueryVariables
  >(ITEM_SEARCH, {
    fetchPolicy: "cache-and-network",
    onCompleted: ({ itemSearch: { edges, pageInfo } }) => {
      // @ts-ignore
      setOptions(edges.map((edge) => edge.node))
    }
  })

  // const buildQuery: (search: string) => OperationVariables = useCallback(
  //   search => ({
  //     variables: {
  //       ...queryVariables,
  //       filter: {
  //         ...(queryVariables.filter || {}),
  //         search
  //       }
  //     }
  //   }),
  //   [queryVariables]
  // )

  const buildQuery = useCallback((search: string) => {
    return {
      variables: {
        search,
        first: 10
      },
      skip: search === ""
    }
  }, [])

  // useEffect(() => {
  //   if (!open) {
  //     setOptions([]);
  //   }
  // }, [open]);

  const handleChange = (e: any, value: string = "") => {
    // @ts-ignore
    doSearch({
      ...buildQuery(value)
    })
  }

  const handleSelect = (
    event: object,
    value: SearchItemFragment | null,
    reason: string
  ) => {
    if (reason === "select-option" && !!value) {
      onSelect && onSelect(value)
    }
  }

  return (
    <Autocomplete
      options={options}
      loading={loading}
      size={"small"}
      open={open}
      onOpen={() => {
        setOpen(true)
      }}
      onClose={() => {
        setOpen(false)
      }}
      onInputChange={handleChange}
      getOptionSelected={(option, value) => option.id === value.id}
      getOptionLabel={(option) => option.name}
      groupBy={(option) => {
        if (!!option.space?.parents) {
          const bits = option.space.parents?.map(
            (space) => space?.name ?? "Space"
          )
          bits.push(option.space.name)
          return bits.join(" / ") ?? null
        }
        return option.space?.name ?? "No Space"
      }}
      selectOnFocus
      clearOnBlur
      handleHomeEndKeys
      onChange={handleSelect}
      renderInput={(params) => (
        <div className={classes.search}>
          <div className={classes.searchIcon}>
            <SearchIcon />
          </div>
          <InputBase
            ref={params.InputProps.ref}
            placeholder="Search Items…"
            classes={{
              root: classes.inputRoot,
              input: classes.inputInput
            }}
            inputProps={{ ...params.inputProps }}
            endAdornment={
              <>
                {loading ? (
                  <CircularProgress color="inherit" size={26} />
                ) : (
                  <CircularProgress
                    variant="determinate"
                    color="inherit"
                    size={26}
                    value={0}
                  />
                )}
              </>
            }
          />
        </div>
      )}
    />
  )
}

export default ItemSearchAutocomplete
