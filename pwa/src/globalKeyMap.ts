import { KeyMap } from "react-hotkeys"

const globalKeyMap: KeyMap = {
  // @ts-ignore
  KONAMI: {
    name: "Konami code",
    sequence: "up up down down left right left right b a enter"
  },
  // LOG_DOWN: { name: "Log Cmd Down", sequence: "command", action: "keydown" },
  // LOG_UP: { name: "Log Cmd Up", sequence: "command", action: "keyup" },
  SHOW_DIALOG: {
    name: "Display keyboard shortcuts",
    sequence: "shift+?",
    action: "keyup"
  }
}

export default globalKeyMap
