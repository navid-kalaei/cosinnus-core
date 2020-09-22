import {
  Grid,
  Typography
} from "@material-ui/core"
import React, {useState} from "react"
import {connect as reduxConnect} from "react-redux"
import {RouteComponentProps} from "react-router-dom"
import {withRouter} from "react-router"
import {FormattedMessage} from "react-intl";
import Iframe from "react-iframe"

import {RootState} from "../../stores/rootReducer"
import {fetchEvents} from "../../stores/events/effects"
import {DispatchedReduxThunkActionCreator} from "../../utils/types"
import {EventSlot} from "../../stores/events/models"
import {findEventById} from "../../utils/events"
import {Content} from "../components/Content/style"
import {useStyles as iframeUseStyles} from "../components/Iframe/style"
import {Main} from "../components/Main/style"
import {Loading} from "../components/Loading"
import {ManageEventButtons} from "../components/ManageEventButtons"
import {Sidebar} from "../components/Sidebar"

interface StageEventProps {
  id: number
  events: EventSlot[]
  fetchEvents: DispatchedReduxThunkActionCreator<Promise<void>>
  url: string
}

function mapStateToProps(state: RootState) {
  console.log(state.room.props)
  return {
    events: state.events[state.room.props.id],
    url: state.room.props.url,
  }
}

const mapDispatchToProps = {
  fetchEvents
}

function StageEventConnector (props: StageEventProps & RouteComponentProps) {
  const { id, events, fetchEvents, url } = props
  const iframeClasses = iframeUseStyles()
  let event = null
  if (events) {
    event = findEventById(events, id)
  } else {
    fetchEvents()
  }
  return (
    <Main container>
      {event && (
        <Content>
          <Typography component="h1">{event.props.title}</Typography>
          {event.props.note && <Typography component="p">{event.props.note}</Typography>}
          <div className={iframeClasses.bbbIframe}>
            <Iframe
              url={event.props.url}
              width="100%"
              height="100%"
              allow="microphone *; camera *"
            />
          </div>
          <ManageEventButtons event={event} />
        </Content>
      ) || (
        <Content>
          <Loading />
        </Content>
      )}
      {url && (
        <Sidebar elements={(
          <Iframe
            url={url}
            width="100%"
            height="100%"
            className={iframeClasses.sidebarIframe}
            allow="microphone *; camera *"
          />
        )} />
      )}
    </Main>
  )
}

export const StageEvent = reduxConnect(mapStateToProps, mapDispatchToProps)(
  withRouter(StageEventConnector)
)
