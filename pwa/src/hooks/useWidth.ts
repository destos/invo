import { Theme, useTheme } from "@material-ui/core/styles"
import { Breakpoint } from "@material-ui/core/styles/createBreakpoints"
import useMediaQuery from "@material-ui/core/useMediaQuery"

type BreakpointOrNull = Breakpoint | null

/**
 * Be careful using this hook. It only works because the number of
 * breakpoints in theme is static. It will break once you change the number of
 * breakpoints. See https://reactjs.org/docs/hooks-rules.html#only-call-hooks-at-the-top-level
 */
function useWidth() {
  const theme: Theme = useTheme()
  const keys: Breakpoint[] = [...theme.breakpoints.keys].reverse()
  const current =
    keys.reduce((output: BreakpointOrNull, key: Breakpoint) => {
      // eslint-disable-next-line react-hooks/rules-of-hooks
      const matches = useMediaQuery(theme.breakpoints.up(key))
      return !output && matches ? key : output
    }, null) || "xs"
  return theme.breakpoints.width(current)
}

export default useWidth
