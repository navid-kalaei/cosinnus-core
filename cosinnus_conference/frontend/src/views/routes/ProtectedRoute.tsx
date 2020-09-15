import * as React from "react"
import { Redirect, Route, RouteProps } from "react-router"
import {Loading} from "../components/Loading"

export interface ProtectedRouteProps extends RouteProps {
  isAuthenticated: boolean
  authPath?: string
  isAllowed?: boolean
  restrictedPath?: string
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = props => {
  if (!props.isAuthenticated) {
    const renderComponent = () => <Loading/>
    return <Route {...props} component={renderComponent} render={undefined} />
  } else {
    return <Route {...props} />
  }
}
