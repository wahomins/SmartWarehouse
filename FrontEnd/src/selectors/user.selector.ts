import { createSelector } from 'reselect';

// types
import IRootState from 'models/IRootState';

export const isLoadingSelector = createSelector(
  (state: IRootState) => state.app,
  (app) => app.isLoading,
);

export const usersDataSelector = createSelector(
  (state: IRootState) => state.user,
  (user) => user.userData,
);

export const usersAccessDataSelector = createSelector(
  (state: IRootState) => state.user,
  (user) => user.userAccessData,
);
