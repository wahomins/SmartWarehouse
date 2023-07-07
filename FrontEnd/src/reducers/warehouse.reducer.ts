import { IWarehouseActionTypes } from 'models/IWarehouseState';

const initialState: any = {
  warehouseData: null,
};

const reducer = (state = initialState, { type, payload }: any) => {
  switch (type) {
    case IWarehouseActionTypes.FETCH_WAREHOUSE:
      return {
        ...state,
        warehouseData: payload,
      };
    default:
      return state;
  }
};

export default reducer;
