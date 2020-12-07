import { gql } from "@apollo/client"
const itemFrag = gql`
  fragment AddItemFrag on ItemTypes {
    ... on ItemInterface {
      name
    }
    ... on Protocol {
      irn
      qr
    }
    ... on ConsumableInterface {
      count
      warningEnabled
      warningCount
      warning
    }
  }
`

export const ADD_ITEM = gql`
  mutation addItem($input: ItemInput!) {
    addItem(input: $input) {
      success
      errors {
        name
        values {
          error
          code
        }
      }
      object {
        ...AddItemFrag
      }
    }
  }
  ${itemFrag}
`

export const ADD_TOOL = gql`
  mutation addTool($input: ToolInput!) {
    addTool(input: $input) {
      success
      object {
        ...AddItemFrag
      }
    }
  }
  ${itemFrag}
`

export const ADD_CONSUMABLE = gql`
  mutation addConsumable($input: ConsumableInput!) {
    addConsumable(input: $input) {
      success
      object {
        ...AddItemFrag
      }
    }
  }
  ${itemFrag}
`
