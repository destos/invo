import { gql } from "@apollo/client"
import { errorFragment, itemListContent } from "./fragments"

const layoutBit = gql`
  fragment LayoutBit on Layout {
    x
    y
    w
    h
  }
`

// Data needed to display space information in a grid item
const spaceGrid = gql`
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
  ${spaceGrid}
`

export const GET_NAVIGATION_SPACE = gql`
  query getNavigationSpace($id: ID!) {
    space(id: $id) {
      ... on Protocol {
        irn
      }
      ... on SpaceInterface {
        id
        name
        volume
        dimensions {
          x
          y
          z
        }
        itemCount
        parents @connection(key: "spaceBreadcrumbs") {
          ... on SpaceInterface {
            id
            name
          }
        }
        children {
          ...SpaceGrid
        }
        isLeaf
        items(first: 100) {
          edges {
            cursor
            node {
              ...ItemListContent
            }
          }
        }
        gridConfig {
          cols
          rowBasis
        }
      }
      ... on GridSpaceNode {
        gridSize {
          rows
          cols
        }
      }
    }
  }
  ${itemListContent}
  ${spaceGrid}
`

export const UPDATE_SPACE_LAYOUT = gql`
  mutation updateSpaceLayout($id: ID!, $layout: LayoutInput!) {
    space: updateSpaceLayout(id: $id, layout: $layout) {
      ...SpaceGrid
    }
  }
  ${spaceGrid}
`

const spaceFrag = gql`
  fragment AddSpaceFrag on SpaceTypes {
    ... on SpaceInterface {
      name
    }
    ... on Protocol {
      irn
      qr
    }
  }
`

export const ADD_SPACE = gql`
  mutation addSpace($input: SpaceInput!) {
    result: addSpace(input: $input) {
      success
      ...ErrorFragment
      object {
        ...AddSpaceFrag
      }
    }
  }
  ${errorFragment}
  ${spaceFrag}
`

export const ADD_GRID_SPACE = gql`
  mutation addGridSpace($input: GridSpaceInput!) {
    result: addGridSpace(input: $input) {
      success
      ...ErrorFragment
      object {
        ...AddSpaceFrag
      }
    }
  }
  ${errorFragment}
  ${spaceFrag}
`
