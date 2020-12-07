// Show the top level spaces in your invo app
import { useMutation, useQuery } from "@apollo/client"
import {
  Badge,
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  Link,
  Tab,
  Theme,
  Typography
} from "@material-ui/core"
import ListIcon from "@material-ui/icons/List"
import TabIcon from "@material-ui/icons/Tab"
import VerticalSplitIcon from "@material-ui/icons/VerticalSplit"
import {
  TabContext,
  TabList,
  TabPanel,
  ToggleButton,
  ToggleButtonGroup
} from "@material-ui/lab"
import { makeStyles } from "@material-ui/styles"
import {
  GetNavigationSpaceQuery,
  GetNavigationSpaceQueryVariables,
  ItemListContentFragment,
  UpdateSpaceLayoutMutation,
  UpdateSpaceLayoutMutationVariables
} from "client/types"
import AddItemDialog from "components/dialogs/AddItemDialog"
import useSitu from "hooks/useSitu"
import _ from "lodash"
import {
  bindPopover,
  bindTrigger,
  usePopupState
} from "material-ui-popup-state/hooks"
import { GET_NAVIGATION_SPACE, UPDATE_SPACE_LAYOUT } from "queries/spaces"
import React, { FC, useState } from "react"
import GridLayout, {
  ItemCallback,
  ReactGridLayoutProps,
  WidthProvider
} from "react-grid-layout"
import { Link as RouterLink, RouteComponentProps } from "react-router-dom"
import { relayDeconstructor } from "relay-connections-deconstructor"
import { spaceDetailUrl } from "routes"
import ItemsList from "./components/ItemsList"

// TODO: when we detect the space is a leaf node, don't care about displaying layout

const useStyles = makeStyles((theme: Theme) => ({
  gridLayout: { width: "100%" },
  card: { height: "100%" },
  fookingPanel: {
    padding: 0
  }
}))

type SpaceRouteProps = {
  id: string
}

type SpaceProps = RouteComponentProps<SpaceRouteProps> & {}

type LayoutProps = {
  space: GetNavigationSpaceQuery["space"] | undefined
  handleChange: ItemCallback
}

// @ts-ignore
const BaseGridLayout: FC<LayoutProps> = ({ width, space, handleChange }) => {
  const classes = useStyles()
  const cols = 12
  const scale = width / cols
  const gridProps: ReactGridLayoutProps = {
    className: classes.gridLayout,
    // items: 50,
    cols,
    rowHeight: scale,
    width,
    // containerWidth: 100,
    // verticalCompact: false,
    // compactType: "vertical",
    compactType: null,
    preventCollision: true
    // resizeHandles: ['s', 'w', 'e', 'n', 'sw', 'nw', 'se', 'ne']
  }
  // TODO: container grid ( queried grid ) supplies these values
  // const spaceGridConfig = {
  //   cols: 12
  // }

  const layout = space?.children.map((space) => {
    return { i: space.id, ...space.layout }
  })

  return (
    <GridLayout
      {...gridProps}
      // @ts-ignore
      layout={layout}
      onDragStop={handleChange}
      onResizeStop={handleChange}
      // onDrop={handleChange}
    >
      {space?.children.map((space) => {
        return (
          <div key={space.id}>
            <Card elevation={3} className={classes.card}>
              <CardHeader
                title={space.name}
                to={spaceDetailUrl(space.id)}
                component={RouterLink}
                color="textPrimary"
              />
              <CardContent>{space.itemCount}</CardContent>
            </Card>
          </div>
        )
      })}
    </GridLayout>
  )
}

const Layout = WidthProvider(BaseGridLayout)

