export type Maybe<T> = T | null
export type Exact<T extends { [key: string]: unknown }> = {
  [K in keyof T]: T[K]
}
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string
  String: string
  Boolean: boolean
  Int: number
  Float: number
  DateTime: any
  JSONData: any
  /** IRN, the invo URN scalar that can be used to differentiate entities and for entity lookup. */
  IRN: any
  Date: any
  URL: any
}

export type Query = {
  __typename?: "Query"
  waffle?: Maybe<Waffle>
  activeSituation?: Maybe<Situation>
  getIrnEntity?: Maybe<Protocol>
  space?: Maybe<SpaceTypes>
  getSpaces: Array<SpaceTypes>
  item?: Maybe<ItemTypes>
  items: Connection
}

export type QueryGetIrnEntityArgs = {
  irn: Scalars["IRN"]
}

export type QuerySpaceArgs = {
  id: Scalars["ID"]
}

export type QueryGetSpacesArgs = {
  filter?: Maybe<SpaceFilter>
}

export type QueryItemArgs = {
  id: Scalars["ID"]
}

export type QueryItemsArgs = {
  first?: Maybe<Scalars["Int"]>
  last?: Maybe<Scalars["Int"]>
  after?: Maybe<Scalars["String"]>
  before?: Maybe<Scalars["String"]>
}

export type Waffle = {
  __typename?: "Waffle"
  flags?: Maybe<Array<Maybe<WaffleFlag>>>
  switches?: Maybe<Array<Maybe<WaffleSwitch>>>
  samples?: Maybe<Array<Maybe<WaffleSample>>>
  all?: Maybe<Array<Maybe<WaffleItem>>>
  /** Retrieve a flag */
  flag?: Maybe<WaffleFlag>
  /** Retrieve a switch */
  switch?: Maybe<WaffleSwitch>
  /** Retrieve a sample */
  sample?: Maybe<WaffleSample>
  flagDefault?: Maybe<Scalars["Boolean"]>
  switchDefault?: Maybe<Scalars["Boolean"]>
  sampleDefault?: Maybe<Scalars["Boolean"]>
}

export type WaffleFlagArgs = {
  name?: Maybe<Scalars["String"]>
}

export type WaffleSwitchArgs = {
  name?: Maybe<Scalars["String"]>
}

export type WaffleSampleArgs = {
  name?: Maybe<Scalars["String"]>
}

export type WaffleFlag = WaffleItem &
  TimeStamped & {
    __typename?: "WaffleFlag"
    id?: Maybe<Scalars["ID"]>
    name?: Maybe<Scalars["String"]>
    active?: Maybe<Scalars["Boolean"]>
    note?: Maybe<Scalars["String"]>
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
  }

export type WaffleItem = {
  id?: Maybe<Scalars["ID"]>
  name?: Maybe<Scalars["String"]>
  active?: Maybe<Scalars["Boolean"]>
  note?: Maybe<Scalars["String"]>
}

export type TimeStamped = {
  created: Scalars["DateTime"]
  modified: Scalars["DateTime"]
}

export type WaffleSwitch = WaffleItem &
  TimeStamped & {
    __typename?: "WaffleSwitch"
    id?: Maybe<Scalars["ID"]>
    name?: Maybe<Scalars["String"]>
    active?: Maybe<Scalars["Boolean"]>
    note?: Maybe<Scalars["String"]>
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
  }

export type WaffleSample = WaffleItem &
  TimeStamped & {
    __typename?: "WaffleSample"
    id?: Maybe<Scalars["ID"]>
    name?: Maybe<Scalars["String"]>
    active?: Maybe<Scalars["Boolean"]>
    note?: Maybe<Scalars["String"]>
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
  }

export type Situation = Node &
  TimeStamped & {
    __typename?: "Situation"
    id: Scalars["ID"]
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
    user: User
    spaces: Array<Maybe<SpaceTypes>>
    items: Array<Maybe<ItemTypes>>
    state: SituationState
    exitCondition: SituationExit
  }

export type Node = {
  id: Scalars["ID"]
}

export type User = Node & {
  __typename?: "User"
  id: Scalars["ID"]
  username?: Maybe<Scalars["String"]>
  firstName?: Maybe<Scalars["String"]>
  listName?: Maybe<Scalars["String"]>
}

export type SpaceTypes = SpaceNode | GridSpaceNode

export type SpaceNode = SpaceInterface &
  TimeStamped &
  Protocol & {
    __typename?: "SpaceNode"
    id: Scalars["ID"]
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
    irn: Scalars["IRN"]
    name: Scalars["String"]
    parent?: Maybe<SpaceTypes>
    children: Array<SpaceTypes>
    items: Connection
    data?: Maybe<Scalars["JSONData"]>
    itemCount: Scalars["Int"]
  }

