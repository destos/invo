import { Grid } from "@material-ui/core"
import { ItemTypesEnum } from "client/types"
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
            { id: ItemTypesEnum.Item, title: "Item" },
            { id: ItemTypesEnum.Tool, title: "Tool" },
            { id: ItemTypesEnum.Consumable, title: "Consumable" }
          ]}
        />
      </Grid>
    </>
  )
}

export default BaseItemForm
