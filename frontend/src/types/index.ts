// frontend/src/types/index.ts

// ==================== USER TYPES ====================

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface LoginCredentials {
  username: string; // API expects 'username' field for email
  password: string;
}

export interface RegisterData {
  email: string;
  full_name: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// ==================== EXPENSE TYPES ====================

export interface Expense {
  id: string;
  user_id: string;
  title: string;
  amount: number;
  category: string;
  date: string;
  payment_method: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface ExpenseCreate {
  title: string;
  amount: number;
  category: string;
  date: string;
  payment_method?: string;
  notes?: string;
}

export interface ExpenseUpdate {
  title?: string;
  amount?: number;
  category?: string;
  date?: string;
  payment_method?: string;
  notes?: string;
}

export interface ExpenseListResponse {
  expenses: Expense[];
  total_count: number;
  total_amount: number;
}

export interface CategorySummary {
  category: string;
  total_amount: number;
  expense_count: number;
}

export interface MonthlySummary {
  year: number;
  month: number;
  total_amount: number;
  expense_count: number;
}

// ==================== INVESTMENT TYPES ====================

export type AssetType = "Stock" | "MutualFund" | "FD" | "Gold" | "Crypto" | "Bond" | "Other";

export interface Investment {
  id: string;
  user_id: string;
  asset_type: AssetType;
  asset_name: string;
  symbol: string | null;
  quantity: number;
  purchase_price: number;
  current_price: number;
  purchase_date: string;
  maturity_date: string | null;
  platform: string | null;
  interest_rate: number | null;
  notes: string | null;
  created_at: string;
  updated_at: string | null;
  // Calculated fields
  invested_amount: number;
  current_value: number;
  absolute_gain: number;
  percentage_gain: number;
  days_held: number;
  is_matured: boolean;
}

export interface InvestmentCreate {
  asset_type: AssetType;
  asset_name: string;
  symbol?: string;
  quantity: number;
  purchase_price: number;
  current_price: number;
  purchase_date: string;
  maturity_date?: string;
  platform?: string;
  interest_rate?: number;
  notes?: string;
}

export interface InvestmentUpdate {
  asset_type?: AssetType;
  asset_name?: string;
  symbol?: string;
  quantity?: number;
  purchase_price?: number;
  current_price?: number;
  purchase_date?: string;
  maturity_date?: string;
  platform?: string;
  interest_rate?: number;
  notes?: string;
}

export interface AssetAllocation {
  asset_type: AssetType;
  value: number;
  percentage: number;
}

export interface PortfolioSummary {
  total_invested: number;
  total_current_value: number;
  total_gain_loss: number;
  total_gain_loss_percentage: number;
  total_investments: number;
  asset_type_breakdown: {
    asset_type: AssetType;
    count: number;
    invested: number;
    current_value: number;
    gain_loss: number;
    percentage_of_portfolio: number;
  }[];
}

export interface InvestmentListResponse {
  investments: Investment[];
  total_count: number;
  portfolio_summary: PortfolioSummary;
}

// ==================== DASHBOARD TYPES ====================

export interface DashboardData {
  summary: {
    net_worth: number;
    total_invested: number;
    investment_gains: number;
    investment_gains_percentage: number;
    current_month_expenses: number;
    last_month_expenses: number;
    expense_change_percentage: number;
    total_investments: number;
    total_expenses_count: number;
  };
  expenses: {
    current_month_total: number;
    current_month_count: number;
    all_time_total: number;
    all_time_count: number;
    top_categories: CategorySummary[];
  };
  investments: {
    portfolio_value: number;
    total_invested: number;
    total_gains: number;
    gains_percentage: number;
    asset_allocation: AssetAllocation[];
    top_performers: {
      id: string;
      asset_name: string;
      asset_type: AssetType;
      percentage_gain: number;
      absolute_gain: number;
      current_value: number;
    }[];
  };
  month_overview: {
    current_month: string;
    days_in_month: number;
    average_daily_expense: number;
  };
}

export interface HealthScore {
  score: number;
  rating: string;
  color: string;
  issues: string[];
  recommendations: string[];
}

// ==================== API ERROR TYPE ====================

export interface ApiError {
  detail: string;
  errors?: {
    loc: string[];
    msg: string;
    type: string;
  }[];
}
