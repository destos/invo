import { gql } from "@apollo/client"

export const ENTITY_SEARCH = gql`
  query entitySearch($text: String!) {
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

export const ITEM_SEARCH = gql`
  query itemSearch(
    $search: String!
    $first: Int
    $last: Int
    $after: String
    $before: String
  ) {
    itemSearch(
      search: $search
      first: $first
      last: $last
      after: $after
      before: $before
    ) {
      pageInfo {
        hasNextPage
        endCursor
        count
      }
      edges {
        node {
          ...SearchItem
        }
      }
    }
  }
  fragment SearchItem on ItemInterface {
    ... on Node {
      id
    }
    name
    space {
      ... on SpaceInterface {
        id
        name
        parents @connection(key: "spaceBreadcrumbs") {
          ... on SpaceInterface {
            id
            name
          }
        }
      }
    }
  }
`
