import React from 'react';
import { useHistory } from 'react-router-dom';

// material core
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import AddIcon from '@material-ui/icons/Add';

// atomic
import PaginationBase from 'components/molecules/PaginationBase';

// helpers
import { canAction } from 'helpers';

// hooks
import { useCustomPagination } from 'hooks/usePagination';

interface SimpleGridProps {
  header: string;
  addPathName: string;
  actions: { resource: string; action: string }[];
  pagination: {
    pageNumber: number;
    itemsPerPage: number;
  };
  table: {
    rows: any[];
    headers: { columnName: string; key: string }[];
  };
}

function SimpleGrid(props: SimpleGridProps) {
  const { header, addPathName, actions, pagination, table } = props;
  const { pageNumber, itemsPerPage } = pagination;

  const history = useHistory();
  const { page, perPage, _changePage, _changePerPage } = useCustomPagination(pageNumber, itemsPerPage);

  return (
    <div>
      <Grid container alignItems="center">
        <Grid sm={8}>
          <h2>{header}</h2>
        </Grid>
        {actions && canAction('create', 'product') ? (
          <Grid container justify="flex-end">
            <Button
              type="submit"
              variant="contained"
              color="primary"
              startIcon={<AddIcon />}
              onClick={() => history.push(addPathName)}
            >
              Add {header}
            </Button>
          </Grid>
        ) : null}
        <br />
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                {table.headers.map((header) => (
                  <TableCell key={header.key}>{header.columnName}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {table.rows.map((row, index) => (
                <TableRow key={index}>
                  {table.headers.map((header) => (
                    <TableCell key={header.key}>{row[header.key]}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <PaginationBase
          pageIndex={page}
          perPage={perPage}
          totalPage={50}
          changePage={_changePage}
          changePerPage={_changePerPage}
        />
      </Grid>
    </div>
  );
}

export default SimpleGrid;
