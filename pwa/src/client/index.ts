import { ApolloClient, ApolloLink, createHttpLink, InMemoryCache, PossibleTypesMap } from '@apollo/client'
import { setContext } from '@apollo/client/link/context'
import { withScalars } from "apollo-link-scalars"
import { irn } from '../utils/urns'
import { possibleTypes } from "../generated/possibleTypes.json"
import introspectionResult from "../generated/graphql.schema.json"

import { buildClientSchema, IntrospectionQuery } from "graphql";

const schema = buildClientSchema((introspectionResult as unknown) as IntrospectionQuery)

const httpLink = createHttpLink({
  // uri: "http://macie.fhome.lan:8000/graphql",
  uri: "http://localhost:8000/graphql",
  // credentials: 'same-origin'
  credentials: 'include'
})

// const authLink = setContext((request, { cookies, headers }) => {
//   console.log(cookies, headers)
//   // get the authentication sessionid from local storage if it exists
//   // const sessionId = localStorage.getItem('sessionid')
//   // return the headers to the context so httpLink can read them
//   return {
//     // cookies: {
//     //   ...cookies,
//     //   sessionId
//     // },
//     headers: {
//       ...headers,
//       // Cookies: sessionId ? `sessionid=${sessionId}` : "",
//     }
//   }
// })

const typesMap = {
  IRN: {
    // TODO: swap any to IRN type
    serialize: (parsed: any) => irn.format(parsed),
    parseValue: (raw: string | number | null): any | null => {
      return raw ? new irn.parse(raw) : null;
      // TODO: validation errors?
      // const erros = irn.validated(parsed)
    }
  }
}

const link = ApolloLink.from([
  withScalars({ schema, typesMap, removeTypenameFromInputs: true, validateEnums: true }),
  // authLink,
  httpLink
])

const client = new ApolloClient({
  cache: new InMemoryCache({ possibleTypes }),
  link
})

export default client