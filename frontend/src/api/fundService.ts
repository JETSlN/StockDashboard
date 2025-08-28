/**
 * Fund API Service
 * Service functions for fund-related API endpoints
 */

import { apiRequest, API_ENDPOINTS } from './config';
import type { 
  ETF, 
  Holding, 
  SectorAllocation, 
  FundSummaryResponse 
} from '../types/fund';

/**
 * Get list of all ETFs with key information for listings/selection
 * Corresponds to: GET /api/funds/
 */
export async function listETFs(): Promise<ETF[]> {
  return apiRequest<ETF[]>(API_ENDPOINTS.FUNDS);
}

/**
 * Get detailed fund information including relationships
 * Corresponds to: GET /api/funds/{symbol_or_id}
 * 
 * @param symbolOrId - ETF symbol (e.g., 'SPY') or ETF ID (e.g., 1)
 */
export async function getETF(symbolOrId: string | number): Promise<ETF> {
  return apiRequest<ETF>(API_ENDPOINTS.FUND_DETAIL(symbolOrId));
}

/**
 * Get fund summary with basic info, top holdings, and top sectors
 * Corresponds to: GET /api/funds/{symbol_or_id}/summary
 * 
 * @param symbolOrId - ETF symbol (e.g., 'SPY') or ETF ID (e.g., 1)
 */
export async function getFundSummary(symbolOrId: string | number): Promise<FundSummaryResponse> {
  return apiRequest<FundSummaryResponse>(API_ENDPOINTS.FUND_SUMMARY(symbolOrId));
}

/**
 * Get all holdings for an ETF
 * Corresponds to: GET /api/funds/{symbol_or_id}/holdings
 * 
 * @param symbolOrId - ETF symbol (e.g., 'SPY') or ETF ID (e.g., 1)
 */
export async function getFundHoldings(symbolOrId: string | number): Promise<Holding[]> {
  return apiRequest<Holding[]>(API_ENDPOINTS.FUND_HOLDINGS(symbolOrId));
}

/**
 * Get all sector allocations for an ETF
 * Corresponds to: GET /api/funds/{symbol_or_id}/sectors
 * 
 * @param symbolOrId - ETF symbol (e.g., 'SPY') or ETF ID (e.g., 1)
 */
export async function getFundSectorAllocations(symbolOrId: string | number): Promise<SectorAllocation[]> {
  return apiRequest<SectorAllocation[]>(API_ENDPOINTS.FUND_SECTORS(symbolOrId));
}

// Convenience functions for common use cases

/**
 * Get fund with its top holdings (first 10)
 */
export async function getFundWithTopHoldings(symbolOrId: string | number): Promise<{
  fund: ETF;
  holdings: Holding[];
}> {
  const [fund, holdings] = await Promise.all([
    getETF(symbolOrId),
    getFundHoldings(symbolOrId)
  ]);
  
  return {
    fund,
    holdings: holdings.slice(0, 10) // Top 10 holdings
  };
}

/**
 * Get fund with its sector allocations
 */
export async function getFundWithSectors(symbolOrId: string | number): Promise<{
  fund: ETF;
  sectors: SectorAllocation[];
}> {
  const [fund, sectors] = await Promise.all([
    getETF(symbolOrId),
    getFundSectorAllocations(symbolOrId)
  ]);
  
  return {
    fund,
    sectors
  };
}

/**
 * Search ETFs by symbol or name (client-side filtering)
 * For more sophisticated search, you might want to implement server-side search
 */
export async function searchETFs(query: string): Promise<ETF[]> {
  const allFunds = await listETFs();
  const searchQuery = query.toLowerCase().trim();
  
  if (!searchQuery) {
    return allFunds;
  }
  
  return allFunds.filter(fund => 
    fund.symbol.toLowerCase().includes(searchQuery) ||
    fund.name.toLowerCase().includes(searchQuery) ||
    (fund.short_name && fund.short_name.toLowerCase().includes(searchQuery))
  );
}
