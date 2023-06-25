import React, { useEffect } from 'react';
import SimpleGrid from 'components/SimpleGrid';
import { useDispatch, useSelector } from 'react-redux';
import { PATH_NAME, DRAWER_MENU_LABEL } from 'configs';
import { fetchDevices } from 'actions/devices.actions';
import { devicesDataSelector } from 'selectors/device.selector';

export default function DeviceList() {
  const header = 'Devices';
  const addPathName = PATH_NAME.DEVICE_ADD;
  const deletePathName = PATH_NAME.DEVICE_ADD;
  const updatePathName = PATH_NAME.DEVICE_ADD;
  const actions = { resource: DRAWER_MENU_LABEL.DEVICE, actions: ['create', 'update', 'delete', 'view'] };
  const pagination = {
    pageNumber: 1,
    itemsPerPage: 10,
  };

  const dispatch = useDispatch();
  // const deviceData = useSelector((state) => state.device.deviceData);
  const devicesData: any = useSelector(devicesDataSelector);

  useEffect(() => {
    dispatch(fetchDevices());
  }, [dispatch]);

  const table = {
    rows: devicesData || [],
    headers: [
      { columnName: 'Device Name', key: 'name' },
      { columnName: 'Description', key: 'description' },
      { columnName: 'Device Group', key: 'device_group' },
      { columnName: 'Device Sub-Group', key: 'device_sub_group' },
      { columnName: 'active', key: 'active' },
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
