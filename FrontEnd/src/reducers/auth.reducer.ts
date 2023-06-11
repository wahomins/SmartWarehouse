import { IAuthActionTypes, IAuthActionCreator, IAuthState } from 'models/IAuthState';

const initialState: IAuthState = {
  user: null,
  fullName: null,
  role: null,
};

const reducer = (state = initialState, { type, payload }: IAuthActionCreator) => {
  console.log('auth reducer: ', { type, payload });

  switch (type) {
    case IAuthActionTypes.LOGIN_SUCCESS:
      return {
        ...state,
        user: payload.user,
        username: payload.fullName,
        role: payload.role,
      };
    case IAuthActionTypes.LOGIN_FAILURE:
      return {
        ...state,
        user: null,
      };
    case IAuthActionTypes.LOGOUT:
      return {
        ...state,
        user: null,
        role: null,
      };
    case IAuthActionTypes.SILENT_LOGIN:
      return {
        ...state,
        user: payload.user,
        username: payload.fullName,
        role: payload.role,
      };

    default:
      return state;
  }
};

export default reducer;
