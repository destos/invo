// Auth is handled here
// There is a routing component that requires authentication be in place
// There is a hook that returns authenticated context
// Handle refreshing token when it expires with Apollo Link JWT

import { ApolloLinkJWT } from "apollo-link-jwt"
import AsyncStorage from "@react-native-async-storage/async-storage"
import {
  createContext,
  Dispatch,
  SetStateAction,
  useContext,
  useEffect,
  useState
} from "react"
import warning from "tiny-warning"
import { useHistory } from "react-router-dom"
import { useLazyQuery } from "@apollo/client"
import { GET_USER_DETAILS } from "queries/auth"
import {
  Maybe,
  User,
  UserDetailsQuery,
  UserDetailsQueryVariables
} from "./types"
// import cookie from "cookie"

const ACCESS_TOKEN = "at"
const REFRESH_TOKEN = "rt"

const getTokens = async () => {
  const accessToken = await AsyncStorage.getItem(ACCESS_TOKEN)
  // const refreshToken = cookie.parse(document.cookie)["refresh_token"]
  const refreshToken = await AsyncStorage.getItem(REFRESH_TOKEN)

  return {
    accessToken,
    refreshToken
  }
}

export const newTokenEvent = (token: string) => {
  // TODO: somehow use apollo for eventing auth events? or use schema/local variables?
  const event = new CustomEvent<string>("tokenChanged", {
    detail: token
  })
  return window.dispatchEvent(event)
}

const onRefreshComplete = async (data: any) => {
  // Find and return the access token and refresh token from the provided fetch callback
  // TODO: fix
  const newAccessToken = data?.data?.refreshToken?.token
  const newRefreshToken = data?.data?.refreshToken?.refreshToken

  // Handle sign out logic if the refresh token attempt failed
  if (!newAccessToken || !newRefreshToken) {
    warning(
      true,
      "Redirect back to login, because the refresh token was expired!"
    )

    // signOutHandler()
    return
  }

  newTokenEvent(newAccessToken)

  // Update tokens in AsyncStorage
  await AsyncStorage.setItem(ACCESS_TOKEN, newAccessToken)
  await AsyncStorage.setItem(REFRESH_TOKEN, newRefreshToken)

  // Return the tokens back to the lib to cache for later use
  return {
    newAccessToken,
    newRefreshToken
  }
}

/**
 * Configure the body of the token refresh method
 */
const fetchBody = async () => ({
  // query: `mutation refreshToken($refreshToken: String!) {
  //   refreshToken(token: $refreshToken) {
  //     token
  //     refreshToken
  //   }
  // }`,
  // variables: {
  refreshToken: await AsyncStorage.getItem(REFRESH_TOKEN)
  // }
})

/**
 * Create Apollo Link JWT
 */
export const apolloLinkJWT = ApolloLinkJWT({
  apiUrl: `${process.env.REACT_APP_API_GATEWAY}token/refresh/`,
  getTokens,
  fetchBody,
  onRefreshComplete,
  debugMode: true
})

// Authentication providers
interface IAuthContext {
  user: Maybe<Partial<User>>
  setTokens: Dispatch<SetStateAction<Tokens | null>>
}

const defaultAuth: IAuthContext = {
  user: null,
  setTokens: () => {}
}

export const AuthContext = createContext<IAuthContext>(defaultAuth)
export const AuthConsumer = AuthContext.Consumer

export const useAuth = () => {
  return useContext(AuthContext)
}

interface AuthProviderProps {
  // route: RouteConfig | undefined
  // unAuthedRedirect?: string
  // authedRedirect?: string
}

interface Tokens {
  access: Maybe<string>
  refresh: Maybe<string>
}
export const AuthProvider: React.FC<AuthProviderProps> = ({
  // route,
  children
  // unAuthedRedirect,
  // authedRedirect
}) => {
  const [tokens, setTokens] = useState<Tokens | null>(null)
  const [user, setUser] = useState<Maybe<Partial<User>>>(null)
  const history = useHistory()
  const [getUser, { loading }] = useLazyQuery<
    UserDetailsQuery,
    UserDetailsQueryVariables
  >(GET_USER_DETAILS, {
    fetchPolicy: "network-only",
    onCompleted: (data) => {
      setUser(data.user)
    }
  })

  // TODO: maybe use local storage hook instead of async storage handler, need to trigger login with access token in place
  useEffect(() => {
    const processTokens = async (tokens: Tokens) => {
      // setToken(token)
      await AsyncStorage.setItem(ACCESS_TOKEN, tokens.access ?? "")
      // TODO: temporary, until we can get token saving as cookie
      await AsyncStorage.setItem(REFRESH_TOKEN, tokens.refresh ?? "")
      getUser()
    }

    ;(async () => {
      // If token found on mount, possibly redirect
      // console.log(unAuthedRedirect, authedRedirect)
      if (tokens !== null) {
        await processTokens(tokens)
      }
    })()

    // const refreshState = (event: CustomEventInit<string>) => {
    //   processToken(event.detail ?? "")
    // }

    // If we store a logout value to localstorage, set the user to null
    // TODO: actually do this to log out
    const logoutCheck = (event: StorageEvent) => {
      if (event.key === "logout") {
        setUser(null)
      }
    }
    // Listen for logout storage events from other windows
    window.addEventListener("storage", logoutCheck)
    return () => {
      window.removeEventListener("storage", logoutCheck)
    }
  }, [setUser, getUser, tokens])

  // Attempt to get current user when component mounts, app layouts will direct properly if user set.
  useEffect(()=> {
    getUser()
  }, [])

  return (
    <AuthContext.Provider value={{ user, setTokens }}>
      {children}
      {/* {renderRoutes(route?.routes)} */}
    </AuthContext.Provider>
  )
}
