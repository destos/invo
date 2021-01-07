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
  AddGridSpaceMutation,
  AddGridSpaceMutationVariables,
  AddSpaceMutation,
  AddSpaceMutationVariables,
  GridSpaceInput,
  Scalars,
  SpaceInput,
  SpaceTypesEnum
} from "client/types"
import { ADD_GRID_SPACE, ADD_SPACE } from "queries/spaces"
import React from "react"
import { FormContainer } from "react-form-hook-mui"
import { useForm } from "react-hook-form"
import { yupResolver } from "utils/yup"
import schema from "./addSpaceSchema"
import BaseSpaceNodeForm from "./forms/BaseSpaceNodeForm"
import GridSpaceNodeForm from "./forms/GridSpaceNodeForm"

export type FormValues = (SpaceInput | GridSpaceInput) & {
  // The type of item being created, maybe an enum eventually
  type: SpaceTypesEnum
}

export interface AddSpaceDialogProps extends DialogProps {
  closeOnAdd?: boolean
  // Space to create this item inside
  parentId?: Scalars["ID"]
  defaultValues?: FormValues
  // TODO: callback style for success/cancel?
}

const AddSpaceDialog: React.FunctionComponent<AddSpaceDialogProps> = ({
  closeOnAdd = true,
  parentId = null,
  defaultValues = {
    name: "",
    type: SpaceTypesEnum.Space,
    dimensions: {
      x: "1 m",
      y: "1 m",
      z: "30 cm"
    },
    gridSize: {
      cols: 2,
      rows: 2
    }
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
  const { watch, reset, setError } = formContext
  const type = watch("type")

  const [addSpace] = useMutation<AddSpaceMutation, AddSpaceMutationVariables>(
    ADD_SPACE
  )
  const [addGridSpace] = useMutation<
    AddGridSpaceMutation,
    AddGridSpaceMutationVariables
  >(ADD_GRID_SPACE)

  const doSubmit = async (data: any) => {
    const mutation = {
      [SpaceTypesEnum.Space]: addSpace,
      [SpaceTypesEnum.Grid]: addGridSpace
    }[type]

    // Because we can't change the context on submit for some goddamn reason.
    delete data["type"]

    const {
      // @ts-ignore
      data: { result }
    } = await mutation({
      variables: {
        input: {
          parent: parentId,
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
        // handleSubmit={handleSubmit}
        onSuccess={doSubmit}
      >
        <DialogTitle>Add space</DialogTitle>
        <DialogContent style={{ marginTop: -8, marginBottom: -8 }}>
          <Grid container spacing={2}>
            <BaseSpaceNodeForm />
            {type === SpaceTypesEnum.Grid ? <GridSpaceNodeForm /> : null}
          </Grid>
          {/* {JSON.stringify(formContext)} */}
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

export default AddSpaceDialog
