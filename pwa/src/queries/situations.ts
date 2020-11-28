import { gql } from "@apollo/client"
import fragments from "./fragments"

export const SITU_QUERY = gql`
  query getActiveSituation {
    currentUser {
      id
      username
      firstName
      lastName
    }
    activeSituation {
      ...SituationBit
    }
  }
  ${fragments}
`

export const SELECT_ENTITIES = gql`
  mutation addToActiveSituation($irns: [IRN!]!){
    selectEntities(irns: $irns) {
      success
      object {
        ...SituationBit
      }
    }
  }
  ${fragments}
`

export const UNSELECT_ENTITIES = gql`
  mutation removeFromActiveSituation($irns: [IRN!]!){
    unselectEntities(irns: $irns) {
      success
      object {
        ...SituationBit
      }
    }
  }
  ${fragments}
`
