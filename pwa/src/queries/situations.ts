import { gql } from "@apollo/client";
import fragments from "./fragments"

export const SITU_QUERY = gql`
query getActiveSituation {
    activeSituation {
        ...SituationBit
    }
}
${fragments}
`

export const SITU_ADD = gql`
mutation  addToActiveSituation($input: SelectEntitiesInput!) {
    selectEntities(input: $input) {
        success
        object {
            ...SituationBit
        }
    }
}
${fragments}
`