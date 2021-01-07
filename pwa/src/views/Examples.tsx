// Show the top level spaces in your invo app
import { Grid, Link, Theme } from "@material-ui/core"
import { makeStyles } from "@material-ui/styles"
import AddItemDialog from "components/dialogs/AddItemDialog"
import AddSpaceForm from "components/forms/AddSpaceForm"
import React, { FC } from "react"
import {
  Link as RouterLink,
  Redirect,
  RouteComponentProps
} from "react-router-dom"

// TODO: when we detect the space is a leaf node, don't care about displaying layout

const useStyles = makeStyles((theme: Theme) => ({
  root: {}
}))

type ExamplesRouteProps = {
  example?: string
}

type ExamplesProps = RouteComponentProps<ExamplesRouteProps> & {}

const ExamplesMap = {
  addItemDialog: () => (
    <AddItemDialog
      open={true}
      spaceId="1"
      hideBackdrop={true}
      disableBackdropClick={true}
      BackdropProps={{ invisible: true }}
    />
  ),
  addSpaceForm: () => <AddSpaceForm />
}

const Examples: FC<ExamplesProps> = ({ match }) => {
  const { example } = match.params
  const classes = useStyles()
  const exampleKeys = Object.keys(ExamplesMap)

  if (example === undefined) {
    return <Redirect to={`/examples/${exampleKeys[0]}`} />
  }
  // @ts-ignore
  const Component = ExamplesMap[example]
  return (
    <>
      <Grid container>
        <Grid item>
          {exampleKeys.map((key) => (
            <Link component={RouterLink} to={`/examples/${exampleKeys[0]}`}>
              {key}
            </Link>
          ))}
        </Grid>
        <Grid item>
          <Component />
        </Grid>
      </Grid>
    </>
  )
}

export default Examples
