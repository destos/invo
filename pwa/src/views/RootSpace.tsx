// Show the top level spaces in your invo app
import { gql, useQuery } from "@apollo/client"
import React, { FC, useState } from "react"

type RootSpaceProps = {}

const GET_ROOT_SPACES = gql`
query getRootSpaces {
  spaces: getSpaces(filter: {level: 0}) {
    ...on SpaceInterface {
      id
      name
      itemCount
    }
  }
}
`

const RootSpace: FC<RootSpaceProps> = () => {
  const { data } = useQuery(GET_ROOT_SPACES, {
    fetchPolicy: "cache-and-network"
  })
  return (<>{ JSON.stringify(data) }</>)
}

export default RootSpace
