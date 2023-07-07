import React, { useEffect } from 'react';
import SimpleGrid from 'components/SimpleGrid';
import { useDispatch, useSelector } from 'react-redux';
import { PATH_NAME, DRAWER_MENU_LABEL } from 'configs';
import { fetchAccesslogs } from 'actions/users.action';
import { usersAccessDataSelector } from 'selectors/user.selector';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

export default function ProductList() {
  const header = 'AccessLogs';
  // const addPathName = PATH_NAME.USER_ADD;
  // const deletePathName = PATH_NAME.USER_ADD;
  // const updatePathName = PATH_NAME.USER_ADD;
  const actions = { resource: DRAWER_MENU_LABEL.USERS, actions: ['view'] };
  const pagination = {
    pageNumber: 1,
    itemsPerPage: 10,
  };

  const dispatch = useDispatch();
  const usersData = useSelector(usersAccessDataSelector);
  // const usersData: any = useSelector((state) => state.user) || [];

  useEffect(() => {
    dispatch(fetchAccesslogs());
  }, [dispatch]);

  const mapData = (key: string, row: any, headerName: string): any => {
    let value: any;

    switch (headerName) {
      case 'Status': {
        const { status } = row;
        const buttonColor = status.toLowerCase() === 'failed' ? '#E57373' : '#008000'; // Function to determine the button color based on severity

        // Custom styles for the button
        const StyledButton = withStyles(() => ({
          root: {
            background: buttonColor,
            color: '#FFF',
            textTransform: 'none',
            borderRadius: 4,
          },
        }))(Button);

        value = (
          <StyledButton variant="contained" disableElevation>
            {status}
          </StyledButton>
        );
        break;
      }
      default:
        value = row[key];
        break;
    }
    return value;
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
      { columnName: 'Timestamp', key: 'timestamp', search: true, orderable: true },
      { columnName: 'Device', key: 'device_name', search: true, orderable: true },
      { columnName: 'User', key: 'user_name', search: false, orderable: false },
      { columnName: 'Status', key: 'status', search: false, orderable: false },
      { columnName: 'Device Id', key: 'device_id', search: false, orderable: false },
    ],
  };
  // console.log(usersData, 'usersData');
  return (
    <SimpleGrid
      header={header}
      addPathName=""
      updatePathName=""
      deletePathName=""
      actions={actions}
      pagination={pagination}
      table={table}
      mapData={mapData}
      onGridSearch={onGridSearch}
    />
  );
}
