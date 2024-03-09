import { gql } from "@apollo/client"
import { situationBit } from "./fragments"

export const SITU_QUERY = gql`
  query getActiveSituation {
    currentUser {
      sites {
        ...SituationSite
      }
    }
    currentSite {
      ...SituationSite
    }
    activeSituation {
      ...SituationBit
    }
  }
  ${situationBit}
  fragment SituationSite on Site {
    domain
    name
  }
`

export const SELECT_ENTITIES = gql`
  mutation addToActiveSituation($irns: [IRN!]!) {
    selectEntities(irns: $irns) {
      success
      object {
        ...SituationBit
      }
    }
  }
  ${situationBit}
`

export const UNSELECT_ENTITIES = gql`
  mutation removeFromActiveSituation($irns: [IRN!]!) {
    unselectEntities(irns: $irns) {
      success
      object {
        ...SituationBit
      }
    }
  }
  ${situationBit}
`

export const ABANDON_SITUATION = gql`
  mutation abandonActiveSituation($irns: [IRN!]!) {
    abandonSituation {
      ...SituationBit
    }
  }
  ${situationBit}
`
