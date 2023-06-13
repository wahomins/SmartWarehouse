import { combineReducers } from 'redux';

// reducers
import app from 'reducers/app.reducer';
import auth from 'reducers/auth.reducer';
import device from 'reducers/device.reducer';
import user from 'reducers/user.reducer';

const reducers = combineReducers({
  app,
  auth,
  device,
  user,
});

export default reducers;
