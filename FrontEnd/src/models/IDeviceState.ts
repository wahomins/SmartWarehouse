export enum IDeviceActionTypes {
  FETCH_DEVICE = 'DEVICE/FETCH_DEVICE',
  GET_DEVICE = 'DEVICE/GET_DEVICE',
  ADD_DEVICE = 'DEVICE/ADD_DEVICE',
  UPDATE_DEVICE = 'DEVICE/UPDATE_DEVICE',
  DELETE_DEVICE = 'DEVICE/DELETE_DEVICE',
}

type ISingleDevice = {
  name: String;
  description: String;
  device_group: String;
  device_sub_group: String;
  active: boolean;
  local_ip: String;
  mac_address: String;
  warehouse: String;
  warehouse_id: String;
  device_sub_group_id: String;
  device_group_id: String;
};

export type IDeviceState = {
  deviceData: any | null;
};

export type IDeviceActionCreator = {
  type: string;
  payload: IDeviceState;
};
