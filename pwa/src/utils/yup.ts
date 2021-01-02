import { FieldValues, Resolver, transformToNestObject } from "react-hook-form"
import * as Yup from "yup"

export const castId = Yup.mixed()
  .nullable()
  // Transform object to just the id
  .transform((value, original) => {
    if (!original) return null
    return original?.id
  })

export const castID = (cast: any) => (origSchema: any) =>
  // @ts-ignore
  Yup.lazy((value: any, config: any) => {
    if (config.context?.cast === cast) {
      return castId
    }
    return origSchema
  })

export const updateCastId = castID("update")
export const createCastId = castID("create")

export const stripOnCast = (cast: any) => (origSchema: any) =>
  // @ts-ignore
  Yup.lazy((value: any, config: any) => {
    if (config.context?.cast === cast) {
      return origSchema.strip(true)
    }
    return origSchema
  })

export const updateStrip = stripOnCast("update")
export const createStrip = stripOnCast("create")

// pulled from https://github.com/react-hook-form/resolvers/blob/master/src/yup.ts for customization of context
const parseErrorSchema = (
  error: Yup.ValidationError,
  validateAllFieldCriteria: boolean
) =>
  Array.isArray(error.inner) && error.inner.length
    ? error.inner.reduce(
        (previous: Record<string, any>, { path, message, type }) => {
          if (!path || !type) return { ...previous }

          const previousTypes = (path && previous[path].types) || {}
          const key = path || type

          return {
            ...previous,
            ...(key
              ? {
                  [key]: {
                    ...(previous[key] || {
                      message,
                      type
                    }),
                    ...(validateAllFieldCriteria
                      ? {
                          types: {
                            ...previousTypes,
                            [type]: previousTypes[type]
                              ? [...[].concat(previousTypes[type]), message]
                              : message
                          }
                        }
                      : {})
                  }
                }
              : {})
          }
        },
        {}
      )
    : {
        // @ts-ignore
        [error.path]: { message: error.message, type: error.type }
      }

export const yupResolver = <TFieldValues extends FieldValues>(
  // @ts-ignore
  schema: Yup.ObjectSchema | Yup.Lazy,
  // @ts-ignore
  options: Omit<Yup.ValidateOptions, "context"> = {
    abortEarly: false
  }
): Resolver<TFieldValues> => async (
  values,
  context,
  validateAllFieldCriteria = false
) => {
  try {
    // if (
    // // @ts-ignore
    //   (options as Yup.ValidateOptions).context &&
    //   process.env.NODE_ENV === "development"
    // ) {
    //   // eslint-disable-next-line no-console
    //   console.warn(
    //     "You should not used the yup options context. Please, use the 'useForm' context object instead"
    //   )
    // }
    return {
      values: (await schema.validate(values, {
        ...options,
        context: {
          ...context,
          ...options.context || {}
        }
      })) as any,
      errors: {}
    }
  } catch (e) {
    const parsedErrors = parseErrorSchema(e, validateAllFieldCriteria)
    return {
      values: {},
      errors: transformToNestObject(parsedErrors)
    }
  }
}
