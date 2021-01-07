import { Grid } from "@material-ui/core"
import React from "react"
import { CheckboxElement, TextFieldElement } from "react-form-hook-mui"
import { useFormContext } from "react-hook-form"
import { FormValues } from "../AddItemDialog"

interface Props {}

const ConsumableForm: React.FC<Props> = ({}) => {
  const { watch } = useFormContext<FormValues>()
  // @ts-ignore
  const { warningEnabled } = watch()
  return (
    <>
      <Grid item xs={12}>
        <TextFieldElement
          name="count"
          type="number"
          label="Current count or value"
          variant="outlined"
          size="small"
          fullWidth
        />
      </Grid>
      {/* TODO: units */}
      <Grid item xs={6}>
        <CheckboxElement
          name="warningEnabled"
          label="Low-count warning"
          size="small"
        />
      </Grid>
      <Grid item xs={6}>
        <TextFieldElement
          name="warningCount"
          type="number"
          label="Warning count or value"
          variant="outlined"
          size="small"
          disabled={!warningEnabled}
          fullWidth
        />
      </Grid>
    </>
  )
}

export default ConsumableForm
