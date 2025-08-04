import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import rebateReducer from './slices/rebateSlice';
import exchangeReducer from './slices/exchangeSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    rebate: rebateReducer,
    exchange: exchangeReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 