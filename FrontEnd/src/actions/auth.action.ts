import { Dispatch } from 'redux';

// types
import { IAuthActionTypes } from 'models/IAuthState';
import { IHistory } from 'models/ICommon';

// services
import authService from 'services/authService';

// configs
import { PATH_NAME } from 'configs';

export const login = (username: string, password: string, history: IHistory) => async (dispatch: Dispatch<any>) => {
  dispatch({ type: IAuthActionTypes.LOGIN_REQUEST });

  const { fullName, user, role } = await authService.loginWithToken(username, password);
  dispatch({
    type: IAuthActionTypes.LOGIN_SUCCESS,
    payload: { fullName, user, role },
  });
  history.push(PATH_NAME.ROOT);
};

export const logout = () => (dispatch: Dispatch<any>) => {
  authService.logOut();
  dispatch({ type: IAuthActionTypes.LOGOUT });
};

export const setUserData = (user: any, username: string, role: string) => (dispatch: Dispatch<any>) => {
  dispatch({
    type: IAuthActionTypes.SILENT_LOGIN,
    payload: { user, fullName: username, role },
  });
};
