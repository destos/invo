import { useMutation } from "@apollo/client"
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogProps,
  DialogTitle,
  Grid
} from "@material-ui/core"
import CloseIcon from "@material-ui/icons/Close"
import {
  AddConsumableMutation,
  AddConsumableMutationVariables,
  AddItemMutation,
  AddItemMutationVariables,
  AddToolMutation,
  AddToolMutationVariables,
  ConsumableInput,
  ItemInput,
  ItemTypesEnum,
  Scalars,
  ToolInput
} from "client/types"
import { ADD_CONSUMABLE, ADD_ITEM, ADD_TOOL } from "queries/items"
import React from "react"
import { FormContainer } from "react-form-hook-mui"
import { useForm } from "react-hook-form"
import { yupResolver } from "utils/yup"
import schema from "./addItemSchema"
import BaseItemForm from "./forms/BaseItemForm"
import ConsumableForm from "./forms/ConsumableForm"

export type FormValues = (ItemInput | ToolInput | ConsumableInput) & {
  // The type of item being created, maybe an enum eventually
  type: ItemTypesEnum
}

export interface AddItemDialogProps extends DialogProps {
  closeOnAdd?: boolean
  // Space to create this item inside
  spaceId?: Scalars["ID"]
  defaultValues?: FormValues
  // TODO: callback style for success/cancel?
}

const AddItemDialog: React.FunctionComponent<AddItemDialogProps> = ({
  closeOnAdd = true,
  spaceId = null,
  defaultValues = {
    name: "",
    type: ItemTypesEnum.Item,
    count: 1,
    warningEnabled: false,
    warningCount: 1
  },
  ...dialogProps
}) => {
  const { onClose } = dialogProps

  const formContext = useForm<FormValues>({
    context: {
      cast: "validate"
    },
    defaultValues,
    resolver: yupResolver(schema, { strict: false })
  })
  const { watch, reset } = formContext
  const type = watch("type")

  const [addItem] = useMutation<AddItemMutation, AddItemMutationVariables>(
    ADD_ITEM
  )
  const [addTool] = useMutation<AddToolMutation, AddToolMutationVariables>(
    ADD_TOOL
  )
  const [addConsumable] = useMutation<
    AddConsumableMutation,
    AddConsumableMutationVariables
  >(ADD_CONSUMABLE)

  const doSubmit = async (data: any) => {
    const mutation = {
      [ItemTypesEnum.Item]: addItem,
      [ItemTypesEnum.Tool]: addTool,
      [ItemTypesEnum.Consumable]: addConsumable
    }[type]

    // Because we can't change the context on submit for some goddamn reason.
    delete data["type"]

    const {
      // @ts-ignore
      data: { result }
    } = await mutation({
      variables: {
        input: {
          spaceId,
          ...data
        }
      }
    })
    if (result.success) {
      reset(defaultValues)
      if (closeOnAdd) closeDialog(null)
    } else {
      // add errors
      // setErrors(data.errors, setError)
    }
  }

  const closeDialog = (e: any, reason?: any) => {
    onClose && onClose(e, reason)
  }

  return (
    <Dialog {...dialogProps}>
      <FormContainer
        formContext={formContext}
        FormProps={{
          "aria-autocomplete": "none",
          autoComplete: "new-password"
        }}
        onSuccess={doSubmit}
      >
        <DialogTitle>Add item</DialogTitle>
        <DialogContent style={{ marginTop: -8, marginBottom: -8 }}>
          <Grid container spacing={2}>
            <BaseItemForm />
            {type === ItemTypesEnum.Consumable ? <ConsumableForm /> : null}
          </Grid>
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
      </FormContainer>
    </Dialog>
  )
}

export default AddItemDialog
