import { SpaceTypesEnum } from "client/types"
import * as yup from "yup"

const combinedSchema = yup
  .object()
  .shape({
    name: yup
      .string()
      .required()
      .min(2, "Item name must be longer")
      .max(50, "Item name too long"),
    // Type selector, is stripped on cast in submission handler for now.
    type: yup.string().oneOf([SpaceTypesEnum.Space, SpaceTypesEnum.Grid]).default(SpaceTypesEnum.Space),
    dimensions: yup.object().shape({
      x: yup.string(),
      y: yup.string(),
      z: yup.string()
    })
    // spaceId: yup.string().notRequired().nullable(),
  })
  // @ts-ignore
  .when("type", (value: SpaceTypesEnum, schema: any, bits) => {
    // value of type is never sent in cb, thanks
    const {
      value: { type }
    } = bits
    switch (type) {
      case SpaceTypesEnum.Space:
        return schema.shape({})
      case SpaceTypesEnum.Grid:
        return schema.shape({
          // TODO:
          gridSize: yup.object().shape({
            cols: yup.number().default(2),
            rows: yup.number().default(2)
          })
        })
      default:
        return schema.shape({})
    }
  })

export default combinedSchema
