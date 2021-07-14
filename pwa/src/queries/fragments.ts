import { gql } from "@apollo/client"

export const timeStamped = gql`
  fragment Times on TimeStamped {
    created
    modified
  }
`

export const errorFragment = gql`
  fragment ErrorFragment on Payload {
    errors {
      name
      values {
        code
        error
      }
    }
  }
`

// Used when an item is used inside a ItemListItem component
export const itemListContent = gql`
  fragment ItemListContent on ItemInterface {
    id
    ...Times
    name
    data
    ... on Protocol {
      irn
      qr
    }
    space {
      ... on SpaceInterface {
        name
      }
    }
    spaceParents {
      ... on SpaceInterface {
        name
      }
    }
  }
  ${timeStamped}
`
export const spaceListContent = gql`
  fragment SpaceListContent on SpaceInterface {
    id
    ...Times
    name
    data
    itemCount
    ... on Protocol {
      irn
      qr
    }
  }
  ${timeStamped}
`

export const situationBit = gql`
  fragment SituationBit on Situation {
    id
    ...Times
    state
    items {
      ...ItemListContent
    }
    spaces {
      ...SpaceListContent
    }
  }
  ${spaceListContent}
  ${timeStamped}
  ${itemListContent}
`
