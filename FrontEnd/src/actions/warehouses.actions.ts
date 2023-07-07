import { Dispatch } from 'redux';
import { IHistory } from 'models/ICommon';
import { IWarehouseActionTypes } from 'models/IWarehouseState';
// import { PATH_NAME } from 'configs';

import WarehouseService from 'services/warehouseService';

export const fetchWarehouses = () => async (dispatch: Dispatch<any>) => {
  const warehouses: any = await WarehouseService.fetchWarehouses();
  dispatch({
    type: IWarehouseActionTypes.FETCH_WAREHOUSE,
    payload: warehouses,
  });
};

export const getWarehouse = (warehouseId: string, history: IHistory) => async (dispatch: Dispatch<any>) => {
  dispatch({
    type: IWarehouseActionTypes.GET_WAREHOUSE,
    payload: {},
  });
};
