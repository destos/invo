import { gql } from "@apollo/client"
import { errorFragment } from "./fragments"

export const GET_USER_DETAILS = gql`
  query UserDetails {
    user: currentUser {
      id
      email
      firstName
      lastName
    }
  }
`

export const SIGN_UP = gql`
  mutation UserSignUp($input: CreateUserInput!) {
    createUser(input: $input) {
      success
      ...ErrorFragment
    }
  }
  ${errorFragment}
`
