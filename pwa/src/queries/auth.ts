import { gql } from "@apollo/client"

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

