import { ApolloProvider } from "@apollo/client"
import React from "react"
import { renderRoutes } from "react-router-config"
import { BrowserRouter as Router } from "react-router-dom"
import "./App.css"
import client from "./client"
import routes from "./routes"

function App() {
  return (
    <ApolloProvider client={client}>
      <Router>{renderRoutes(routes)}</Router>
    </ApolloProvider>
  )
}

export default App
