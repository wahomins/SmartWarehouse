import React, { useState } from 'react';
import { IconButton, TableBody, TableCell, TableContainer, TableHead, TableRow, Table, Paper } from '@material-ui/core';
import { Edit as EditIcon, Delete as DeleteIcon, ArrowUpward, ArrowDownward } from '@material-ui/icons';

interface SimpleTableProps {
  page: number;
  perPage: number;
  rows: any[];
  headers: { key: string; columnName: string; search?: boolean; orderable?: boolean }[];
  canUpdate: boolean;
  canDelete: boolean;
  history: any;
  updatePathName: string;
  deletePathName: string;
  mapData: any;
  onGridSearch: any;
}

const SimpleTable: React.FC<SimpleTableProps> = ({
  page,
  perPage,
  rows,
  headers,
  canUpdate,
  canDelete,
  history,
  updatePathName,
  deletePathName,
  mapData,
  onGridSearch,
}) => {
  const startIndex = (page - 1) * perPage;
  const endIndex = startIndex + perPage;
  const [searchValues, setSearchValues] = useState<Record<string, string>>({});
  const [sortKey, setSortKey] = useState<string>(headers[0]?.key || '');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>, header: any) => {
    const { value } = e.target;
    if (Object.keys(searchValues).length === 1 && value.length === 0) {
      setSearchValues({});
    } else {
      setSearchValues((prevSearchValues) => ({
        ...prevSearchValues,
        [header.columnName]: value,
      }));
    }
  };

  const getSortIcon = (key: string) => {
    if (key === sortKey) {
      return sortOrder === 'asc' ? <ArrowUpward /> : <ArrowDownward />;
    }
    return (
      <span style={{ opacity: 0.5, display: 'inline-flex' }}>
        <ArrowUpward />
      </span>
    );
  };

  const handleSortClick = (key: string) => {
    if (key === sortKey) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('desc');
    }
  };

  const filteredRows = Object.keys(searchValues).length > 0 ? onGridSearch(rows, searchValues, headers) : rows;

  const sortedRows = filteredRows;
  // ? filteredRows.slice().sort((a, b) => {
  //     const valueA = a[sortKey];
  //     const valueB = b[sortKey];
  //     if (valueA < valueB) {
  //       return sortOrder === 'asc' ? -1 : 1;
  //     }
  //     if (valueA > valueB) {
  //       return sortOrder === 'asc' ? 1 : -1;
  //     }
  //     return 0;
  //   })
  // : filteredRows;

  const pageRows = sortedRows.slice(startIndex, endIndex);

  return (
    <TableContainer component={Paper}>
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            {headers.map((header) => (
              <TableCell key={header.key}>
                {header.columnName}
                {header.orderable && (
                  <IconButton onClick={() => handleSortClick(header.key)} disabled={sortKey !== header.key}>
                    {getSortIcon(header.key)}
                  </IconButton>
                )}
              </TableCell>
            ))}
            {(canUpdate || canDelete) && <TableCell>Action</TableCell>}
          </TableRow>
          <TableRow>
            {headers.map((header, index) => (
              <TableCell key={`${header.key}-${index}`}>
                {header.search && (
                  <input
                    key={`${header.key}-${index}`}
                    type="text"
                    value={searchValues[header.columnName] || ''}
                    onChange={(e) => handleSearchChange(e, header)}
                    placeholder={`Search ${header.columnName}`}
                  />
                )}
              </TableCell>
            ))}
            {(canUpdate || canDelete) && <TableCell />}
          </TableRow>
        </TableHead>

        <TableBody>
          {pageRows.map((row, index) => (
            <TableRow key={index}>
              {headers.map((header) => (
                <TableCell key={header.key}>{mapData(header.key, row, header.columnName)}</TableCell>
              ))}
              {canUpdate && (
                <IconButton color="primary" aria-label="edit-device" onClick={() => history.push(`${updatePathName}/${row.id}`)}>
                  <EditIcon />
                </IconButton>
              )}
              {canDelete && (
                <IconButton
                  color="primary"
                  aria-label="delete-device"
                  onClick={() => history.push(`${deletePathName}/${row.id}`)}
                >
                  <DeleteIcon />
                </IconButton>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SimpleTable;
