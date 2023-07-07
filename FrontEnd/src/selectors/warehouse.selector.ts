import { createSelector } from 'reselect';

// types
import IRootState from 'models/IRootState';

export const isLoadingSelector = createSelector(
  (state: IRootState) => state.app,
  (app) => app.isLoading,
);

export const warehousesDataSelector = createSelector(
  (state: IRootState) => state.warehouse,
  (warehouse) => warehouse.warehouseData,
);
