import { AuthProvider } from "client/auth"
import { ComponentType, lazy } from "react"
import { RouteConfig } from "react-router-config"
import { generatePath, Redirect } from "react-router-dom"
import { Scalars } from "./client/types"
import Root from "./layout/Root"
import UnAuthedRoot from "./layout/UnAuthedRoot"
import ExamplesView from "./views/Examples"
import LoginView from "./views/auth/Login"
import SignUpView from "./views/auth/SignUp"
import AllSpaces from "views/AllSpaces"

const RootSpaceView = lazy(
  () => import(/* webpackChunkName: "spaces" */ "./views/RootSpace")
)
const SituationCenterView = lazy(
  () => import(/* webpackChunkName: "situations" */ "./views/SituationCenter")
)
const SpaceView = lazy(
  () => import(/* webpackChunkName: "spaces" */ "./views/Space")
)

const routes: Array<RouteConfig> = [
  {
    component: UnAuthedRoot,
    path: "/auth/*",
    exact: false,
    routes: [
      // {
      //   path: "/auth",
      //   exact: true,
      //   render: () => <Redirect to="/auth/login/" />
      // },
      {
        path: "/auth/login/",
        exact: true,
        component: LoginView
      },
      {
        path: "/auth/signup/",
        exact: true,
        component: SignUpView
      },
      // TODO: make forgot view/backend functionality
      {
        path: "/auth/forgot/",
        exact: true,
        component: SignUpView
      }
    ]
  },
  {
    component: Root,
    path: "*",
    routes: [
      {
        path: "/",
        exact: true,
        component: RootSpaceView
        // TODO: SpaceView props
      },
      // {
      //   path: "/search",
      //   exact: true,
      //   component: ItemSearchView
      // }
      {
        path: "/select",
        exact: true,
        component: SituationCenterView
      },
      {
        path: "/space/:id",
        exact: true,
        component: SpaceView
      },
      {
        path: "/space/:id/item/:itemId",
        exact: true,
        component: SpaceView
      },
      // TODO: tab route for view type selection and tab to drive tab state?
      {
        path: "/examples/:example",
        exact: true,
        component: ExamplesView
      },
      {
        path: "/examples/",
        exact: true,
        component: ExamplesView
      },
      {
        path: "/spaces/",
        component: AllSpaces
      }
    ]
  }
  // TODO: Site/location selection

  // TODO:
  // label Print page, how do labels werk?
  // Do labels get printed from a django template/page?
  // Do we create a file object in the browser and print that?
]

export const spaceDetailUrl = (id: Scalars["ID"]) =>
  generatePath("/space/:id", { id })

export const spaceItemDetailUrl = (id: Scalars["ID"], itemId: Scalars["ID"]) =>
  generatePath("/space/:id/item/:itemId", { id, itemId })

export default routes
