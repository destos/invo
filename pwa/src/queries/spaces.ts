import { gql } from "@apollo/client"

const layoutBit = gql`
  fragment LayoutBit on Layout {
    x
    y
    w
    h
  }
`

const spaceBit = gql`
  fragment SpaceGrid on SpaceTypes {
    ... on Protocol {
      irn
    }
    ... on SpaceInterface {
      id
      name
      itemCount
      layout {
        ...LayoutBit
      }
    }
  }
  ${layoutBit}
`

export const GET_ROOT_SPACES = gql`
  query getRootSpaces {
    spaces: getSpaces(filter: { level: 0 }) {
      ...SpaceGrid
    }
  }
  ${spaceBit}
`

export const UPDATE_SPACE_LAYOUT = gql`
  mutation updateSpaceLayout($id: ID!, $layout: LayoutInput!) {
    space: updateSpaceLayout(id: $id, layout: $layout) {
      ...SpaceGrid
    }
  }
  ${spaceBit}
`
