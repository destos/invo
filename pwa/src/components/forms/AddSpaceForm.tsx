import Form from "@rjsf/material-ui"
import React from "react"
// import schema from "generated/jsonSchema.json"

interface AddSpaceFormProps {}
// schema.properties.Mutation.properties.addSpace
const test_schema = {
  title: "Name",
  type: "string"
}

const AddSpaceForm: React.FC<AddSpaceFormProps> = ({}) => {
  return (
    // @ts-ignore
    <Form schema={test_schema} />
  )
}

export default AddSpaceForm
