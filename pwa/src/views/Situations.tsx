import React, { FC, useState } from "react";
import { Button, Card, CardContent, CardHeader, TextField, Box } from "@material-ui/core";
import { useMutation, useQuery } from "@apollo/client";
import { SITU_QUERY, SITU_ADD } from "../queries/situations"
import { irn } from "../utils/urns"


interface TestButtonProps {
    irn: string
    doEntry: (urnString: string) => void
}

const TestButton: FC<TestButtonProps> = ({ irn, doEntry }) => {
    return <Button variant="contained" onClick={() => doEntry(irn)}>{irn}</Button>
}
interface SituationsProps {
    reload?: boolean
}

const Situations: FC<SituationsProps> = ({ reload = false }) => {
    // const [focused, setFocused] = useState(false)
    const [value, setValue] = useState("")
    const [entries, setEntries] = useState<Array<string | null>>([])

    const handleChange = (event: any) => {
        setValue(event?.target?.value)
    }

    const { data, loading, error } = useQuery(SITU_QUERY)


    const [addEntity] = useMutation(SITU_ADD)

    const doEntry = (urnString: string) => {
        const parsed_irn = irn.parse(urnString)
        if (parsed_irn == null) return
        console.log(parsed_irn)
        setEntries([parsed_irn, ...entries])
        addEntity({
            variables: {
                input: {
                    irns: [parsed_irn]
                }
            }
        })
    }

    const handlePress = (event: any) => {
        if (event.key === "Enter") {
            doEntry(value)
            setValue("")
        }
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
                {loading ? "lol" : "not loading"}
                <pre>
                {JSON.stringify(data, null, 2)}
                {JSON.stringify(error, null, 2)}
                {JSON.stringify(entries, null, 2)}
                </pre>
                <Box m={3}>
                    <TestButton doEntry={doEntry} irn="irn:stage:spaces.gridspacenode:54" />
                    <TestButton doEntry={doEntry} irn="irn:stage:items.tool:2" />
                    <TestButton doEntry={doEntry} irn="irn:stage:items.consumable:5" />
                    <TestButton doEntry={doEntry} irn="irn:stage:items.trackedconsumable:4" />
                    <TestButton doEntry={doEntry} irn="irn:stage:spaces.spacenode:71" />
                </Box>
            </CardContent>
        </Card>
    )
}

export default Situations