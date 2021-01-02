import { Grid } from "@material-ui/core"
import { SpaceTypesEnum } from "client/types"
import React from "react"
import { SelectElement, TextFieldElement } from "react-form-hook-mui"

interface Props {}

const BaseItemForm: React.FC<Props> = ({}) => {

  return (
    <>
      <Grid item xs={8}>
        <TextFieldElement
          autoFocus
          name="name"
          label="Name"
          variant="outlined"
          size="small"
          fullWidth
        />
      </Grid>
      <Grid item xs={4}>
        <SelectElement
          name="type"
          label="Type"
          variant="outlined"
          size="small"
          fullWidth
          options={[
            { id: SpaceTypesEnum.Space, title: "Regular Space" },
            { id: SpaceTypesEnum.Grid, title: "Grid Space" }
          ]}
        />
      </Grid>
      <Grid item xs={4}>
        <TextFieldElement
          name="dimensions.x"
          label="Width"
          variant="outlined"
          size="small"
          fullWidth
        />
      </Grid>
      <Grid item xs={4}>
        <TextFieldElement
          name="dimensions.y"
          label="Height"
          variant="outlined"
          size="small"
          fullWidth
        />
      </Grid>
      <Grid item xs={4}>
        <TextFieldElement
          name="dimensions.z"
          label="Depth"
          variant="outlined"
          size="small"
          fullWidth
        />
      </Grid>
    </>
  )
}

export default BaseItemForm
