import Avatar from "@material-ui/core/Avatar"
import Button from "@material-ui/core/Button"
import Checkbox from "@material-ui/core/Checkbox"
import FormControlLabel from "@material-ui/core/FormControlLabel"
import Grid from "@material-ui/core/Grid"
import Link from "@material-ui/core/Link"
import { makeStyles } from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"
import LockOutlinedIcon from "@material-ui/icons/LockOutlined"
import { useAuth } from "client/auth"
import React from "react"
import { FormContainer, TextFieldElement } from "react-form-hook-mui"
import { useForm } from "react-hook-form"
import { Link as RouterLink } from "react-router-dom"
import { yupResolver } from "utils/yup"
import schema from "./loginSchema"

const useStyles = makeStyles((theme) => ({
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main
  },
  form: {
    marginTop: theme.spacing(1)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  }
}))

export type FormValues = {
  email: string
  password: string
}

const defaultValues = {
  email: "",
  password: ""
}

export default function SignIn() {
  const classes = useStyles()
  const auth = useAuth()
  const formContext = useForm<FormValues>({
    context: {
      cast: "validate"
    },
    defaultValues,
    resolver: yupResolver(schema, { strict: false })
  })
  const { reset } = formContext

  const doSubmit = async (data: FormValues) => {
    const result = await fetch(`${process.env.REACT_APP_API_GATEWAY}token/`, {
      body: JSON.stringify(data),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      method: "post"
    })

    if (result.status === 200) {
      // @ts-ignore
      const tokens = await result.json()
      auth.setTokens(tokens)
      reset(defaultValues)
    } else {
      formContext.setError("password", {
        type: "validate",
        shouldFocus: true,
        message: "Password is incorrect"
      })
    }
  }

  return (
    <>
      <Avatar className={classes.avatar}>
        <LockOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h5">
        Sign in
      </Typography>
      <FormContainer
        FormProps={{
          className: classes.form,
          autoComplete: "new-password"
        }}
        formContext={formContext}
        onSuccess={doSubmit}
      >
        <TextFieldElement
          variant="outlined"
          margin="normal"
          fullWidth
          label="Email Address"
          name="email"
          autoComplete="email"
          autoFocus
        />
        <TextFieldElement
          variant="outlined"
          margin="normal"
          fullWidth
          name="password"
          label="Password"
          type="password"
          autoComplete="current-password"
        />
        <FormControlLabel
          control={<Checkbox value="remember" color="primary" />}
          label="Remember me"
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          className={classes.submit}
        >
          Sign In
        </Button>
        <Grid container>
          <Grid item xs>
            <Link to="/auth/forgot" component={RouterLink} variant="body2">
              Forgot password?
            </Link>
          </Grid>
          <Grid item>
            <Link to="/auth/signup" component={RouterLink} variant="body2">
              {"Don't have an account? Sign Up"}
            </Link>
          </Grid>
        </Grid>
      </FormContainer>
    </>
  )
}
