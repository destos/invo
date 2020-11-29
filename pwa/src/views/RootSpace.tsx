// Show the top level spaces in your invo app
import { useMutation, useQuery } from "@apollo/client"
import { Card, CardContent, CardHeader, Theme } from "@material-ui/core"
import { makeStyles } from "@material-ui/styles"
import _ from "lodash"
import React, { FC } from "react"
import GridLayout, { ReactGridLayoutProps } from "react-grid-layout"
import {
  GetRootSpacesQuery,
  GetRootSpacesQueryVariables,
  UpdateSpaceLayoutMutation,
  UpdateSpaceLayoutMutationVariables
} from "../client/types"
import { GET_ROOT_SPACES, UPDATE_SPACE_LAYOUT } from "../queries/spaces"

const useStyles = makeStyles((theme: Theme) => ({
  rootSpaces: { width: "100%" },
  card: { height: "100%" }
}))

type RootSpaceProps = {}

const RootSpace: FC<RootSpaceProps> = () => {
  const classes = useStyles()
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
              <CardHeader title={space.name} />
              <CardContent>What</CardContent>
            </Card>
          </div>
        )
      })}
    </GridLayout>
  )
}

export default RootSpace
