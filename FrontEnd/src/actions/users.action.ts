import { Dispatch } from 'redux';
import { IHistory } from 'models/ICommon';
import { IUserActionTypes } from 'models/IUserState';
// import { PATH_NAME } from 'configs';

import commonService from 'services/commonServices';

export const fetchUsers = () => async (dispatch: Dispatch<any>) => {
  const users: any = await commonService.callGet('/users/');
  dispatch({
    type: IUserActionTypes.FETCH_USER,
    payload: users,
  });
};

export const fetchAccesslogs = () => async (dispatch: Dispatch<any>) => {
  const users: any = await commonService.callGet('/users/logs/access/');
  dispatch({
    type: IUserActionTypes.FETCH_USER_ACCESS_LOGS,
    payload: users,
  });
};

export const getUser = (userId: string, history: IHistory) => async (dispatch: Dispatch<any>) => {
  dispatch({
    type: IUserActionTypes.FETCH_USER,
    payload: {},
  });
};
