import { gql } from "@apollo/client"
import { itemListContent } from "./fragments"

const layoutBit = gql`
  fragment LayoutBit on Layout {
    x
    y
    w
    h
  }
`

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
      ...SpaceGrid
      ... on SpaceInterface {
        parents @connection(key: "spaceBreadcrumbs") {
          ... on SpaceInterface {
            id
            name
          }
        }
        children {
          ...SpaceGrid
        }
        items(first: 100) {
          edges {
            cursor
            node {
              ...ItemListContent
            }
          }
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
