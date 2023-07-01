import React, { useEffect } from 'react';
import SimpleGrid from 'components/SimpleGrid';
import { useDispatch, useSelector } from 'react-redux';
import { PATH_NAME, DRAWER_MENU_LABEL } from 'configs';
import { fetchAccesslogs } from 'actions/users.action';
import { usersAccessDataSelector } from 'selectors/user.selector';

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

  const table = {
    rows: usersData || [],
    headers: [
      { columnName: 'Device', key: 'device_name' },
      { columnName: 'User', key: 'user_name' },
      { columnName: 'Status', key: 'status' },
      { columnName: 'Timestamp', key: 'timestamp' },
      { columnName: 'username', key: 'username' },
    ],
  };

  return (
    <SimpleGrid
      header={header}
      addPathName=""
      updatePathName=""
      deletePathName=""
      actions={actions}
      pagination={pagination}
      table={table}
    />
  );
}
