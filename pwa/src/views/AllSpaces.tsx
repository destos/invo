import { useQuery } from "@apollo/client"
import { Card, CardContent, CardHeader, TextField } from "@material-ui/core"
import ChevronRightIcon from "@material-ui/icons/ChevronRight"
import ExpandMoreIcon from "@material-ui/icons/ExpandMore"
import { TreeView } from "@material-ui/lab"
import React, { FC, useState } from "react"

interface AllSpacesProps {
  reload?: boolean
}

const AllSpaces: FC<AllSpacesProps> = ({ reload = false }) => {
  // const [focused, setFocused] = useState(false)
  const [value, setValue] = useState("")

  const handleChange = (event: any) => {
    setValue(event?.target?.value)
  }

  // const {} = useQuery()

  // const gridVisitor = (grids) => {}

  return (
    <Card>
      <CardHeader
        title="All Spaces"
        subheader="All your spaces, minus grid sub-spaces"
      />
      <CardContent>
        <TextField
          variant="outlined"
          value={value}
          onChange={handleChange}
          label="Search"
          size="small"
          autoFocus
        />
        <TreeView
          defaultCollapseIcon={<ExpandMoreIcon />}
          defaultExpandIcon={<ChevronRightIcon />}
        ></TreeView>
      </CardContent>
    </Card>
  )
}

export default AllSpaces
