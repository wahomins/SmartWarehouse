import { IAppState } from './IAppState';
import { IAuthState } from './IAuthState';
import { IDeviceState } from './IDeviceState';
import { IUserState } from './IUserState';
import { IWarehouseState } from './IWarehouseState';

type IRootState = {
  app: IAppState;
  auth: IAuthState;
  device: IDeviceState;
  user: IUserState;
  warehouse: IWarehouseState;
};

export default IRootState;
