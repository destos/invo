import { FieldError } from "client/types"
import join from "lodash/join"
import map from "lodash/map"

export function setErrors(errors: Array<FieldError>, setError: any) {
  errors.forEach(fieldError => {
    const errorJoined = join(map(fieldError.values, "error"), ", ")
    setError(fieldError.name, errorJoined)
  })
}

// export function parseError(errorType:)
