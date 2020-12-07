import SituationCenterView from "./views/SituationCenter"
import RootSpaceView from "./views/RootSpace"
import SpaceView from "./views/Space"
import Root from "./layout/Root"
import { RouteConfig } from "react-router-config"
import { generatePath } from "react-router-dom"
import { Scalars } from "./client/types"

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
      {
        path: "/space/:id",
        component: SpaceView
      }
      // TODO: tab route for view type selection and tab to drive tab state?
    ]
  }
  // TODO:
  // label Print page, how do labels werk?
  // Do labels get printed from a django template/page?
]

export const spaceDetailUrl = (id: Scalars["ID"]) => generatePath("/space/:id", {id})

export default routes
