import { gql } from "@apollo/client";

const fragments = gql`
fragment Times on TimeStamped {
    created
    modified
}
fragment SituationBit on Situation {
    id
    ...Times
    state
    items {
        ...ItemBit
    }
    spaces {
        ...SpaceBit
    }
}
fragment ItemBit on ItemInterface {
    id
    ...Times
    name
    data
}
fragment SpaceBit on SpaceInterface {
    id
    ...Times
    name
    data
    itemCount
}
`
export default fragments