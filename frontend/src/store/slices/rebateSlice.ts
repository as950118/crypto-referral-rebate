import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

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
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/rebates/transactions/', {
        headers: { Authorization: `Bearer ${token}` }
      });
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
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/rebates/stats/', {
        headers: { Authorization: `Bearer ${token}` }
      });
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
        state.transactions = action.payload;
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
        state.stats = action.payload;
      })
      .addCase(fetchRebateStats.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError } = rebateSlice.actions;
export default rebateSlice.reducer; 