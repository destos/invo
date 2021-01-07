import { ApolloProvider } from "@apollo/client"
import { ThemeProvider } from "@material-ui/core"
import { createMuiTheme } from "@material-ui/core/styles"
import React from "react"
import { renderRoutes } from "react-router-config"
import { BrowserRouter as Router } from "react-router-dom"
import "./App.css"
import client from "./client"
import routes from "./routes"

const theme = createMuiTheme({
  palette: {
    type: "dark",
    common: {
      black: "rgba(25, 25, 25, 1)",
      white: "rgba(250, 250, 250, 1)"
    },
    background: {
      paper: "rgba(74, 71, 64, 1)",
      default: "rgba(45, 45, 42, 1)"
    },
    primary: {
      light: "rgba(255, 175, 76, 1)",
      main: "rgba(244, 126, 23, 1)",
      dark: "rgba(187, 80, 0, 1)",
      contrastText: "#fff"
    },
    secondary: {
      light: "rgba(139, 107, 97, 1)",
      main: "rgba(93, 64, 55, 1)",
      dark: "rgba(50, 25, 17, 1)",
      contrastText: "#fff"
    },
    error: {
      light: "#e57373",
      main: "#f44336",
      dark: "#d32f2f",
      contrastText: "#fff"
    },
    text: {
      primary: "rgba(247, 247, 247, 0.87)",
      secondary: "rgba(222, 210, 197, 0.95)",
      disabled: "rgba(195, 195, 195, 0.77)",
      hint: "rgba(150, 147, 145, 0.38)"
    }
  }
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <ApolloProvider client={client}>
        <Router>{renderRoutes(routes)}</Router>
      </ApolloProvider>
    </ThemeProvider>
  )
}

export default App
