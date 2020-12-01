import { gql } from "@apollo/client"

const fragments = gql`
  fragment Times on TimeStamped {
    created
    modified
  }
  fragment SituationBit on Situation {
    id
    ...Times
    state
    items {
      ...ItemBit
    }
    spaces {
      ...SpaceBit
    }
  }
  fragment ItemBit on ItemInterface {
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
  fragment SpaceBit on SpaceInterface {
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
`
export default fragments
