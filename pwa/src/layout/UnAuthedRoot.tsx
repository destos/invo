import Box from "@material-ui/core/Box"
import Container from "@material-ui/core/Container"
import CssBaseline from "@material-ui/core/CssBaseline"
import Link from "@material-ui/core/Link"
import { makeStyles } from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"
import { useAuth } from "client/auth"
import React from "react"
import { renderRoutes } from "react-router-config"
import { Redirect } from "react-router-dom"
import { RootProps } from "./Root"

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href={`https://${process.env.REACT_APP_DOMAIN}`}>
        My Invo App
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  )
}

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(3)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  }
}))

const UnAuthedRoot: React.FC<RootProps> = ({ route }) => {
  const classes = useStyles()
  const auth = useAuth()
  if (auth.user !== null) {
    return <Redirect to="/" />
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>{renderRoutes(route?.routes)}</div>
      <Box mt={5}>
        <Copyright />
      </Box>
    </Container>
  )
}
export default UnAuthedRoot
