import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '../../utils/api';

interface RebateTransaction {
  id: number;
  amount: string;
  currency: string;
  commission_amount: string;
  status: string;
  transaction_date: string;
  exchange: string;
}

interface RebateStats {
  total_rebates: string;
  monthly_rebates: string;
  total_transactions: number;
  monthly_transactions: number;
}

interface RebateState {
  transactions: RebateTransaction[];
  stats: RebateStats | null;
  loading: boolean;
  error: string | null;
}

const initialState: RebateState = {
  transactions: [],
  stats: null,
  loading: false,
  error: null,
};

export const fetchRebateTransactions = createAsyncThunk(
  'rebate/fetchTransactions',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/api/v1/rebates/list/');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch transactions');
    }
  }
);

export const fetchRebateStats = createAsyncThunk(
  'rebate/fetchStats',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/api/v1/rebates/stats/');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch stats');
    }
  }
);

const rebateSlice = createSlice({
  name: 'rebate',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Transactions
      .addCase(fetchRebateTransactions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRebateTransactions.fulfilled, (state, action) => {
        state.loading = false;
        // API 응답이 배열이거나 객체 안에 배열이 있을 수 있음
        const payload = action.payload;
        if (Array.isArray(payload)) {
          state.transactions = payload;
        } else if (payload && Array.isArray(payload.results)) {
          state.transactions = payload.results;
        } else if (payload && Array.isArray(payload.recent_rebates)) {
          state.transactions = payload.recent_rebates;
        } else {
          state.transactions = [];
        }
      })
      .addCase(fetchRebateTransactions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch Stats
      .addCase(fetchRebateStats.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRebateStats.fulfilled, (state, action) => {
        state.loading = false;
        // API 응답에서 statistics 객체를 추출하거나 직접 사용
        const payload = action.payload;
        if (payload.statistics) {
          state.stats = {
            total_rebates: `$${payload.statistics.total_earnings || 0}`,
            monthly_rebates: `$${payload.statistics.monthly_earnings || 0}`,
            total_transactions: payload.statistics.total_transactions || 0,
            monthly_transactions: 0 // API에서 제공하지 않음
          };
        } else {
          state.stats = {
            total_rebates: `$${payload.total_earnings || 0}`,
            monthly_rebates: `$${payload.monthly_earnings || 0}`,
            total_transactions: payload.total_transactions || 0,
            monthly_transactions: 0
          };
        }
      })
      .addCase(fetchRebateStats.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError } = rebateSlice.actions;
export default rebateSlice.reducer; 