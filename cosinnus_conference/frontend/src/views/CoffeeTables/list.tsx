import {
  Grid,
  Typography
} from "@material-ui/core"
import React, {useEffect, useState} from "react"
import {connect as reduxConnect} from "react-redux"
import {RouteComponentProps} from "react-router-dom"
import {withRouter} from "react-router"
import {FormattedMessage} from "react-intl";

import {RootState} from "../../stores/rootReducer"
import {DispatchedReduxThunkActionCreator} from "../../utils/types"
import {Content} from "../components/Content/style"
import {Sidebar} from "../components/Sidebar"
import {useStyles} from "./style"
import {CoffeeTable} from "../components/CoffeeTable"
import {fetchEvents} from "../../stores/events/effects"
import {ManageRoomButtons} from "../components/ManageRoomButtons"
import {Room} from "../../stores/room/models"
import {Loading} from "../components/Loading"
import {EventRoomState} from "../../stores/events/reducer"

interface CoffeeTablesProps {
  events: EventRoomState
  fetchEvents: DispatchedReduxThunkActionCreator<Promise<void>>
  room: Room
}

function mapStateToProps(state: RootState, _ownProps: CoffeeTablesProps) {
  return {
    events: state.events[state.room.props.id],
    room: state.room,
  }
}

const mapDispatchToProps = {
  fetchEvents: fetchEvents
}

function CoffeeTablesConnector (props: CoffeeTablesProps & RouteComponentProps) {
  const { events, fetchEvents, room } = props
  // Rerender every minute
  const [time, setTime] = useState(new Date())
  useEffect(() => { setInterval(() => setTime(new Date()), 60000) })

  if (!events) {
    fetchEvents()
  }
  const classes = useStyles()
  return (
    <Grid container>
      <Content>
        <div className={classes.section}>
          <Typography component="h1"><FormattedMessage id="Happening now" /></Typography>
          {room.props.descriptionHtml && (
            <div className="description" dangerouslySetInnerHTML={{__html: room.props.descriptionHtml}} />
          )}
          {(events && events.events && events.events.length > 0 && (
            <Grid container spacing={4}>
              {events.events.map((event, index) => (
                <Grid item key={index} sm={6} className="now">
                  <CoffeeTable event={event} />
                </Grid>
              ))}
            </Grid>
          ))
          || (events && events.loading && <Loading />)
          || <Typography><FormattedMessage id="No coffee tables." /></Typography>
        }
        </div>
        <ManageRoomButtons />
      </Content>
      {room.props.url && <Sidebar url={room.props.url} />}
    </Grid>
  )
}

export const CoffeeTables = reduxConnect(mapStateToProps, mapDispatchToProps)(
  withRouter(CoffeeTablesConnector)
)
