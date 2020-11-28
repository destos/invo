import React, { FC, useState } from "react"
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  TextField,
  Box,
  List,
} from "@material-ui/core"
import { irn } from "../utils/urns"
import useSitu from "../hooks/useSitu"
import ItemListItem from "../components/ListItems/ItemListItem"
import SpaceListItem from "../components/ListItems/SpaceListItem"
// import IRNListItem from "../../holding/EntityListItem"

interface TestButtonProps {
  irn: string
  doEntry: (urnString: string) => void
}

const TestButton: FC<TestButtonProps> = ({ irn, doEntry }) => {
  return (
    <Button variant="contained" onClick={() => doEntry(irn)}>
      {irn}
    </Button>
  )
}

interface SituationCenterProps {
  reload?: boolean
}

const SituationCenter: FC<SituationCenterProps> = ({ reload = false }) => {
  // const [focused, setFocused] = useState(false)
  const [value, setValue] = useState("")
  const [entries, setEntries] = useState<Array<string | null>>([])

  const handleChange = (event: any) => {
    setValue(event?.target?.value)
  }

  const { situation, loading, select, unselect } = useSitu()

  const doEntry = (urnString: string) => {
    // const parsed_irn = irn.parse(urnString)
    // if (parsed_irn == null) return
    setEntries([urnString, ...entries])
    select([urnString])
  }

  const handlePress = (event: any) => {
    if (event.key === "Enter") {
      doEntry(value)
      setValue("")
    }
  }
  if (!situation) {
    return <>{"happinin"}</>
  }

  return (
    <Card>
      <CardHeader title="Finder" subheader="Finding the bits" />
      <CardContent>
        <TextField
          variant="outlined"
          onKeyPress={handlePress}
          value={value}
          onChange={handleChange}
          label="input"
          size="small"
          autoFocus
        />
        {/* <pre>
                {JSON.stringify(situation, null, 2)}
                </pre> */}
        <List>
          {situation.spaces.map((space) => (
            // @ts-ignore
            <SpaceListItem key={space.irn} entity={space} />
          ))}
          {situation.items.map((item) => (
            // @ts-ignore
            <ItemListItem key={item.irn} entity={item} />
          ))}
        </List>
        <Box m={3}>
          <TestButton
            doEntry={doEntry}
            irn="irn:stage:spaces.gridspacenode:54"
          />
          <TestButton doEntry={doEntry} irn="irn:stage:items.tool:2" />
          <TestButton doEntry={doEntry} irn="irn:stage:items.consumable:5" />
          <TestButton
            doEntry={doEntry}
            irn="irn:stage:items.trackedconsumable:4"
          />
          <TestButton doEntry={doEntry} irn="irn:stage:spaces.spacenode:71" />
        </Box>
      </CardContent>
    </Card>
  )
}

export default SituationCenter
