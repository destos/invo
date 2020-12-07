import { useMutation } from "@apollo/client"
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogProps,
  DialogTitle,
  TextField,
  Theme
} from "@material-ui/core"
import CloseIcon from "@material-ui/icons/Close"
import { makeStyles } from "@material-ui/styles"
import { Scalars } from "client/types"
import { ADD_ITEM } from "queries/items"
import React, { useState } from "react"

// Dialog
const useStyles = makeStyles((theme: Theme) => ({
  root: {}
}))

interface AddItemDialogProps extends DialogProps {
  // Space to create this item inside
  spaceId?: Scalars["ID"]
  // The type of item being created, maybe an enum eventually
  type?: "item" | "tool" | "consumable"
}

// const ItemForm = ({state, update}) => {}

const AddItemDialog: React.FunctionComponent<AddItemDialogProps> = ({
  spaceId = null,
  type = null,
  ...dialogProps
}) => {
  const { onClose } = dialogProps

  // type: type ?? "item",
  const [formState, setFormState] = useState({
    name: ""
  })

  const handleChange = (
    event: React.ChangeEvent<{ name?: string; value: unknown }>
  ) => {
    const name = event.target.name as keyof typeof formState
    setFormState({
      ...formState,
      // @ts-ignore
      [name]: event.target.value
    })
  }

  const handleSubmit = (e: any) => {
    e.preventDefault()
    addItem({
      variables: {
        input: {
          spaceId,
          ...formState
        }
      }
    })
  }

  const closeDialog = (e: any, reason?: any) => {
    // TODO: Clear state?
    onClose && onClose(e, reason)
  }

  const [addItem, { data }] = useMutation(ADD_ITEM)

  return (
    <Dialog {...dialogProps}>
      <form onSubmit={handleSubmit}>
        <DialogTitle>Add item</DialogTitle>
        {/* <DialogContent>
          <DialogContentText>Enter item details</DialogContentText>
          <Select
            native
            // variant="outlined"
            value={formState.type}
            onChange={handleChange}
            name="type"
            inputProps={{}}
          >
            <option value={"item"}>Item</option>
            <option value={"tool"}>Tool</option>
            <option value={"consumable"}>Consumable</option>
          </Select>
        </DialogContent>
        <Divider /> */}
        <DialogContent>
          <TextField
            value={formState.name}
            name="name"
            label="Name"
            onChange={handleChange}
          />
        </DialogContent>
        <DialogActions>
          <Button type="submit" color="primary" variant="contained">
            Create
          </Button>
          <Button
            onClick={() => closeDialog(undefined, undefined)}
            variant="outlined"
            startIcon={<CloseIcon />}
          >
            Close
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  )
}

export default AddItemDialog
