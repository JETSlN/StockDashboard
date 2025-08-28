/**
 * API Module Index
 * Central export point for all API functions and types
 */

// Export API configuration
export { API_BASE_URL, API_ENDPOINTS, APIError } from './config';

// Export fund service functions
export {
  listETFs,
  getETF,
  getFundSummary,
  getFundHoldings,
  getFundSectorAllocations,
  getFundWithTopHoldings,
  getFundWithSectors,
  searchETFs
} from './fundService';

// Export price service functions
export {
  getPriceHistory,
  getLatestPrice,
  getPriceSummary,
  getPriceHistoryLastDays,
  getPriceHistoryLastMonth,
  getPriceHistoryLastQuarter,
  getPriceHistoryLastYear,
  getPriceHistoryYTD,
  getPriceHistoryDateRange,
  calculatePriceChange,
  calculateTotalReturn,
  findPriceExtremes
} from './priceService';

// Re-export types for convenience
export type {
  ETF,
  PriceHistory,
  Holding,
  SectorAllocation,
  FundOperations,
  EquityMetrics,
  FundOverview,
  FundSummaryResponse,
  PriceSummaryResponse,
  PriceHistoryParams,
  APIError as APIErrorType
} from '../types/fund';
