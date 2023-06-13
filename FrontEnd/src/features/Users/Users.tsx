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

  console.log(usersData);
  const table = {
    rows: usersData || [],
    headers: [
      { columnName: 'UserId', key: '_id' },
      { columnName: 'Name', key: 'full_name' },
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
    />
  );
}
