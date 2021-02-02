import { useMutation } from "@apollo/client"
import { TextField } from "@material-ui/core"
import Avatar from "@material-ui/core/Avatar"
import Button from "@material-ui/core/Button"
import Checkbox from "@material-ui/core/Checkbox"
import FormControlLabel from "@material-ui/core/FormControlLabel"
import Grid from "@material-ui/core/Grid"
import Link from "@material-ui/core/Link"
import { makeStyles } from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"
import LockOutlinedIcon from "@material-ui/icons/LockOutlined"
import { newTokenEvent } from "client/auth"
import React from "react"
import { useForm } from "react-hook-form"
import { Link as RouterLink, useHistory } from "react-router-dom"
import { yupResolver } from "utils/yup"
import schema from "./loginSchema"

const useStyles = makeStyles((theme) => ({
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

export default function SignUp() {
  const classes = useStyles()
  // const history = useHistory()
  // const formContext = useForm<FormValues>({
  //   context: {
  //     cast: "validate"
  //   },
  //   defaultValues,
  //   resolver: yupResolver(schema, { strict: false })
  // })
  // const { reset } = formContext

  // const [signIn] = useMutation<SignInMutation, SignInMutationVariables>(SIGN_IN)

  // const doSubmit = async (data: FormValues) => {
  //   const {
  //     // @ts-ignore
  //     data: { token }
  //   } = await signIn({
  //     variables: data
  //   })
  //   if (token) {
  //     reset(defaultValues)
  //     const event = newTokenEvent(token)
  //     // Redirect
  //     history.replace("/")
  //   } else {
  //     formContext.setError("password", {
  //       type: "validate",
  //       shouldFocus: true,
  //       message: "Password is incorrect"
  //     })
  //   }
  // }

  return (
    <>
      <Avatar className={classes.avatar}>
        <LockOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h5">
        Sign up
      </Typography>
      <form className={classes.form} noValidate>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              autoComplete="fname"
              name="firstName"
              variant="outlined"
              required
              fullWidth
              id="firstName"
              label="First Name"
              autoFocus
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="lastName"
              label="Last Name"
              name="lastName"
              autoComplete="lname"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
          </Grid>
          <Grid item xs={12}>
            <FormControlLabel
              control={<Checkbox value="allowExtraEmails" color="primary" />}
              label="You agree that when using this alpha project you won't be mad if data disappears or stuff breaks."
            />
          </Grid>
        </Grid>
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          className={classes.submit}
        >
          Sign Up
        </Button>
        <Grid container justify="flex-end">
          <Grid item>
            <Link to="/auth/login" component={RouterLink} variant="body2">
              Already have an account? Sign in
            </Link>
          </Grid>
        </Grid>
      </form>
    </>
  )
}
