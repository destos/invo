import { ApolloProvider } from "@apollo/client"
import { ThemeProvider } from "@material-ui/core"
import { AuthProvider } from "client/auth"
import React from "react"
import { renderRoutes } from "react-router-config"
import { Router, matchPath } from "react-router-dom"
import "./App.css"
import client from "./client"
import routes from "./routes"
import theme from "./theme"
import * as Sentry from "@sentry/react"
import { Integrations } from "@sentry/tracing"
import { createBrowserHistory } from "history"

const history = createBrowserHistory()

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  debug: process.env.NODE_ENV !== "production",
  integrations: [
    new Integrations.BrowserTracing({
      tracingOrigins: ["localhost", "myinvo.app", /^\//],
      routingInstrumentation: Sentry.reactRouterV5Instrumentation(
        history,
        // @ts-ignore
        routes,
        matchPath
      )
    })
  ],

  // We recommend adjusting this value in production, or using tracesSampler
  // for finer control
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
  release: "invo@" + process.env.REACT_APP_VERSION
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <ApolloProvider client={client}>
        <AuthProvider>
          <Router history={history}>{renderRoutes(routes)}</Router>
        </AuthProvider>
      </ApolloProvider>
    </ThemeProvider>
  )
}

export default App