export type SpaceNodeChildrenArgs = {
  filter?: Maybe<SpaceFilter>
}

export type SpaceNodeItemsArgs = {
  first?: Maybe<Scalars["Int"]>
  last?: Maybe<Scalars["Int"]>
  after?: Maybe<Scalars["String"]>
  before?: Maybe<Scalars["String"]>
}

export type SpaceInterface = {
  id: Scalars["ID"]
  name: Scalars["String"]
  parent?: Maybe<SpaceTypes>
  children: Array<SpaceTypes>
  items: Connection
  data?: Maybe<Scalars["JSONData"]>
  itemCount: Scalars["Int"]
}

export type SpaceInterfaceChildrenArgs = {
  filter?: Maybe<SpaceFilter>
}

export type SpaceInterfaceItemsArgs = {
  first?: Maybe<Scalars["Int"]>
  last?: Maybe<Scalars["Int"]>
  after?: Maybe<Scalars["String"]>
  before?: Maybe<Scalars["String"]>
}

export type SpaceFilter = {
  name?: Maybe<Scalars["String"]>
  name__icontains?: Maybe<Scalars["String"]>
}

export type Connection = ListPageInfo & {
  __typename?: "Connection"
  pageInfo?: Maybe<PageInfo>
  edges?: Maybe<Array<Maybe<Edge>>>
}

export type ListPageInfo = {
  pageInfo?: Maybe<PageInfo>
}

export type PageInfo = {
  __typename?: "PageInfo"
  hasNextPage: Scalars["Boolean"]
  hasPreviousPage: Scalars["Boolean"]
  startCursor?: Maybe<Scalars["String"]>
  endCursor?: Maybe<Scalars["String"]>
  count?: Maybe<Scalars["Int"]>
}

export type Edge = {
  __typename?: "Edge"
  cursor?: Maybe<Scalars["String"]>
  node?: Maybe<Node>
}

export type Protocol = {
  irn: Scalars["IRN"]
}

export type GridSpaceNode = SpaceInterface &
  TimeStamped &
  Protocol & {
    __typename?: "GridSpaceNode"
    id: Scalars["ID"]
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
    irn: Scalars["IRN"]
    name: Scalars["String"]
    size?: Maybe<Array<Maybe<Scalars["Int"]>>>
    parent?: Maybe<SpaceTypes>
    children: Array<SpaceTypes>
    items: Connection
    data?: Maybe<Scalars["JSONData"]>
    itemCount: Scalars["Int"]
  }

export type GridSpaceNodeChildrenArgs = {
  filter?: Maybe<SpaceFilter>
}

export type GridSpaceNodeItemsArgs = {
  first?: Maybe<Scalars["Int"]>
  last?: Maybe<Scalars["Int"]>
  after?: Maybe<Scalars["String"]>
  before?: Maybe<Scalars["String"]>
}

/** All the different Item types */
export type ItemTypes = Item | Tool | Consumable | TrackedConsumable

export type Item = Node &
  ItemInterface &
  TimeStamped &
  Protocol & {
    __typename?: "Item"
    id: Scalars["ID"]
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
    irn: Scalars["IRN"]
    name: Scalars["String"]
    data?: Maybe<Scalars["JSONData"]>
    space?: Maybe<SpaceTypes>
    spaceParents: Array<Maybe<SpaceTypes>>
  }

export type ItemSpaceParentsArgs = {
  depth?: Maybe<Scalars["Int"]>
}

export type ItemInterface = {
  id: Scalars["ID"]
  name: Scalars["String"]
  data?: Maybe<Scalars["JSONData"]>
  space?: Maybe<SpaceTypes>
  spaceParents: Array<Maybe<SpaceTypes>>
}

export type ItemInterfaceSpaceParentsArgs = {
  depth?: Maybe<Scalars["Int"]>
}

export type Tool = Node &
  ItemInterface &
  TimeStamped &
  Protocol & {
    __typename?: "Tool"
    id: Scalars["ID"]
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
    irn: Scalars["IRN"]
    name: Scalars["String"]
    data?: Maybe<Scalars["JSONData"]>
    space?: Maybe<SpaceTypes>
    spaceParents: Array<Maybe<SpaceTypes>>
  }

export type ToolSpaceParentsArgs = {
  depth?: Maybe<Scalars["Int"]>
}

