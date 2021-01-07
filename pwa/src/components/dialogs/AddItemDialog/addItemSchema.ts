import { ItemTypesEnum } from "client/types"
import * as yup from "yup"

const combinedSchema = yup
  .object()
  .shape({
    name: yup
      .string()
      .required()
      .min(2, "Item name must be longer")
      .max(50, "Item name too long"),
    spaceId: yup.string().notRequired().nullable(),
    // Type selector, is stripped on cast in submission handler for now.
    type: yup.string().oneOf(["ITEM", "TOOL", "CONSUMABLE"]).default("ITEM")
    // type: createStrip(
    //   // TODO: use enum
    //   yup.mixed().oneOf(["ITEM", "TOOL", "CONSUMABLE"]).default("ITEM")
    // )
  })
  // @ts-ignore
  .when("type", (value: ItemTypesEnum, schema: any, bits) => {
    // value of type is never sent in cb, thanks
    const {
      value: { type }
    } = bits
    switch (type) {
      case ItemTypesEnum.Item:
        return schema.shape({})
      case ItemTypesEnum.Tool:
        return schema.shape({})
      case ItemTypesEnum.Consumable:
        return schema.shape({
          count: yup.number().default(1),
          warningEnabled: yup.boolean().default(true),
          warningCount: yup.number().default(1)
        })
      default:
        return schema.shape({})
    }
  })

export default combinedSchema
