import { Dispatch } from 'redux';
import { IHistory } from 'models/ICommon';
import { IDeviceActionTypes } from 'models/IDeviceState';
// import { PATH_NAME } from 'configs';

import deviceService from 'services/deviceSerice';

export const fetchDevices = () => async (dispatch: Dispatch<any>) => {
  const devices: any = await deviceService.fetchDevices();
  dispatch({
    type: IDeviceActionTypes.FETCH_DEVICE,
    payload: devices,
  });
};

export const getDevice = (deviceId: string, history: IHistory) => async (dispatch: Dispatch<any>) => {
  dispatch({
    type: IDeviceActionTypes.GET_DEVICE,
    payload: {},
  });
};

export const fetchDeviceActivities = () => async (dispatch: Dispatch<any>) => {
  dispatch({
    type: IDeviceActionTypes.FETCH_DEVICE_ACTIVIES,
    payload: {},
  });
};
