// Show the top level spaces in your invo app
import { useMutation, useQuery } from "@apollo/client"
import {
  Box,
  Breadcrumbs,
  Card,
  CardContent,
  CardHeader,
  Link,
  Theme,
  Typography
} from "@material-ui/core"
import { Link as RouterLink } from "react-router-dom"
import { makeStyles } from "@material-ui/styles"
import _ from "lodash"
import React, { FC } from "react"
import GridLayout, { ReactGridLayoutProps } from "react-grid-layout"
import { RouteComponentProps } from "react-router-dom"
import {
  GetNavigationSpaceQuery,
  GetNavigationSpaceQueryVariables,
  UpdateSpaceLayoutMutation,
  UpdateSpaceLayoutMutationVariables
} from "../client/types"
import { GET_NAVIGATION_SPACE, UPDATE_SPACE_LAYOUT } from "../queries/spaces"
import useWidth from "../hooks/useWidth"
import { spaceDetailUrl } from "../routes"

const useStyles = makeStyles((theme: Theme) => ({
  gridLayout: { width: "100%" },
  card: { height: "100%" }
}))

type SpaceRouteProps = {
  id: string
}

type SpaceProps = RouteComponentProps<SpaceRouteProps> & {}

const Space: FC<SpaceProps> = ({ match }) => {
  const classes = useStyles()
  const width = useWidth()

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
  const spaceGridConfig = {
    cols: 12
  }

  const [updateLayout] = useMutation<
    UpdateSpaceLayoutMutation,
    UpdateSpaceLayoutMutationVariables
  >(UPDATE_SPACE_LAYOUT)

  const layout = space?.children.map((space) => {
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
      <Breadcrumbs maxItems={4}>
        {space?.parents.map((parent) => (
          <Link component={RouterLink} to={spaceDetailUrl(parent.id)}>
            {parent.name}
          </Link>
        ))}
      </Breadcrumbs>
      <Box>
        <Typography variant="h2">{space?.name}</Typography>
      </Box>
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
                <CardHeader title={space.name} to={spaceDetailUrl(space.id)} component={RouterLink}/>
                <CardContent>{space.itemCount}</CardContent>
              </Card>
            </div>
          )
        })}
      </GridLayout>
    </>
  )
}

export default Space
