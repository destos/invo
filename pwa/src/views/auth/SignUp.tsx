import { useMutation } from "@apollo/client"
import Avatar from "@material-ui/core/Avatar"
import Button from "@material-ui/core/Button"
import FormControlLabel from "@material-ui/core/FormControlLabel"
import Grid from "@material-ui/core/Grid"
import Link from "@material-ui/core/Link"
import { makeStyles } from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"
import LockOutlinedIcon from "@material-ui/icons/LockOutlined"
import { UserSignUpMutation, UserSignUpMutationVariables } from "client/types"
import { SIGN_UP } from "queries/auth"
import React from "react"
import {
  CheckboxElement,
  FormContainer,
  TextFieldElement
} from "react-form-hook-mui"
import { useForm } from "react-hook-form"
import { Link as RouterLink, useHistory } from "react-router-dom"
import { setErrors } from "utils/form"
import { yupResolver } from "utils/yup"
import schema from "./signupSchema"

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

export type FormValues = {
  firstName: string
  lastName: string
  email: string
  password: string
  accept: boolean
}

const defaultValues = {
  firstName: "",
  lastName: "",
  email: "",
  password: "",
  accept: false
}

export default function SignUp() {
  const classes = useStyles()
  const history = useHistory()

  const formContext = useForm<FormValues>({
    context: {
      cast: "validate"
    },
    defaultValues,
    resolver: yupResolver(schema, { strict: false })
  })
  const { reset, setError } = formContext

  const [signIn] = useMutation<UserSignUpMutation, UserSignUpMutationVariables>(
    SIGN_UP
  )

  const doSubmit = async (data: FormValues) => {
    const input = schema.cast(data, { context: { cast: "create" } })

    const {
      data: {
        // @ts-ignore
        createUser: { success, errors }
      }
    } = await signIn({
      variables: {
        // @ts-ignore
        input
      }
    })

    if (success) {
      reset(defaultValues)
      // Redirect
      // @ts-ignore
      history.replace("/auth/login")
    } else {
      setErrors(errors, setError)
    }
  }

  return (
    <>
      <Avatar className={classes.avatar}>
        <LockOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h5">
        Sign up
      </Typography>
      <FormContainer
        FormProps={{
          className: classes.form,
          autoComplete: "on"
        }}
        formContext={formContext}
        onSuccess={doSubmit}
      >
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextFieldElement
              autoComplete="fname"
              name="firstName"
              variant="outlined"
              fullWidth
              id="firstName"
              label="First Name"
              autoFocus
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextFieldElement
              variant="outlined"
              fullWidth
              id="lastName"
              label="Last Name"
              name="lastName"
              autoComplete="lname"
            />
          </Grid>
          <Grid item xs={12}>
            <TextFieldElement
              variant="outlined"
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
            />
          </Grid>
          <Grid item xs={12}>
            <TextFieldElement
              variant="outlined"
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
          </Grid>
          <Grid item xs={12}>
            <CheckboxElement
              name="accept"
              color="primary"
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
              Already have an account? Sign in instead
            </Link>
          </Grid>
        </Grid>
      </FormContainer>
    </>
  )
}
