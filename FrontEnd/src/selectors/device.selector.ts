import { createSelector } from 'reselect';

// types
import IRootState from 'models/IRootState';

export const isLoadingSelector = createSelector(
  (state: IRootState) => state.app,
  (app) => app.isLoading,
);

export const devicesDataSelector = createSelector(
  (state: IRootState) => state.device,
  (device) => device.deviceData,
);
