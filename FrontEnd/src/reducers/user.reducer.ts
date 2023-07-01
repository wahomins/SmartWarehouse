import { IUserActionTypes } from 'models/IUserState';

const initialState: any = {
  userData: null,
};

const reducer = (state = initialState, { type, payload }: any) => {
  switch (type) {
    case IUserActionTypes.FETCH_USER:
      return {
        ...state,
        userData: payload,
      };

    case IUserActionTypes.FETCH_USER_ACCESS_LOGS:
      return {
        ...state,
        userAccessData: payload,
      };

    default:
      return state;
  }
};

export default reducer;
