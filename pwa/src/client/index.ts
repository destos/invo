import {
  ApolloClient,
  ApolloLink,
  createHttpLink,
  InMemoryCache,
  split
} from "@apollo/client"
import { WebSocketLink } from "@apollo/client/link/ws"
import { getMainDefinition } from "@apollo/client/utilities"
// import { buildClientSchema, IntrospectionQuery } from "graphql"
// import introspectionResult from "../generated/graphql.schema.json"
import { possibleTypes } from "../generated/possibleTypes.json"
// import { withScalars } from "apollo-link-scalars"
// import { irn } from "../utils/urns"
import { apolloLinkJWT } from "./auth"

// const schema = buildClientSchema(
//   (introspectionResult as unknown) as IntrospectionQuery
// )

const isBrowser = typeof window !== "undefined"

const httpLink = createHttpLink({
  uri: process.env.REACT_APP_API_GATEWAY,
  // credentials: "same-origin"
  credentials: "include"
})

const wsLink = new WebSocketLink({
  // @ts-ignore
  uri: process.env.REACT_APP_WS_API_GATEWAY,
  options: {
    // reconnect: true
    reconnect: false
  }
})

const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query)
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    )
  },
  wsLink,
  httpLink
)

// const typesMap = {
//   IRN: {
//     // TODO: swap any to IRN type
//     serialize: (parsed: any) => {
//       return irn.format(parsed)
//     },
//     parseValue: (raw: string | null): any | null => {
//       return raw ? irn.parse(raw) : null
//       // TODO: validation errors?
//       // const errors = irn.validated(parsed)
//     }
//   }
// }

const link = ApolloLink.from([
  // withScalars({
  //   schema,
  //   typesMap,
  //   removeTypenameFromInputs: true,
  //   validateEnums: true,
  // }),
  apolloLinkJWT,
  // httpLink
  splitLink
])

const client = new ApolloClient({
  connectToDevTools: isBrowser,
  cache: new InMemoryCache({ possibleTypes }),
  link
})

export default client
