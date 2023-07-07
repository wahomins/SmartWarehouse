import React, { useEffect } from 'react';
import SimpleGrid from 'components/SimpleGrid';
import { useDispatch, useSelector } from 'react-redux';
import { PATH_NAME, DRAWER_MENU_LABEL } from 'configs';
import { fetchDeviceActivities } from 'actions/devices.actions';
import { devicesActivitySelector } from 'selectors/device.selector';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';

export default function DeviceActivity() {
  const header = 'Device Logs';
  const addPathName = PATH_NAME.DEVICE_ADD;
  const deletePathName = PATH_NAME.DEVICE_ADD;
  const updatePathName = PATH_NAME.DEVICE_ADD;
  const actions = { resource: DRAWER_MENU_LABEL.DEVICE, actions: [] };
  const pagination = {
    pageNumber: 1,
    itemsPerPage: 10,
  };

  const dispatch = useDispatch();
  // const deviceData = useSelector((state) => state.device.deviceData);
  const devicesData: any = useSelector(devicesActivitySelector);

  useEffect(() => {
    dispatch(fetchDeviceActivities());
  }, [dispatch]);

  const getButtonColor = (severity: string): string => {
    let color: string;

    switch (severity) {
      case 'LOW':
        color = '#FFFFFF';
      case 'HIGH':
        color = '#E57373'; // Medium red shade for HIGH severity
        break;
      case 'CRITICAL':
        color = '#B71C1C'; // Dark red shade for CRITICAL severity
        break;
      default:
        color = '#808080'; // Default color for other severity levels
        break;
    }

    return color;
  };
  const mapData = (key: string, row: any, headerName: string): any => {
    let value: any;

    switch (headerName) {
      case 'Severity': {
        const { severity } = row.meta_data || {};

        const buttonColor = getButtonColor(severity); // Function to determine the button color based on severity

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
            {severity}
          </StyledButton>
        );
        break;
      }
      case 'Reading':
        value = row.meta_data?.reading || '';
        break;
      case 'Units':
        value = row.meta_data?.units || '';
        break;
      case 'Action':
        value = row.meta_data?.action || '';
        break;
      case 'Name':
        value = row.meta_data?.name || '';
        break;
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
          const value = row[columnName];
          // Perform MySQL-like search based on the columnName
          switch (columnName) {
            case 'Severity': {
              const { severity } = row.meta_data || {};
              const regExp = new RegExp(searchValue, 'i');
              if (regExp.test(severity)) {
                results.push(row);
              }
              break;
            }
            case 'Action': {
              const { action } = row.meta_data || {};
              const regExp = new RegExp(searchValue, 'i');
              if (regExp.test(action)) {
                results.push(row);
              }
              break;
            }
            case 'Name': {
              const { name } = row.meta_data || {};
              const regExp = new RegExp(searchValue, 'i');
              if (regExp.test(name)) {
                results.push(row);
              }
              break;
            }
            default: {
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
      { columnName: 'TimeStamp', key: 'timestamp', search: true, orderable: true },
      // { columnName: 'Description', key: 'action' },
      { columnName: 'Route', key: 'name', search: true, orderable: false },
      { columnName: 'Name', key: 'meta_data.name', search: true, orderable: false },
      { columnName: 'Action', key: 'action', search: true, orderable: false },
      { columnName: 'Severity', key: 'severity', search: true, orderable: false },
      { columnName: 'Reading', key: 'reading', search: false, orderable: true },
      { columnName: 'Units', key: 'units', search: false, orderable: false },
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
