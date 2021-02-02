import {
  Button,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogProps,
  DialogTitle,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Theme,
  Typography,
  ListItemSecondaryAction,
  Tooltip
} from "@material-ui/core"
import CloseIcon from "@material-ui/icons/Close"
import InfoIcon from "@material-ui/icons/Info"
import { makeStyles } from "@material-ui/styles"
import { Scalars, SubscribedEventTypeFragment } from "client/types"
import React from "react"

// Dialog
const useStyles = makeStyles((theme: Theme) => ({
  root: {},
  closeButton: {
    marginRight: "auto"
  },
  listSection: {
    // background: theme.palette.grey[300]
    padding: 0
  }
}))

// The idea for this component is it is popped up when making many selections so a batch of irns
// can be scanned and then input into some part of the process.
// They can be removed from the selection before sent to the backend as official selections.
// May act as an alternative interface for when you want to really do batch scans/selections.

interface SubscriptionsDialogProps extends DialogProps {
  title: string
  // eventTypes: Array<SubscribedEventTypeFragment>
  // defaultIds?: Array<Scalars["ID"]>
  onSubscribe: (id: Scalars["ID"]) => void
  onUnsubscribe: (id: Scalars["ID"]) => void
}

const SubscriptionDialog: React.FunctionComponent<SubscriptionsDialogProps> = ({
  title,
  // eventTypes,
  // defaultIds = [],
  onSubscribe,
  onUnsubscribe,
  ...dialogProps
}) => {
  const { onClose } = dialogProps
  const classes = useStyles()

  const closeDialog = (e: any, reason?: any) => {
    // Clear state
    onClose && onClose(e, reason)
  }

  const handleToggleSubscription = (et: SubscribedEventTypeFragment) => {
    if (et.isObjectSubscribed) {
      onUnsubscribe(et.id)
    } else {
      onSubscribe(et.id)
    }
  }

  // TODO: show the defaults that would be toggled and provide buttons that
  // turn those on and off? a toggle button at the top?
  return (
    <Dialog {...dialogProps}>
      <DialogTitle disableTypography>
        <Typography variant="h4">{title}</Typography>
      </DialogTitle>
      <DialogContent className={classes.listSection} dividers>
        <List>
          {eventTypes.map(et => (
            <ListItem
              key={et.id}
              role={undefined}
              dense
              button={true}
              // @ts-ignore
              onClick={() => handleToggleSubscription(et)}
            >
              <ListItemIcon>
                <Checkbox
                  edge="start"
                  checked={et.isObjectSubscribed}
                  tabIndex={-1}
                  disableRipple
                  inputProps={{ "aria-labelledby": `label-${et.id}` }}
                />
              </ListItemIcon>
              <ListItemText id={`label-${et.id}`} primary={et.label} />
              {defaultIds.indexOf(et.id) >= 0 ? (
                <ListItemSecondaryAction>
                  <Tooltip title="Default event subscription" arrow>
                    <InfoIcon fontSize="small" />
                  </Tooltip>
                </ListItemSecondaryAction>
              ) : null}
            </ListItem>
          ))}
        </List>
      </DialogContent>
      <DialogActions>
        <Button
          className={classes.closeButton}
          onClick={() => closeDialog(undefined, undefined)}
          variant="outlined"
          startIcon={<CloseIcon />}
        >
          Close
        </Button>
        <Button variant="contained" color="primary">
          Select
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default SubscriptionDialog
