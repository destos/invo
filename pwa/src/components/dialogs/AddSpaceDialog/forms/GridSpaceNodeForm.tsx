import { Grid } from "@material-ui/core"
import React from "react"
import { TextFieldElement } from "react-form-hook-mui"

interface Props {}

const ConsumableForm: React.FC<Props> = ({}) => {

  return (
    <>
      <Grid item xs={6}>
        <TextFieldElement
          name="gridSize.cols"
          type="number"
          label="Columns"
          variant="outlined"
          size="small"
          fullWidth
        />
      </Grid>
      <Grid item xs={6}>
        <TextFieldElement
          name="gridSize.rows"
          type="number"
          label="Rows"
          variant="outlined"
          size="small"
          fullWidth
        />
      </Grid>
    </>
  )
}

export default ConsumableForm
