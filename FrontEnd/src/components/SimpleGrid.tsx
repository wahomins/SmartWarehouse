import React from 'react';
import { useHistory } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import AddIcon from '@material-ui/icons/Add';

import PaginationBase from 'components/molecules/PaginationBase';
import SimpleTable from 'components/SimpleTable';
import { canAction } from 'helpers';
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
  mapData: any;
  onGridSearch: any;
}

const SimpleGrid: React.FC<SimpleGridProps> = (props) => {
  const { header, addPathName, actions, deletePathName, updatePathName, pagination, table, mapData, onGridSearch } = props;
  const { pageNumber, itemsPerPage } = pagination;

  const history = useHistory();
  const { page, perPage, _changePage, _changePerPage } = useCustomPagination(pageNumber, itemsPerPage);
  const totalPages = Math.ceil(table.rows.length / perPage);
  const canCreate = actions.actions.includes('create') && canAction('create', actions.resource);
  const canUpdate = actions.actions.includes('update') && canAction('update', actions.resource);
  const canDelete = actions.actions.includes('delete') && canAction('delete', actions.resource);

  return (
    <div>
      <Grid container alignItems="center">
        <Grid sm={8}>
          <h2>{header}</h2>
        </Grid>
        {canCreate && (
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
        )}
        <SimpleTable
          page={page}
          perPage={perPage}
          rows={table.rows}
          headers={table.headers}
          canUpdate={canUpdate}
          canDelete={canDelete}
          history={history}
          updatePathName={updatePathName}
          deletePathName={deletePathName}
          mapData={mapData}
          onGridSearch={onGridSearch}
        />
        <PaginationBase
          pageIndex={page}
          perPage={perPage}
          totalPage={totalPages}
          changePage={_changePage}
          changePerPage={_changePerPage}
        />
      </Grid>
    </div>
  );
};

export default SimpleGrid;
