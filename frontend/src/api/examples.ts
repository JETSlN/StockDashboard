/**
 * API Usage Examples
 * This file demonstrates how to use the API functions in your components
 */

import {
  listETFs,
  getETF,
  getFundSummary,
  getPriceHistory,
  getLatestPrice,
  getPriceHistoryLastMonth,
  calculatePriceChange,
  APIError
} from './index';

// Example 1: List all ETFs
export async function exampleListETFs() {
  try {
    const etfs = await listETFs();
    console.log('All ETFs:', etfs);
    return etfs;
  } catch (error) {
    if (error instanceof APIError) {
      console.error('API Error:', error.message, 'Status:', error.status);
    } else {
      console.error('Unexpected error:', error);
    }
    throw error;
  }
}

// Example 2: Get specific ETF details
export async function exampleGetETFDetails(symbol: string) {
  try {
    const etf = await getETF(symbol);
    console.log(`ETF Details for ${symbol}:`, etf);
    return etf;
  } catch (error) {
    if (error instanceof APIError) {
      if (error.status === 404) {
        console.error(`ETF ${symbol} not found`);
      } else {
        console.error('API Error:', error.message);
      }
    }
    throw error;
  }
}

// Example 3: Get fund summary with holdings and sectors
export async function exampleGetFundSummary(symbol: string) {
  try {
    const summary = await getFundSummary(symbol);
    console.log(`Fund Summary for ${symbol}:`, {
      fund: summary.fund.name,
      topHoldings: summary.top_holdings.length,
      topSectors: summary.top_sectors.length
    });
    return summary;
  } catch (error) {
    console.error('Error fetching fund summary:', error);
    throw error;
  }
}

// Example 4: Get price history and calculate performance
export async function exampleGetPricePerformance(symbol: string) {
  try {
    // Get last month's price history
    const priceHistory = await getPriceHistoryLastMonth(symbol);
    
    // Calculate price change
    const priceChange = calculatePriceChange(priceHistory);
    
    if (priceChange) {
      console.log(`Price Performance for ${symbol}:`, {
        currentPrice: priceChange.currentPrice.toFixed(2),
        priceChange: priceChange.priceChange.toFixed(2),
        priceChangePercent: priceChange.priceChangePercent.toFixed(2) + '%'
      });
    }
    
    return { priceHistory, priceChange };
  } catch (error) {
    console.error('Error fetching price performance:', error);
    throw error;
  }
}

// Example 5: Get latest price for quick display
export async function exampleGetLatestPrice(symbol: string) {
  try {
    const latestPrice = await getLatestPrice(symbol);
    console.log(`Latest price for ${symbol}:`, {
      price: latestPrice.close_price,
      date: latestPrice.date
    });
    return latestPrice;
  } catch (error) {
    console.error('Error fetching latest price:', error);
    throw error;
  }
}

// Example 6: Search ETFs by name or symbol
export async function exampleSearchETFs(query: string) {
  try {
    // Note: This uses client-side filtering. For large datasets,
    // you might want to implement server-side search
    const allETFs = await listETFs();
    const searchResults = allETFs.filter(etf => 
      etf.symbol.toLowerCase().includes(query.toLowerCase()) ||
      etf.name.toLowerCase().includes(query.toLowerCase())
    );
    
    console.log(`Search results for "${query}":`, searchResults.length, 'funds found');
    return searchResults;
  } catch (error) {
    console.error('Error searching ETFs:', error);
    throw error;
  }
}

// Example 7: React Hook pattern for using API functions
export function useETFData(symbol: string) {
  // This is a conceptual example - you'd typically use React Query, SWR, or similar
  // for actual data fetching in React components
  
  const fetchETFData = async () => {
    try {
      const [etf, summary, priceHistory] = await Promise.all([
        getETF(symbol),
        getFundSummary(symbol),
        getPriceHistoryLastMonth(symbol)
      ]);
      
      return {
        etf,
        summary,
        priceHistory,
        priceChange: calculatePriceChange(priceHistory)
      };
    } catch (error) {
      console.error(`Error fetching data for ${symbol}:`, error);
      throw error;
    }
  };
  
  return { fetchETFData };
}
