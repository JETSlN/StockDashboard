/**
 * Price API Service
 * Service functions for price-related API endpoints
 */

import { apiRequest, API_ENDPOINTS, buildQueryString } from './config';
import type { 
  PriceHistory, 
  PriceHistoryParams, 
  PriceSummaryResponse 
} from '../types/fund';

/**
 * Get price history for an ETF
 * Corresponds to: GET /api/funds/{symbol_or_id}/prices
 * 
 * @param symbolOrId - ETF symbol (e.g., 'SPY') or ETF ID (e.g., 1)
 * @param params - Optional date range parameters
 */
export async function getPriceHistory(
  symbolOrId: string | number, 
  params?: PriceHistoryParams
): Promise<PriceHistory[]> {
  const queryString = params ? buildQueryString(params) : '';
  const endpoint = `${API_ENDPOINTS.PRICE_HISTORY(symbolOrId)}${queryString}`;
  
  return apiRequest<PriceHistory[]>(endpoint);
}

/**
 * Get the most recent price data for an ETF
 * Corresponds to: GET /api/funds/{symbol_or_id}/prices/latest
 * 
 * @param symbolOrId - ETF symbol (e.g., 'SPY') or ETF ID (e.g., 1)
 */
export async function getLatestPrice(symbolOrId: string | number): Promise<PriceHistory> {
  return apiRequest<PriceHistory>(API_ENDPOINTS.LATEST_PRICE(symbolOrId));
}

/**
 * Get price summary including latest price and recent history
 * Corresponds to: GET /api/funds/{symbol_or_id}/prices/summary
 * 
 * @param symbolOrId - ETF symbol (e.g., 'SPY') or ETF ID (e.g., 1)
 */
export async function getPriceSummary(symbolOrId: string | number): Promise<PriceSummaryResponse> {
  return apiRequest<PriceSummaryResponse>(API_ENDPOINTS.PRICE_SUMMARY(symbolOrId));
}

// Convenience functions for common date ranges

/**
 * Get price history for the last N days
 */
export async function getPriceHistoryLastDays(
  symbolOrId: string | number, 
  days: number
): Promise<PriceHistory[]> {
  const endDate = new Date();
  const startDate = new Date();
  startDate.setDate(endDate.getDate() - days);
  
  return getPriceHistory(symbolOrId, {
    start: startDate.toISOString().split('T')[0], // YYYY-MM-DD format
    end: endDate.toISOString().split('T')[0]
  });
}

/**
 * Get price history for the last month (30 days)
 */
export async function getPriceHistoryLastMonth(symbolOrId: string | number): Promise<PriceHistory[]> {
  return getPriceHistoryLastDays(symbolOrId, 30);
}

/**
 * Get price history for the last quarter (90 days)
 */
export async function getPriceHistoryLastQuarter(symbolOrId: string | number): Promise<PriceHistory[]> {
  return getPriceHistoryLastDays(symbolOrId, 90);
}

/**
 * Get price history for the last year (365 days)
 */
export async function getPriceHistoryLastYear(symbolOrId: string | number): Promise<PriceHistory[]> {
  return getPriceHistoryLastDays(symbolOrId, 365);
}

/**
 * Get price history for year-to-date
 */
export async function getPriceHistoryYTD(symbolOrId: string | number): Promise<PriceHistory[]> {
  const now = new Date();
  const startOfYear = new Date(now.getFullYear(), 0, 1); // January 1st of current year
  
  return getPriceHistory(symbolOrId, {
    start: startOfYear.toISOString().split('T')[0],
    end: now.toISOString().split('T')[0]
  });
}

/**
 * Get price history for a specific date range
 */
export async function getPriceHistoryDateRange(
  symbolOrId: string | number,
  startDate: string, // YYYY-MM-DD format
  endDate: string    // YYYY-MM-DD format
): Promise<PriceHistory[]> {
  return getPriceHistory(symbolOrId, {
    start: startDate,
    end: endDate
  });
}

// Utility functions for price calculations

/**
 * Calculate price change and percentage change from price history
 */
export function calculatePriceChange(priceHistory: PriceHistory[]): {
  priceChange: number;
  priceChangePercent: number;
  currentPrice: number;
  previousPrice: number;
} | null {
  if (priceHistory.length < 2) {
    return null;
  }
  
  // Assuming price history is sorted by date ascending
  const currentPrice = priceHistory[priceHistory.length - 1].close_price;
  const previousPrice = priceHistory[priceHistory.length - 2].close_price;
  
  const priceChange = currentPrice - previousPrice;
  const priceChangePercent = (priceChange / previousPrice) * 100;
  
  return {
    priceChange,
    priceChangePercent,
    currentPrice,
    previousPrice
  };
}

/**
 * Calculate total return from price history
 */
export function calculateTotalReturn(priceHistory: PriceHistory[]): {
  totalReturn: number;
  totalReturnPercent: number;
  startPrice: number;
  endPrice: number;
} | null {
  if (priceHistory.length < 2) {
    return null;
  }
  
  const startPrice = priceHistory[0].close_price;
  const endPrice = priceHistory[priceHistory.length - 1].close_price;
  
  const totalReturn = endPrice - startPrice;
  const totalReturnPercent = (totalReturn / startPrice) * 100;
  
  return {
    totalReturn,
    totalReturnPercent,
    startPrice,
    endPrice
  };
}

/**
 * Find the highest and lowest prices in price history
 */
export function findPriceExtremes(priceHistory: PriceHistory[]): {
  highPrice: number;
  lowPrice: number;
  highDate: string;
  lowDate: string;
} | null {
  if (priceHistory.length === 0) {
    return null;
  }
  
  let highPrice = priceHistory[0].close_price;
  let lowPrice = priceHistory[0].close_price;
  let highDate = priceHistory[0].date;
  let lowDate = priceHistory[0].date;
  
  for (const price of priceHistory) {
    if (price.close_price > highPrice) {
      highPrice = price.close_price;
      highDate = price.date;
    }
    if (price.close_price < lowPrice) {
      lowPrice = price.close_price;
      lowDate = price.date;
    }
  }
  
  return {
    highPrice,
    lowPrice,
    highDate,
    lowDate
  };
}
