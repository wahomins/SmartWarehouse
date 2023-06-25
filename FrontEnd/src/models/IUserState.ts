export enum IUserActionTypes {
  FETCH_USER = 'USER/FETCH_USER',
  GET_USER = 'USER/GET_USER',
  ADD_USER = 'USER/ADD_USER',
  UPDATE_USER = 'USER/UPDATE_USER',
  DELETE_USER = 'USER/DELETE_USER',
  FETCH_USER_ACCESS_LOGS = 'USER/FETCH_USER_ACCESS_LOGS',
}

export type IUser = {
  full_name: String;
  accessToken: String;
  role: String;
  email: String;
  card_number: String;
  bio_data: String;
  warehouse_id: String;
};

export type IUserState = {
  userData: any | null;
};
