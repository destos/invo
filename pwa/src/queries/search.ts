import { gql } from "@apollo/client"

export const ENTITY_SEARCH = gql`
  query entitySearch($text: String!){
    entitySearch(search: { text: $text }) {
      irn
      score
      object {
        ...SearchObject
      }
    }
  }
  fragment SearchObject on Protocol {
    ... on Protocol {
      irn
    }
    ... on ItemInterface {
      name
    }
    ... on SpaceInterface {
      name
    }
  }
`
