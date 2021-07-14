import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogProps,
  DialogTitle,
  Theme
} from "@material-ui/core"
import CloseIcon from "@material-ui/icons/Close"
import { makeStyles } from "@material-ui/styles"
import { getApplicationKeyMap } from "react-hotkeys"
import React from "react"

// Dialog
const useStyles = makeStyles((theme: Theme) => ({
  root: {}
}))

interface ShortcutDialogProps extends DialogProps {}

const ShortcutDialog: React.FunctionComponent<ShortcutDialogProps> = ({
  ...dialogProps
}) => {
  const { onClose } = dialogProps
  // const keyMap = getApplicationKeyMap()

  const closeDialog = (e: any, reason?: any) => {
    // TODO: Clear state?
    onClose && onClose(e, reason)
  }

  // const bits = Object.keys(keyMap).reduce((memo, actionName) => {
  //   const { sequences, name } = keyMap[actionName]

  //   // @ts-ignore
  //   memo.push(
  //     <tr key={name || actionName}>
  //       <td>{name}</td>
  //       <td>
  //         {sequences.map(({ sequence }) => (
  //           <span key={sequence as string}>{sequence}</span>
  //         ))}
  //       </td>
  //     </tr>
  //   )

  //   return memo
  // })
  return (
    <Dialog {...dialogProps}>
      <DialogTitle>Shortcuts</DialogTitle>
      <DialogContentText>
        Theses are global shortcuts that are used throughout the site
      </DialogContentText>
      <DialogContent></DialogContent>
      <DialogActions>
        <Button
          onClick={() => closeDialog(undefined, undefined)}
          variant="outlined"
          startIcon={<CloseIcon />}
        >
          Close
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default ShortcutDialog
