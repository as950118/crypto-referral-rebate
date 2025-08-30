import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '../../utils/api';

interface Exchange {
  id: number;
  name: string;
  logo_url: string;
  api_configured: boolean;
  referral_link: string;
}

interface ExchangeState {
  exchanges: Exchange[];
  loading: boolean;
  error: string | null;
}

const initialState: ExchangeState = {
  exchanges: [],
  loading: false,
  error: null,
};

export const fetchExchanges = createAsyncThunk(
  'exchange/fetchExchanges',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/api/v1/exchanges/list/');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch exchanges');
    }
  }
);

export const configureExchangeAPI = createAsyncThunk(
  'exchange/configureAPI',
  async (data: { exchange_id: number; api_key: string; api_secret: string; passphrase?: string }, { rejectWithValue }) => {
    try {
      const response = await api.post('/api/v1/exchanges/configure/', data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to configure API');
    }
  }
);

const exchangeSlice = createSlice({
  name: 'exchange',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Exchanges
      .addCase(fetchExchanges.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchExchanges.fulfilled, (state, action) => {
        state.loading = false;
        state.exchanges = action.payload;
      })
      .addCase(fetchExchanges.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Configure API
      .addCase(configureExchangeAPI.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(configureExchangeAPI.fulfilled, (state, action) => {
        state.loading = false;
        // Update the specific exchange in the list
        const index = state.exchanges.findIndex(ex => ex.id === action.payload.id);
        if (index !== -1) {
          state.exchanges[index] = action.payload;
        }
      })
      .addCase(configureExchangeAPI.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError } = exchangeSlice.actions;
export default exchangeSlice.reducer; 