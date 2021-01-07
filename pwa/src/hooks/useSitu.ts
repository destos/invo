import React from "react"
import SituationContext from "../context/SituationContext"

function useSitu() {
  const context = React.useContext(SituationContext)
  if (context === undefined) {
    throw new Error("`useSitu` must be within a `SituationContext`")
  }
  return context
}

export default useSitu