/** Consumables are items that consist of multiple physically similar objects, like screws. */
export type Consumable = Node &
  ItemInterface &
  ConsumableInterface &
  TimeStamped &
  Protocol & {
    __typename?: "Consumable"
    id: Scalars["ID"]
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
    irn: Scalars["IRN"]
    name: Scalars["String"]
    data?: Maybe<Scalars["JSONData"]>
    space?: Maybe<SpaceTypes>
    spaceParents: Array<Maybe<SpaceTypes>>
    count: Scalars["Int"]
    warningEnabled: Scalars["Boolean"]
    warningCount: Scalars["Float"]
    warning: Scalars["Boolean"]
  }

/** Consumables are items that consist of multiple physically similar objects, like screws. */
export type ConsumableSpaceParentsArgs = {
  depth?: Maybe<Scalars["Int"]>
}

export type ConsumableInterface = {
  count: Scalars["Int"]
  warningEnabled: Scalars["Boolean"]
  warningCount: Scalars["Float"]
  warning: Scalars["Boolean"]
}

/**
 * Tracked consumables hold a reference to identifiable information.
 * Like a bar code or item number, consuming Tracked items requires you pass
 * the reference that you are consuming.
 */
export type TrackedConsumable = Node &
  ItemInterface &
  ConsumableInterface &
  TimeStamped &
  Protocol & {
    __typename?: "TrackedConsumable"
    id: Scalars["ID"]
    created: Scalars["DateTime"]
    modified: Scalars["DateTime"]
    irn: Scalars["IRN"]
    name: Scalars["String"]
    data?: Maybe<Scalars["JSONData"]>
    space?: Maybe<SpaceTypes>
    spaceParents: Array<Maybe<SpaceTypes>>
    count: Scalars["Int"]
    warningEnabled: Scalars["Boolean"]
    warningCount: Scalars["Float"]
    warning: Scalars["Boolean"]
  }

/**
 * Tracked consumables hold a reference to identifiable information.
 * Like a bar code or item number, consuming Tracked items requires you pass
 * the reference that you are consuming.
 */
export type TrackedConsumableSpaceParentsArgs = {
  depth?: Maybe<Scalars["Int"]>
}

export enum SituationState {
  /** Just started and not interacted with */
  Start = "START",
  /** User is selecting entities */
  Selecting = "SELECTING",
  /** User decided to add new items? */
  Adding = "ADDING",
  /** User decided to place items in a space */
  Placing = "PLACING",
  /** User added more inventory */
  Increment = "INCREMENT",
  /** User consumed some inventory */
  Consuming = "CONSUMING"
}

export enum SituationExit {
  Open = "OPEN",
  Abandoned = "ABANDONED",
  Completed = "COMPLETED"
}

export type Mutation = {
  __typename?: "Mutation"
  root?: Maybe<Scalars["Boolean"]>
  selectEntities: SituationPayload
  unselectEntities: SituationPayload
  abandonSituation?: Maybe<Situation>
}

export type MutationSelectEntitiesArgs = {
  input: SelectEntitiesInput
}

export type MutationUnselectEntitiesArgs = {
  input: SelectEntitiesInput
}

export type SelectEntitiesInput = {
  irns: Array<Scalars["IRN"]>
}

export type SituationPayload = {
  __typename?: "SituationPayload"
  success: Scalars["Boolean"]
  object: Situation
  entities: Array<Maybe<Protocol>>
}

type Times_WaffleFlag_Fragment = { __typename?: "WaffleFlag" } & Pick<
  WaffleFlag,
  "created" | "modified"
>

type Times_WaffleSwitch_Fragment = { __typename?: "WaffleSwitch" } & Pick<
  WaffleSwitch,
  "created" | "modified"
>

type Times_WaffleSample_Fragment = { __typename?: "WaffleSample" } & Pick<
  WaffleSample,
  "created" | "modified"
>

type Times_Situation_Fragment = { __typename?: "Situation" } & Pick<
  Situation,
  "created" | "modified"
>

type Times_SpaceNode_Fragment = { __typename?: "SpaceNode" } & Pick<
  SpaceNode,
  "created" | "modified"
>

type Times_GridSpaceNode_Fragment = { __typename?: "GridSpaceNode" } & Pick<
  GridSpaceNode,
  "created" | "modified"
>

type Times_Item_Fragment = { __typename?: "Item" } & Pick<
  Item,
  "created" | "modified"
>

type Times_Tool_Fragment = { __typename?: "Tool" } & Pick<
  Tool,
  "created" | "modified"
>

type Times_Consumable_Fragment = { __typename?: "Consumable" } & Pick<
  Consumable,
  "created" | "modified"
>

type Times_TrackedConsumable_Fragment = {
  __typename?: "TrackedConsumable"
} & Pick<TrackedConsumable, "created" | "modified">

