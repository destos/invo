import { createStrip } from "utils/yup"
import * as yup from "yup"

const schema = yup.object().shape({
  firstName: yup.string().required(),
  lastName: yup.string().required(),
  email: yup.string().required().email(),
  password: yup.string().required(),
  accept: createStrip(
    yup.boolean().required().oneOf([true], "You must accept the terms")
  )
})

export default schema
