import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles({
    root: {
        width: '100%',
    },
});

export default function SearchableTable() {
    const classes = useStyles();
    const [searchTerm, setSearchTerm] = useState('');
    const [isEntered, setIsEntered] = useState(false)
    const [rows, setRows] = useState([]);

    useEffect(() => {
        if (isEntered){
        const request_data = JSON.stringify(
            [
                {
                    "conditions": [
                        {
                            "token": searchTerm
                        }
                    ]
                }
            ])

        // Fetch the data from the JSON file
        fetch('http://localhost:8080/search', {
            method: 'POST',
            headers: { "Content-type": "application/json" },
            body: request_data
        })
            .then((response) => response.json())
            .then((data) => {
                // Set the rows state variable
                setRows(data);
            });
        
        setIsEntered(false)
        }
    }, [isEntered, searchTerm]);

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleSearchEnter = (event) => {
        setIsEntered(event.key === 'Enter')
    }

    return (
        <>
            <TextField
                label="Search"
                value={searchTerm}
                onChange={handleSearchChange}
                onKeyDown={handleSearchEnter}
            />
            <Table className={classes.root}>
                <TableHead>
                    <TableRow>
                        <TableCell align="right">corpus</TableCell>
                        <TableCell align="right">token</TableCell>
                        <TableCell align="left">sentence</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <TableRow key={row.name}>
                            <TableCell align="right">{row.text_name}</TableCell>
                            <TableCell align="right">{row.token}</TableCell>
                            <TableCell align="left">{row.sentence_tokens}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </>
    );
};