import React, {useState} from "react"
import {Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Link} from "@material-ui/core"
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome"
import {faPen, faPlus, faTrashAlt} from "@fortawesome/free-solid-svg-icons"
import {FormattedMessage} from "react-intl"
import axios from "axios"

import {Event} from "../../../stores/events/models"
import {useStyles} from "./style"
import axios from "axios"

interface ManageEventButtonsProps {
  event: Event
}

export function ManageEventButtons(props: ManageEventButtonsProps) {
  const {event} = props
  const classes = useStyles()
  const [deleteOpen, setDeleteOpen] = useState(false);
  if (!event.props.managementUrls) {
    return null
  }
  function deleteEvent() {
    axios.post(event.props.managementUrls.deleteEvent, {},{
      headers: {
        'X-CSRFTOKEN': Cookies.get('csrftoken'),
      },
      withCredentials: true
    }).then(res => {
      window.location.href = "../"
    })
  }
  return (
    <div className={classes.buttons}>
      {event.props.managementUrls.updateEvent && (
        <Button
          variant="contained"
          disableElevation
          href="#"
          onClick={() => window.location.href = event.props.managementUrls.updateEvent}
        >
          <FontAwesomeIcon icon={faPen} />&nbsp;
          <FormattedMessage id="Edit event" defaultMessage="Edit event" />
        </Button>
      )}
      {event.props.managementUrls.deleteEvent && (
        <span>
          <Button
            variant="contained"
            disableElevation
            href="#"
            onClick={() => setDeleteOpen(true)}
          >
            <FontAwesomeIcon icon={faTrashAlt} />&nbsp;
            <FormattedMessage id="Delete event" defaultMessage="Delete event" />
          </Button>
          <Dialog
            open={deleteOpen}
            keepMounted
            onClose={() => setDeleteOpen(false)}
          >
            <DialogTitle><FormattedMessage id="Delete Event" defaultMessage="Delete Event" /></DialogTitle>
            <DialogContent>
              <DialogContentText>
                <FormattedMessage
                  id="Are you sure you want to delete this event?"
                  defaultMessage="Are you sure you want to delete this event?"
                />
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setDeleteOpen(false)} color="primary">
                <FormattedMessage id="No" defaultMessage="No" />
              </Button>
              <Button onClick={deleteEvent} color="primary">
                <FormattedMessage id="Yes" defaultMessage="Yes" />
              </Button>
            </DialogActions>
          </Dialog>
        </span>
      )}
    </div>
  )
}
