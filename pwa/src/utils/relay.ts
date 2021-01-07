// Typescript to take connection and set return type properly
// type Deconstructor<O> = {
//   relayObj: O
// }

// import { Connection } from "client/types"

// interface Edge<Node> {
//   cursor: string
//   node: Node
// }

// interface Connection<Node> {
//   edges: Edge<Node>
// }


// const relayDeconstructor: <O extends Connection> = (relayObj: O): any => {
export const relayDeconstructor = (relayObj: any): any => {
  if (!relayObj || typeof relayObj !== "object" || Array.isArray(relayObj)) {
    return relayObj
  }

  const result: any = {}

  // If we are a connection iterate and return
  if (relayObj.edges && Array.isArray(relayObj.edges)) {
    return [
      ...relayObj.edges.map((edge: any) => {
        const { node, ...theRest } = edge
        if (!node) {
          return theRest
        }
        const deconstructedNode = relayDeconstructor(node)
        return { ...theRest, ...deconstructedNode }
      })
    ]
  }

  // // pass in full object with relay connections to be deconstructed
  Object.entries(relayObj).forEach(([key, value]) => {
    result[key] = relayDeconstructor(value)
  })

  return result
}