export type TimesFragment =
  | Times_WaffleFlag_Fragment
  | Times_WaffleSwitch_Fragment
  | Times_WaffleSample_Fragment
  | Times_Situation_Fragment
  | Times_SpaceNode_Fragment
  | Times_GridSpaceNode_Fragment
  | Times_Item_Fragment
  | Times_Tool_Fragment
  | Times_Consumable_Fragment
  | Times_TrackedConsumable_Fragment

export type SituationBitFragment = { __typename?: "Situation" } & Pick<
  Situation,
  "id" | "state"
> & {
    items: Array<
      Maybe<
        | ({ __typename?: "Item" } & ItemBit_Item_Fragment)
        | ({ __typename?: "Tool" } & ItemBit_Tool_Fragment)
        | ({ __typename?: "Consumable" } & ItemBit_Consumable_Fragment)
        | ({
            __typename?: "TrackedConsumable"
          } & ItemBit_TrackedConsumable_Fragment)
      >
    >
    spaces: Array<
      Maybe<
        | ({ __typename?: "SpaceNode" } & SpaceListContent_SpaceNode_Fragment)
        | ({
            __typename?: "GridSpaceNode"
          } & SpaceListContent_GridSpaceNode_Fragment)
      >
    >
  } & Times_Situation_Fragment

type ItemBit_Item_Fragment = { __typename?: "Item" } & Pick<
  Item,
  "id" | "name" | "data"
> & {
    space?: Maybe<
      | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
      | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
    >
    spaceParents: Array<
      Maybe<
        | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
        | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
      >
    >
  } & Times_Item_Fragment

type ItemBit_Tool_Fragment = { __typename?: "Tool" } & Pick<
  Tool,
  "id" | "name" | "data"
> & {
    space?: Maybe<
      | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
      | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
    >
    spaceParents: Array<
      Maybe<
        | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
        | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
      >
    >
  } & Times_Tool_Fragment

type ItemBit_Consumable_Fragment = { __typename?: "Consumable" } & Pick<
  Consumable,
  "id" | "name" | "data"
> & {
    space?: Maybe<
      | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
      | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
    >
    spaceParents: Array<
      Maybe<
        | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
        | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
      >
    >
  } & Times_Consumable_Fragment

type ItemBit_TrackedConsumable_Fragment = {
  __typename?: "TrackedConsumable"
} & Pick<TrackedConsumable, "id" | "name" | "data"> & {
    space?: Maybe<
      | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
      | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
    >
    spaceParents: Array<
      Maybe<
        | ({ __typename?: "SpaceNode" } & Pick<SpaceNode, "name">)
        | ({ __typename?: "GridSpaceNode" } & Pick<GridSpaceNode, "name">)
      >
    >
  } & Times_TrackedConsumable_Fragment

export type ItemListItemFragment =
  | ItemBit_Item_Fragment
  | ItemBit_Tool_Fragment
  | ItemBit_Consumable_Fragment
  | ItemBit_TrackedConsumable_Fragment

type SpaceListContent_SpaceNode_Fragment = { __typename?: "SpaceNode" } & Pick<
  SpaceNode,
  "id" | "name" | "data" | "itemCount"
> &
  Times_SpaceNode_Fragment

type SpaceListContent_GridSpaceNode_Fragment = {
  __typename?: "GridSpaceNode"
} & Pick<GridSpaceNode, "id" | "name" | "data" | "itemCount"> &
  Times_GridSpaceNode_Fragment

export type SpaceListContentFragment =
  | SpaceListContent_SpaceNode_Fragment
  | SpaceListContent_GridSpaceNode_Fragment

export type GetActiveSituationQueryVariables = Exact<{ [key: string]: never }>

export type GetActiveSituationQuery = { __typename?: "Query" } & {
  activeSituation?: Maybe<{ __typename?: "Situation" } & SituationBitFragment>
}

export type AddToActiveSituationMutationVariables = Exact<{
  input: SelectEntitiesInput
}>

export type AddToActiveSituationMutation = { __typename?: "Mutation" } & {
  selectEntities: { __typename?: "SituationPayload" } & Pick<
    SituationPayload,
    "success"
  > & { object: { __typename?: "Situation" } & SituationBitFragment }
}

export type RemoveFromActiveSituationMutationVariables = Exact<{
  input: SelectEntitiesInput
}>

export type RemoveFromActiveSituationMutation = { __typename?: "Mutation" } & {
  unselectEntities: { __typename?: "SituationPayload" } & Pick<
    SituationPayload,
    "success"
  > & { object: { __typename?: "Situation" } & SituationBitFragment }
}
