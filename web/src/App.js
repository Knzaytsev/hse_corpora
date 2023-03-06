import React, { useState, useEffect } from 'react';

import TablePaginationActions from './Pagination';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableFooter from '@mui/material/TableFooter';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { makeStyles } from '@mui/styles';
import TextField from '@mui/material/TextField';
import TableHead from '@mui/material/TableHead';
import LoadingSpinner from "./LoadingSpinner";
import Autocomplete from '@mui/material/Autocomplete';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';


const DEBUG = false

const useStyles = makeStyles({
    root: {
        marginLeft: '20',
        marginRight: '20',
    },
});

const pos_tags = [
    { label: 'NOUN' },
    { label: 'VERB' },
    { label: 'ADJ' },
    { label: 'ADV' },
    { label: 'SCONJ' },
    { label: 'DET' },
    { label: 'PRON' },
    { label: 'NUM' },
    { label: 'X' },
    { label: 'AUX' },
    { label: 'SYM' },
    { label: 'ADP' },
    { label: 'CCONJ' },
    { label: 'INTJ' },
    { label: 'PUNCT' },
    { label: 'PART' },
    { label: 'PROPN' },
]

const dep_tags = [
    { label: 'det' },
    { label: 'pobj' },
    { label: 'advcl' },
    { label: 'prt' },
    { label: 'agent' },
    { label: 'predet' },
    { label: 'nummod' },
    { label: 'csubjpass' },
    { label: 'conj' },
    { label: 'xx' },
    { label: 'xcomp' },
    { label: 'intj' },
    { label: 'ccomp' },
    { label: 'meta' },
    { label: 'neg' },
    { label: 'nsubjpass' },
    { label: 'punct' },
    { label: 'oprd' },
    { label: 'poss' },
    { label: 'attr' },
    { label: 'dobj' },
    { label: 'compound' },
    { label: 'nsubj' },
    { label: 'appos' },
    { label: 'nmod' },
    { label: 'amod' },
    { label: 'mark' },
    { label: 'acomp' },
    { label: 'aux' },
    { label: 'acl' },
    { label: 'case' },
    { label: 'parataxis' },
    { label: 'dep' },
    { label: 'cc' },
    { label: 'prep' },
    { label: 'ROOT' },
    { label: 'auxpass' },
    { label: 'pcomp' },
    { label: 'preconj' },
    { label: 'relcl' },
    { label: 'dative' },
    { label: 'csubj' },
    { label: 'advmod' },
    { label: 'npadvmod' },
    { label: 'quantmod' },
    { label: 'expl' },
]

export default function SearchableTable() {

    const classes = useStyles();
    const [searchTerm, setSearchTerm] = useState('');
    const [posTag, setPosTag] = useState([])
    const [depTag, setDepTag] = useState([])
    const [isEntered, setIsEntered] = useState(false)
    const [isLoading, setIsLoading] = useState(false);
    const [rows, setRows] = useState([]);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);

    useEffect(() => {
        const fictiveRequest = [
            {
                "by": "token",
                "value": "have",
                "conditions": [
                    {
                        "pos": "AUX"
                    },
                    {
                        "pos": "VERB"
                    }
                ]
            },
            {
                "by": "token",
                "value": "being"
            }
        ]

        if (isEntered) {
            const conditions = [
                {
                    "pos": posTag.map(({ label }) => label),
                    "dep": depTag.map(({ label }) => label),
                }
            ]

            const realRequest = [
                {
                    "by": "token",
                    "value": searchTerm,
                    "conditions": conditions,
                }
            ]

            setIsLoading(true);
            const body = DEBUG ? fictiveRequest : realRequest
            const requestData = JSON.stringify(body);

            console.log(requestData)

            // Fetch the data from the JSON file
            fetch(process.env.REACT_APP_API + "/search", {
                method: 'POST',
                headers: { "Content-type": "application/json" },
                body: requestData
            })
                .then((response) => response.json())
                .then((data) => {
                    // Set the rows state variable
                    setRows(data);
                    setIsLoading(false);
                });

            setIsEntered(false)
        }
    }, [isEntered, searchTerm, posTag, depTag]);

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleSearchEnter = (event) => {
        setIsEntered(event.key === 'Enter');
    };

    const handlePosTagChange = (event, value) => {
        setPosTag(value);
    };

    const handleDepTagChange = (event, value) => {
        setDepTag(value);
    };

    const emptyRows =
        page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    function boldTokens(row) {
        let offset = 0
        var boldRow = []
        for (let i = 0; i < row.num_fields; i++) {
            let start = row.sentence_tokens.slice(offset, row.token_start[i])
            let span_token = row.sentence_tokens.slice(row.token_start[i], row.token_end[i])
            span_token = <span style={{ fontWeight: 'bold' }}>{span_token}</span>
            offset = row.token_end[i]
            boldRow.push(start)
            boldRow.push(span_token)
        }
        let end = row.sentence_tokens.slice(offset, row.sentence_tokens.length)
        boldRow.push(end)
        return boldRow
    };

    const renderTableContent = (
        <TableContainer>
            <Table className={classes.root}>
                <TableHead component={Paper}>
                    <TableRow>
                        <TableCell style={{ width: 100 }} align="center">corpus</TableCell>
                        <TableCell align="left">sentence</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {(rowsPerPage > 0
                        ? rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                        : rows
                    ).map((row) => (
                        <TableRow key={row.name}>
                            <TableCell style={{ width: 100 }} align="center">{row.text_name}</TableCell>
                            <TableCell align="left">{boldTokens(row)}</TableCell>
                        </TableRow>
                    ))}

                    {emptyRows > 0 && (
                        <TableRow style={{ height: 53 * emptyRows }}>
                            <TableCell colSpan={6} />
                        </TableRow>
                    )}
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TablePagination
                            rowsPerPageOptions={[5, 10, 25, { label: 'All', value: -1 }]}
                            colSpan={3}
                            count={rows.length}
                            rowsPerPage={rowsPerPage}
                            page={page}
                            SelectProps={{
                                inputProps: {
                                    'aria-label': 'rows per page',
                                },
                                native: true,
                            }}
                            onPageChange={handleChangePage}
                            onRowsPerPageChange={handleChangeRowsPerPage}
                            ActionsComponent={TablePaginationActions}
                        />
                    </TableRow>
                </TableFooter>
            </Table>
        </TableContainer>
    )

    return (

        <Box
        sx={{
          pt: 4,
          pb: 3,
        }}
        >
        <Container maxWidth="xl">
        <Stack spacing={2}>
            <TextField
                label="Search"
                value={searchTerm}
                onChange={handleSearchChange}
                onKeyDown={handleSearchEnter}
                sx={{ width: '400px' }} />
            <Autocomplete
                multiple
                id="pos_tags"
                options={pos_tags}
                getOptionLabel={(option) => option.label}
                onChange={handlePosTagChange}
                filterSelectedOptions
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label="Filter by POS"
                        placeholder="POS tags" />
                )}
                sx={{ width: '400px' }} />
            <Autocomplete
                multiple
                id="dep_tags"
                options={dep_tags}
                getOptionLabel={(option) => option.label}
                onChange={handleDepTagChange}
                filterSelectedOptions
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label="Filter by DEP"
                        placeholder="DEP tags" />
                )}
                sx={{ width: '400px' }} />
            <div style={{ width: '100%' }}>{isLoading ? <LoadingSpinner /> : renderTableContent}</div>
            </Stack>
            </Container>
            </Box>

    );

}