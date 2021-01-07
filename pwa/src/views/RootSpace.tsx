// Show the top level spaces in your invo app
import { useMutation, useQuery } from "@apollo/client"
import {
  Link,
  Card,
  CardContent,
  CardHeader,
  Theme,
  Breadcrumbs,
  Grid,
  Typography,
  Button
} from "@material-ui/core"
import { makeStyles } from "@material-ui/styles"
import {
  GetRootSpacesQuery,
  GetRootSpacesQueryVariables,
  UpdateSpaceLayoutMutation,
  UpdateSpaceLayoutMutationVariables
} from "client/types"
import AddSpaceDialog from "components/dialogs/AddSpaceDialog"
import _ from "lodash"
import { bindTrigger, bindPopover } from "material-ui-popup-state/core"
import { usePopupState } from "material-ui-popup-state/hooks"
import { GET_ROOT_SPACES, UPDATE_SPACE_LAYOUT } from "queries/spaces"
import React, { FC } from "react"
import GridLayout, { ReactGridLayoutProps } from "react-grid-layout"
import { Link as RouterLink } from "react-router-dom"
import { spaceDetailUrl } from "routes"

const useStyles = makeStyles((theme: Theme) => ({
  rootSpaces: { width: "100%" },
  card: { height: "100%" }
}))

type RootSpaceProps = {}

const RootSpace: FC<RootSpaceProps> = () => {
  const classes = useStyles()

  const addSpacePopupState = usePopupState({
    variant: "popover",
    popupId: "addSpaceDialog"
  })

  const gridProps: ReactGridLayoutProps = {
    className: classes.rootSpaces,
    // items: 50,
    cols: 12,
    rowHeight: 30,
    width: 1000,
    // containerWidth: 100,
    // verticalCompact: false,
    // compactType: "vertical",
    compactType: null,
    preventCollision: true
  }
  const { data } = useQuery<GetRootSpacesQuery, GetRootSpacesQueryVariables>(
    GET_ROOT_SPACES,
    {
      fetchPolicy: "network-only"
    }
  )

  const [updateLayout] = useMutation<
    UpdateSpaceLayoutMutation,
    UpdateSpaceLayoutMutationVariables
  >(UPDATE_SPACE_LAYOUT)

  const layout = data?.spaces.map((space) => {
    return { i: space.id, ...space.layout }
  })

  const handleChange = (layout: any, oldItem: any, newItem: any) => {
    updateLayout({
      variables: {
        id: newItem.i,
        layout: _.pick(newItem, ["x", "y", "w", "h"])
      }
    })
  }

  return (
    <>
      <Breadcrumbs
        maxItems={5}
        itemsAfterCollapse={3}
        expandText="Show all spaces"
        key="root"
      >
        <Link component={RouterLink} to="/">
          Spaces
        </Link>
      </Breadcrumbs>
      <Grid container>
        <Grid item>
          <Typography variant="h3">Root Spaces</Typography>
        </Grid>
        <Grid item>
          <Button {...bindTrigger(addSpacePopupState)}>Add Space</Button>
        </Grid>
      </Grid>
      <GridLayout
        {...gridProps}
        // @ts-ignore
        layout={layout}
        onDragStop={handleChange}
        onResizeStop={handleChange}
        // onDrop={handleChange}
      >
        {data?.spaces.map((space) => {
          return (
            <div key={space.id}>
              <Card elevation={3} className={classes.card}>
                <CardHeader
                  title={space.name}
                  to={spaceDetailUrl(space.id)}
                  component={Link}
                />
                <CardContent>{space.itemCount}</CardContent>
              </Card>
            </div>
          )
        })}
      </GridLayout>
      <AddSpaceDialog {...bindPopover(addSpacePopupState)} />
    </>
  )
}

export default RootSpace
