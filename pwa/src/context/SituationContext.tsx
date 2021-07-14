import { useMutation, useQuery } from "@apollo/client"
import { PopupState } from "material-ui-popup-state/core"
import React, { createContext, useCallback } from "react"
import {
  GetActiveSituationQuery,
  GetActiveSituationQueryVariables,
  Scalars,
  Site,
  SituationBitFragment
} from "client/types"
import {
  SELECT_ENTITIES,
  SITU_QUERY,
  UNSELECT_ENTITIES
} from "queries/situations"
import { difference, find, isEmpty } from "lodash"

// TODO:
// Refresh every so often to check for any situation changes.
// Track when the last time a situation was accessed
// and refresh after a certain period when attempting to interact/select.
// Session level data syncing between tabs?

export type SituValue =
  | {
      situation: SituationBitFragment | null
      site: Partial<Site> | null
      sites: Array<Site>
      loading: boolean
      select: (irns: Array<Scalars["IRN"]>) => any
      selectToggle: (irns: Array<Scalars["IRN"]>) => any
      unselect: (irns: Array<Scalars["IRN"]>) => any
      isItemSelected: (irn: Scalars["IRN"]) => any
      isSpaceSelected: (irn: Scalars["IRN"]) => any
      searchPopup: PopupState
      situDrawer: PopupState
    }
  | undefined

export type SituProviderProps = {
  interactions: {
    searchPopupState: PopupState
    situDrawerState: PopupState
  }
  children: React.ReactNode
}

const ActiveSituContext = createContext<SituValue>(undefined)

export const ActiveSituProvider: React.FC<SituProviderProps> = ({
  interactions: { searchPopupState, situDrawerState },
  children
}) => {
  const { data, loading, error, refetch } = useQuery<
    GetActiveSituationQuery,
    GetActiveSituationQueryVariables
  >(SITU_QUERY)

  // const allSelectedIRNs = data.
  const situation = data?.activeSituation ?? null
  const site = data?.currentSite ?? null
  const sites = data?.currentUser?.sites ?? []

  const [
    selectEntity,
    { loading: selectLoading, error: selectError }
  ] = useMutation(SELECT_ENTITIES, { onCompleted: () => refetch() })
  const [
    unselectEntity,
    { loading: unselectLoading, error: unselectError }
  ] = useMutation(UNSELECT_ENTITIES, { onCompleted: () => refetch() })

  const select = useCallback(
    (irns) => {
      return selectEntity({ variables: { irns } })
    },
    [selectEntity]
  )

  const unselect = useCallback(
    (irns) => {
      return unselectEntity({ variables: { irns } })
    },
    [unselectEntity]
  )

  const value = {
    situation,
    site,
    sites,
    loading: loading || selectLoading || unselectLoading,
    select,
    unselect,
    selectToggle(irns: Array<Scalars["IRN"]>) {
      const unselected: Array<Scalars["IRN"]> = []
      // look through all spaces and items selected and select which is to be
      // selected or unselected and then do that.
      // const unselect = situation?.items
      irns.forEach((irn) => {
        if (!!find(situation?.items, { irn })) {
          unselected.push(irn)
        }
      })
      irns.forEach((irn) => {
        if (!!find(situation?.spaces, { irn })) {
          unselected.push(irn)
        }
      })
      const selected = difference(irns, unselected)
      if (!isEmpty(selected)) {
        select(selected)
      }
      if (!isEmpty(unselected)) {
        unselect(unselected)
      }
    },
    isItemSelected(irn) {
      return !!find(situation?.items ?? [], { irn })
    },
    isSpaceSelected(irn) {
      return !!find(situation?.spaces ?? [], { irn })
    },
    searchPopup: searchPopupState,
    situDrawer: situDrawerState
  } as SituValue

  return (
    <ActiveSituContext.Provider value={value}>
      {children}
    </ActiveSituContext.Provider>
  )
}

export default ActiveSituContext
