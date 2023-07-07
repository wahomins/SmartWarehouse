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
    rows: devicesData || [],
    headers: [
      { columnName: 'Device Name', key: 'name', search: true, orderable: true },
      { columnName: 'Description', key: 'description' },
      { columnName: 'Device Group', key: 'device_group', search: true, orderable: true },
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
      mapData={mapData}
      onGridSearch={onGridSearch}
    />
  );
}
