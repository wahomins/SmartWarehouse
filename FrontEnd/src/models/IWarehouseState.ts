export enum IWarehouseActionTypes {
  FETCH_WAREHOUSE = 'WAREHOUSE/FETCH_WAREHOUSE',
  GET_WAREHOUSE = 'WAREHOUSE/GET_WAREHOUSE',
  ADD_WAREHOUSE = 'WAREHOUSE/ADD_WAREHOUSE',
  UPDATE_WAREHOUSE = 'WAREHOUSE/UPDATE_WAREHOUSE',
  DELETE_WAREHOUSE = 'WAREHOUSE/DELETE_WAREHOUSE',
}

export type IWarehouseState = {
  warehouseData: any | [];
};

export type IWarehouseActionCreator = {
  type: string;
  payload: IWarehouseState;
};
