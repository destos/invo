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
    result: addItem(input: $input) {
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
    result: addTool(input: $input) {
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
    result: addConsumable(input: $input) {
      success
      object {
        ...AddItemFrag
      }
    }
  }
  ${itemFrag}
`
