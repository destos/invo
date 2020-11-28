import SituationCenterView from "./views/SituationCenter"
import RootSpaceView from "./views/RootSpace"
import Root from "./layout/Root"
import { RouteConfig } from "react-router-config"

const routes: Array<RouteConfig> = [
  {
    component: Root,
    routes: [
      {
        path: "/",
        exact: true,
        component: RootSpaceView
      },
      {
        path: "/select",
        component: SituationCenterView
      },
      // {
      //   path: "/space/:irn",
      //   component:
      // }
    ]
  }
]

export default routes
