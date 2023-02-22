import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableFooter from '@mui/material/TableFooter';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import FirstPageIcon from '@mui/icons-material/FirstPage';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import LastPageIcon from '@mui/icons-material/LastPage';
import { makeStyles } from '@mui/styles';
import TextField from '@mui/material/TextField';
import TableHead from '@mui/material/TableHead';
import LoadingSpinner from "./LoadingSpinner";

const DEBUG = false

const useStyles = makeStyles({
    root: {
        marginLeft: '20',
        marginRight: '20'
    },
});

function TablePaginationActions(props) {
    const theme = useTheme();
    const { count, page, rowsPerPage, onPageChange } = props;

    const handleFirstPageButtonClick = (event) => {
        onPageChange(event, 0);
    };

    const handleBackButtonClick = (event) => {
        onPageChange(event, page - 1);
    };

    const handleNextButtonClick = (event) => {
        onPageChange(event, page + 1);
    };

    const handleLastPageButtonClick = (event) => {
        onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
    };

    return (
        <Box sx={{ flexShrink: 0, ml: 2.5 }}>
            <IconButton
                onClick={handleFirstPageButtonClick}
                disabled={page === 0}
                aria-label="first page"
            >
                {theme.direction === 'rtl' ? <LastPageIcon /> : <FirstPageIcon />}
            </IconButton>
            <IconButton
                onClick={handleBackButtonClick}
                disabled={page === 0}
                aria-label="previous page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowRight /> : <KeyboardArrowLeft />}
            </IconButton>
            <IconButton
                onClick={handleNextButtonClick}
                disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                aria-label="next page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowLeft /> : <KeyboardArrowRight />}
            </IconButton>
            <IconButton
                onClick={handleLastPageButtonClick}
                disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                aria-label="last page"
            >
                {theme.direction === 'rtl' ? <FirstPageIcon /> : <LastPageIcon />}
            </IconButton>
        </Box>
    );
}

TablePaginationActions.propTypes = {
    count: PropTypes.number.isRequired,
    onPageChange: PropTypes.func.isRequired,
    page: PropTypes.number.isRequired,
    rowsPerPage: PropTypes.number.isRequired,
};

export default function SearchableTable() {
    const classes = useStyles();
    const [searchTerm, setSearchTerm] = useState('');
    const [isEntered, setIsEntered] = useState(false)
    const [isLoading, setIsLoading] = useState(false);
    const [rows, setRows] = useState([]);
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(5);

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

        const realRequest = [
            {
                "by": "token",
                "value": searchTerm
            }
        ]


        if (isEntered) {
            setIsLoading(true);
            const body = DEBUG ? fictiveRequest : realRequest
            const request_data = JSON.stringify(body);

            // Fetch the data from the JSON file
            fetch(process.env.REACT_APP_API + "/search", {
                method: 'POST',
                headers: { "Content-type": "application/json" },
                body: request_data
            })
                .then((response) => response.json())
                .then((data) => {
                    // Set the rows state variable
                    setRows(data);
                    setIsLoading(false);
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
    }

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
        <>
            <TextField
                label="Search"
                value={searchTerm}
                onChange={handleSearchChange}
                onKeyDown={handleSearchEnter}
            />
            <div>{isLoading ? <LoadingSpinner /> : renderTableContent}</div>
        </>
    );
};