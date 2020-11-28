import { useMutation, useQuery } from "@apollo/client"
import { PopupState } from "material-ui-popup-state/core"
import React, { createContext } from "react"
import {
  GetActiveSituationQuery,
  GetActiveSituationQueryVariables,
  Scalars,
  SituationBitFragment
} from "../client/types"
import {
  SELECT_ENTITIES,
  SITU_QUERY,
  UNSELECT_ENTITIES
} from "../queries/situations"

export type SituValue =
  | {
      situation: SituationBitFragment | null
      loading: boolean
      select: (irns: any) => any
      unselect: (irns: any) => any
      searchPopup: PopupState
    }
  | undefined

export type SituProviderProps = {
  searchPopupState: PopupState
  children: React.ReactNode
}

const ActiveSituContext = createContext<SituValue>(undefined)

export const ActiveSituProvider: React.FC<SituProviderProps> = ({
  searchPopupState,
  children
}) => {
  const { data, loading, error } = useQuery<
    GetActiveSituationQuery,
    GetActiveSituationQueryVariables
  >(SITU_QUERY)

  const situation = data?.activeSituation ?? null

  const [
    selectEntity,
    { loading: selectLoading, error: selectError }
  ] = useMutation(SELECT_ENTITIES)
  const [
    unselectEntity,
    { loading: unselectLoading, error: unselectError }
  ] = useMutation(UNSELECT_ENTITIES)

  const value = {
    situation,
    loading: loading || selectLoading || unselectLoading,
    select(irns: Array<Scalars["IRN"]>) {
      return selectEntity({ variables: { irns } })
    },
    unselect(irns: Array<Scalars["IRN"]>) {
      return unselectEntity({ variables: { irns } })
    },
    searchPopup: searchPopupState
  }

  return (
    <ActiveSituContext.Provider value={value}>
      {children}
    </ActiveSituContext.Provider>
  )
}

export default ActiveSituContext
