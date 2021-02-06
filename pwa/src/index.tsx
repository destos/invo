import React from "react"
import ReactDOM from "react-dom"
import "./index.css"
import "../node_modules/react-grid-layout/css/styles.css"
import "../node_modules/react-resizable/css/styles.css"
import * as Sentry from "@sentry/react"
import App from "./App"

const FinalApp = Sentry.withProfiler(App, { name: "CustomAppName" })

// import reportWebVitals from "./reportWebVitals"

ReactDOM.render(
  <React.StrictMode>
    <FinalApp />
  </React.StrictMode>,
  document.getElementById("root")
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals(console.log)
