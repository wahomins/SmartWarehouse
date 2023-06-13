import { IAppState } from './IAppState';
import { IAuthState } from './IAuthState';
import { IDeviceState } from './IDeviceState';
import { IUserState } from './IUserState';

type IRootState = {
  app: IAppState;
  auth: IAuthState;
  device: IDeviceState;
  user: IUserState;
};

export default IRootState;
