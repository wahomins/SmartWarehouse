import { IDeviceActionTypes, IDeviceActionCreator, IDeviceState } from 'models/IDeviceState';

const initialState: any = {
  deviceData: null,
};

const reducer = (state = initialState, { type, payload }: any) => {
  console.log('device reducer: ', { type, payload });

  switch (type) {
    case IDeviceActionTypes.FETCH_DEVICE:
      return {
        ...state,
        deviceData: payload.devices,
      };

    default:
      return state;
  }
};

export default reducer;