const Space: FC<SpaceProps> = ({ match }) => {
  // TODO: leaf space nodes act differently.
  // TODO: tab interface to show all direct/child items then switch to space gid view
  const situ = useSitu()

  const classes = useStyles()
  const [tabView, setTabView] = useState("layout")
  const [pageLayout, setPageLayout] = useState("tabs")

  const handleViewChange = (event: React.ChangeEvent<{}>, newView: string) => {
    setTabView(newView)
  }

  const handlePageLayout = (
    event: React.MouseEvent<HTMLElement>,
    newPageLayout: string | null
  ) => {
    if (newPageLayout !== null) {
      setPageLayout(newPageLayout)
    }
  }

  const addItemPopupState = usePopupState({
    variant: "popover",
    popupId: "addItemDialog"
  })

  const addSpacePopupState = usePopupState({
    variant: "popover",
    popupId: "addSpaceDialog"
  })

  const { data } = useQuery<
    GetNavigationSpaceQuery,
    GetNavigationSpaceQueryVariables
  >(GET_NAVIGATION_SPACE, {
    fetchPolicy: "cache-and-network",
    variables: {
      id: match.params.id
    }
  })
  const space = data?.space

  const [updateLayout] = useMutation<
    UpdateSpaceLayoutMutation,
    UpdateSpaceLayoutMutationVariables
  >(UPDATE_SPACE_LAYOUT)

  const handleChange = (layout: any, oldItem: any, newItem: any) => {
    updateLayout({
      variables: {
        id: newItem.i,
        layout: _.pick(newItem, ["x", "y", "w", "h"])
      }
    })
  }
  const itemData = relayDeconstructor(
    space?.items
  ) as Array<ItemListContentFragment>

  const Content =
    pageLayout === "tabs" ? (
      <TabContext value={tabView}>
        <TabList onChange={handleViewChange}>
          <Tab value="layout" label="Layout" />
          <Tab
            value="items"
            label={
              <Badge
                badgeContent={space?.itemCount}
                color="secondary"
                overlap="rectangle"
              >
                <Typography variant="button">Items</Typography>
                &nbsp; &nbsp;
              </Badge>
            }
          />
        </TabList>
        <Divider />
        <TabPanel value="layout" className={classes.fookingPanel}>
          <Layout
            space={space}
            handleChange={handleChange}
            measureBeforeMount={true}
          />
        </TabPanel>
        <TabPanel value="items" className={classes.fookingPanel}>
          <ItemsList itemData={itemData} />
        </TabPanel>
      </TabContext>
    ) : pageLayout === "split" ? (
      <Grid container spacing={3}>
        <Grid item xs={12} lg={10} md={11}>
          <Layout
            space={space}
            handleChange={handleChange}
            measureBeforeMount={true}
          />
        </Grid>
        <Grid item xs={12} lg={2} md={3}>
          <ItemsList itemData={itemData} />
        </Grid>
      </Grid>
    ) : (
      <ItemsList itemData={itemData} />
      // <List>
      //   {itemData?.map((item) => (
      //     <ListItem key={item.irn}>
      //       <ItemListContent entity={item} />
      //     </ListItem>
      //   ))}
      // </List>
    )

  return (
    <>
      <Breadcrumbs
        maxItems={5}
        itemsAfterCollapse={3}
        expandText="Show all spaces"
        key={space?.id}
      >
        <Link component={RouterLink} to={"/"}>
          Spaces
        </Link>
        {space?.parents.map((parent) => (
          <Link component={RouterLink} to={spaceDetailUrl(parent.id)}>
            {parent.name}
          </Link>
        ))}
        <Typography color="textPrimary">{space?.name}</Typography>
      </Breadcrumbs>
      <Grid container>
        <Grid item>
          <Typography variant="h3">{space?.name}</Typography>
        </Grid>
        <Grid item>
          <Button {...bindTrigger(addItemPopupState)}>Add Item</Button>
          <Button {...bindTrigger(addSpacePopupState)}>Add Space</Button>
          <Button
            onClick={(e) => {
              situ.select([space?.irn])
            }}
          >
            Select
          </Button>
        </Grid>
        <Grid item>
          <ToggleButtonGroup
            value={pageLayout}
            size="small"
            onChange={handlePageLayout}
            exclusive
          >
            <ToggleButton value="tabs">
              <TabIcon />
            </ToggleButton>
            <ToggleButton value="split">
              <VerticalSplitIcon />
            </ToggleButton>
            <ToggleButton value="list">
              <ListIcon />
            </ToggleButton>
          </ToggleButtonGroup>
        </Grid>
      </Grid>
      {Content}
      <AddItemDialog spaceId={space?.id} {...bindPopover(addItemPopupState)} />
      <AddItemDialog spaceId={space?.id} {...bindPopover(addSpacePopupState)} />
    </>
  )
}

export default Space
