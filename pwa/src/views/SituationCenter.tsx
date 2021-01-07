import {
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  TextField
} from "@material-ui/core"
import ItemListContent from "components/listItems/ItemListContent"
import SpaceListContent from "components/listItems/SpaceListContent"
import useSitu from "hooks/useSitu"
import React, { FC, useState } from "react"

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
    return <>{"it's happening!"}</>
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
        {/* If items/spaces are empty, show a large select area for each type */}
        <List>
          {situation.spaces.map((space) => (
            <ListItem key={space.irn}>
              <SpaceListContent key={space.irn} entity={space} />
            </ListItem>
          ))}
          {situation.items.map((item) => (
            <ListItem key={item.irn}>
              <ItemListContent entity={item} />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  )
}

export default SituationCenter
