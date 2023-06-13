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
import IconButton from '@material-ui/core/IconButton';
import EditIcon from '@material-ui/icons/Edit';
import DeleteIcon from '@material-ui/icons/Delete';
import AddIcon from '@material-ui/icons/Add';

// atomic
import PaginationBase from 'components/molecules/PaginationBase';

// helpers
import { canAction } from 'helpers';

// hooks
import { useCustomPagination } from 'hooks/usePagination';

interface Action {
  resource: string;
  actions: string[];
}

interface Header {
  columnName: string;
  key: string;
}

interface SimpleGridProps {
  header: string;
  addPathName: string;
  actions: Action;
  deletePathName: string;
  updatePathName: string;
  pagination: {
    pageNumber: number;
    itemsPerPage: number;
  };
  table: {
    rows: any[];
    headers: Header[];
  };
}

function SimpleGrid(props: SimpleGridProps) {
  const { header, addPathName, actions, deletePathName, updatePathName, pagination, table } = props;
  const { pageNumber, itemsPerPage } = pagination;

  const history = useHistory();
  const { page, perPage, _changePage, _changePerPage } = useCustomPagination(pageNumber, itemsPerPage);
  const canCreate = actions.actions.includes('create') && canAction('create', actions.resource);
  const canUpdate = actions.actions.includes('update') && canAction('update', actions.resource);
  const canDelete = actions.actions.includes('delete') && canAction('delete', actions.resource);
  return (
    <div>
      <Grid container alignItems="center">
        <Grid sm={8}>
          <h2>{header}</h2>
        </Grid>
        {canCreate ? (
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
                {actions.actions.length > 0 ? <TableCell>Action</TableCell> : null}
              </TableRow>
            </TableHead>
            <TableBody>
              {table.rows.map((row, index) => (
                <TableRow key={index}>
                  {table.headers.map((header) => (
                    <TableCell key={header.key}>{row[header.key]}</TableCell>
                  ))}
                  {canUpdate ? (
                    <IconButton
                      color="primary"
                      aria-label="edit-device"
                      onClick={() => history.push(`${updatePathName}/${row.id}`)}
                    >
                      <EditIcon />
                    </IconButton>
                  ) : null}
                  {canDelete ? (
                    <IconButton
                      color="primary"
                      aria-label="delete-device"
                      onClick={() => history.push(`${deletePathName}/${row.id}`)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  ) : null}
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
