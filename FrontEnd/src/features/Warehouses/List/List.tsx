import React, { useEffect } from 'react';
import SimpleGrid from 'components/SimpleGrid';
import { useDispatch, useSelector } from 'react-redux';
import { PATH_NAME, DRAWER_MENU_LABEL } from 'configs';
import { fetchWarehouses } from 'actions/warehouses.actions';
import { warehousesDataSelector } from 'selectors/warehouse.selector';

export default function WarehouseList() {
  const header = 'Warehouses';
  const addPathName = 'PATH_NAME.DEVICE_ADD';
  const deletePathName = 'PATH_NAME.DEVICE_ADD';
  const updatePathName = 'PATH_NAME.DEVICE_ADD';
  const actions = { resource: DRAWER_MENU_LABEL.DEVICE, actions: ['create', 'update', 'delete', 'view'] };
  const pagination = {
    pageNumber: 1,
    itemsPerPage: 10,
  };

  const dispatch = useDispatch();
  // const deviceData = useSelector((state) => state.device.deviceData);
  const warehousesData: any = useSelector(warehousesDataSelector);

  useEffect(() => {
    dispatch(fetchWarehouses());
  }, [dispatch]);

  const mapData = (key: string, row: any, headerName: string): any => {
    let value: any;

    switch (headerName) {
      case 'Location': {
        value = `(${row.latitute}, ${row.longitude})`;
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
    rows: warehousesData || [],
    headers: [
      { columnName: 'Name', key: 'name' },
      { columnName: 'Description', key: 'description' },
      { columnName: 'Manager', key: 'manager_name' },
      { columnName: 'town', key: 'town' },
      { columnName: 'close Land Mark', key: 'close_land_mark' },
      { columnName: 'Location', key: 'longitude' },
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
