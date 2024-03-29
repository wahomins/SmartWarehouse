import React, { useEffect } from 'react';
import SimpleGrid from 'components/SimpleGrid';
import { useDispatch, useSelector } from 'react-redux';
import { PATH_NAME, DRAWER_MENU_LABEL } from 'configs';
import { fetchUsers } from 'actions/users.action';
import { usersDataSelector } from 'selectors/user.selector';

export default function ProductList() {
  const header = 'Users';
  const addPathName = PATH_NAME.USER_ADD;
  const deletePathName = PATH_NAME.USER_ADD;
  const updatePathName = PATH_NAME.USER_ADD;
  const actions = { resource: DRAWER_MENU_LABEL.USERS, actions: ['create', 'update', 'delete', 'view'] };
  const pagination = {
    pageNumber: 1,
    itemsPerPage: 10,
  };

  const dispatch = useDispatch();
  const usersData = useSelector(usersDataSelector);
  // const usersData: any = useSelector((state) => state.user) || [];

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  const mapData = (key: string, row: any, headerName: string): any => {
    return row[key];
  };
  const onGridSearch = (rows: any[], searchValues: Record<string, string>, headers: any[]): any[] => {
    const results: [number, number][] = [];

    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];

      for (let j = 0; j < headers.length; j++) {
        const header = headers[j];
        const { columnName } = header;
        const searchValue = searchValues[columnName]?.toLowerCase();

        if (searchValue) {
          // Perform search where key in rows and value exists
          const keys = Object.keys(row);
          for (let k = 0; k < keys.length; k++) {
            const key = keys[k];
            const rowValue = row[key];
            const formattedRowValue = String(rowValue)?.toLowerCase();
            const regExp = new RegExp(searchValue, 'i');
            if (regExp.test(formattedRowValue)) {
              results.push(row);
              break;
            }
          }
        }
      }
    }
    return results;
  };
  const table = {
    rows: usersData || [],
    headers: [
      { columnName: 'UserId', key: '_id', search: true, orderable: true },
      { columnName: 'Name', key: 'full_name', search: true, orderable: true },
      { columnName: 'Email', key: 'email' },
      { columnName: 'Role', key: 'role' },
      { columnName: 'username', key: 'username' },
    ],
  };

  return (
    <SimpleGrid
      header={header}
      addPathName={addPathName}
      updatePathName={updatePathName}
      deletePathName={deletePathName}
      actions={actions}
      pagination={pagination}
      table={table}
      mapData={mapData}
      onGridSearch={onGridSearch}
    />
  );
}
