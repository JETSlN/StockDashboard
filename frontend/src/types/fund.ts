/**
 * TypeScript types for ETF/Fund data structures
 * Based on backend models and API responses
 */

// Base ETF/Fund interface matching the backend ETF model
export interface ETF {
  id: number;
  symbol: string;
  name: string;
  
  // Basic Info
  category?: string;
  family?: string;
  exchange?: string;
  full_exchange_name?: string;
  currency?: string;
  country?: string;
  legal_type?: string;
  
  // Financial Metrics
  net_assets?: number;
  nav?: number;
  expense_ratio?: number;
  yield_rate?: number;
  pe_ratio?: number;
  pb_ratio?: number;
  beta?: number;
  
  // Performance Metrics
  ytd_return?: number;
  three_year_return?: number;
  five_year_return?: number;
  trailing_three_month_returns?: number;
  
  // Inception and Management
  inception_date?: string;
  fund_inception_date?: string;
  
  // Additional Info
  website?: string;
  summary?: string;
  long_name?: string;
  short_name?: string;
  
  // Technical Indicators
  fifty_day_average?: number;
  two_hundred_day_average?: number;
  fifty_two_week_high?: number;
  fifty_two_week_low?: number;
  
  // Volume and Trading
  average_volume?: number;
  average_volume_10days?: number;
  average_daily_volume_3month?: number;
  shares_outstanding?: number;
  market_cap?: number;
  
  // Current Trading Data
  current_price?: number;
  day_high?: number;
  day_low?: number;
  previous_close?: number;
  
  // Dividend Information
  trailing_annual_dividend_rate?: number;
  trailing_annual_dividend_yield?: number;
  
  // Market Data Fields
  open_price?: number;
  regular_market_open?: number;
  regular_market_day_low?: number;
  regular_market_day_high?: number;
  regular_market_previous_close?: number;
  regular_market_price?: number;
  regular_market_volume?: number;
  regular_market_change?: number;
  regular_market_change_percent?: number;
  regular_market_day_range?: string;
  
  // Bid/Ask Data
  bid?: number;
  ask?: number;
  bid_size?: number;
  ask_size?: number;
  
  // Post Market Data
  post_market_price?: number;
  post_market_change?: number;
  post_market_change_percent?: number;
  
  // Additional Volume Data
  volume?: number;
  average_daily_volume_10day?: number;
  
  // 52-Week Performance Calculations
  fifty_two_week_change_percent?: number;
  fifty_two_week_low_change?: number;
  fifty_two_week_low_change_percent?: number;
  fifty_two_week_high_change?: number;
  fifty_two_week_high_change_percent?: number;
  fifty_two_week_range?: string;
  
  // Technical Indicators

  fifty_day_average_change?: number;
  fifty_day_average_change_percent?: number;
  two_hundred_day_average_change?: number;
  two_hundred_day_average_change_percent?: number;
  

  
  // Additional Fund Data
  book_value?: number;
  dividend_yield?: number;
  trailing_three_month_nav_returns?: number;
  eps_trailing_twelve_months?: number;
  trailing_peg_ratio?: number;
  total_assets?: number;
  net_expense_ratio?: number;
  price_to_book?: number;
  
  // Market Metadata
  quote_type?: string;
  market?: string;
  exchange_timezone_name?: string;
  exchange_timezone_short_name?: string;
  gmt_offset_milliseconds?: number;
  market_state?: string;
  language?: string;
  region?: string;
  type_disp?: string;
  quote_source_name?: string;
  
  // Trading Metadata
  tradeable?: boolean;
  crypto_tradeable?: boolean;
  has_pre_post_market_data?: boolean;
  triggerable?: boolean;
  esg_populated?: boolean;
  
  // Technical Data
  price_hint?: number;
  source_interval?: number;
  exchange_data_delayed_by?: number;
  max_age?: number;
  
  // Timestamps
  first_trade_date_milliseconds?: number;
  regular_market_time?: number;
  post_market_time?: number;
  
  // Additional Identifiers
  message_board_id?: string;
  financial_currency?: string;
  
  // Confidence and Alert Data
  custom_price_alert_confidence?: string;
  
  // Metadata
  created_at?: string;
  updated_at?: string;
  last_data_update?: string;
  
  // Nested relationships (optional, loaded separately)
  fund_operations?: FundOperations;
  equity_metrics?: EquityMetrics;
  fund_overview?: FundOverview;
}

// Price history data structure
export interface PriceHistory {
  id: number;
  etf_id: number;
  date: string;
  open_price?: number;
  high_price?: number;
  low_price?: number;
  close_price: number;
  adjusted_close?: number;
  volume?: number;
  daily_return?: number;
  cumulative_return?: number;
  created_at?: string;
}

// Holdings data structure
export interface Holding {
  id: number;
  etf_id: number;
  symbol?: string;
  name?: string;
  weight?: number;
  shares?: number;
  market_value?: number;
  sector?: string;
  industry?: string;
  country?: string;
  region?: string;
  asset_class?: string;
  security_type?: string;
  as_of_date?: string;
  created_at?: string;
  updated_at?: string;
}

// Sector allocation data structure
export interface SectorAllocation {
  id: number;
  etf_id: number;
  sector_name: string;
  allocation_percentage: number;
  as_of_date?: string;
  created_at?: string;
}

// Fund operations data structure
export interface FundOperations {
  id: number;
  etf_id: number;
  annual_report_expense_ratio?: number;
  annual_holdings_turnover?: number;
  total_net_assets?: number;
  category_average_expense_ratio?: number;
  category_average_turnover?: number;
  as_of_date?: string;
  created_at?: string;
  updated_at?: string;
}

// Equity metrics data structure
export interface EquityMetrics {
  id: number;
  etf_id: number;
  fund_price_earnings?: number;
  fund_price_book?: number;
  fund_price_sales?: number;
  fund_price_cashflow?: number;
  fund_median_market_cap?: number;
  fund_geometric_mean_market_cap?: number;
  category_price_earnings?: number;
  category_price_book?: number;
  category_price_sales?: number;
  as_of_date?: string;
  created_at?: string;
  updated_at?: string;
}

// Fund overview data structure
export interface FundOverview {
  id: number;
  etf_id: number;
  category_name?: string;
  family?: string;
  legal_type?: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

// API Response types (what the controllers actually return)

// Fund summary response (from /api/funds/{id}/summary)
export interface FundSummaryResponse {
  fund: ETF;
  top_holdings: Holding[];
  top_sectors: SectorAllocation[];
  total_holdings: number;
  total_sectors: number;
}

// Price summary response (from /api/funds/{id}/prices/summary)
export interface PriceSummaryResponse {
  fund_symbol: string;
  fund_name: string;
  latest_price?: PriceHistory;
  price_statistics: {
    total_records: number;
    price_range: {
      min: number;
      max: number;
    };
    date_range: {
      start: string;
      end: string;
    };
  };
  recent_history: PriceHistory[];
}

// Query parameters for price history
export interface PriceHistoryParams {
  start?: string; // YYYY-MM-DD format
  end?: string;   // YYYY-MM-DD format
}

// Error response type
export interface APIError {
  detail: string;
}