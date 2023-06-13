import { IUserActionTypes } from 'models/IUserState';

const initialState: any = {
  userData: null,
};

const reducer = (state = initialState, { type, payload }: any) => {
  console.log('user reducer: ', { type, payload });

  switch (type) {
    case IUserActionTypes.FETCH_USER:
      return {
        ...state,
        userData: payload,
      };

    default:
      return state;
  }
};

export default reducer;
