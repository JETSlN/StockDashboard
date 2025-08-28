import { useState, useEffect } from 'react';
import { Activity, Target, Loader2, AlertCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';


// Import API functions and types
import {
  getETF,
  getFundSummary,
  getFundHoldings,
  getPriceHistoryLastMonth,
  getPriceHistoryLastQuarter,
  getPriceHistoryYTD,
  getPriceHistoryLastYear,
  getPriceHistoryDateRange,
  APIError
} from '@/api';
import { listETFs } from '@/api/fundService';
import type { ETF, PriceHistory, FundSummaryResponse, Holding } from '@/types';

// Import components
import ETFCard from '@/components/ETFCard';
import PerformanceChart from '@/components/PerformanceChart';
import FundTabs from '@/components/FundTabs';
import KeyMetrics from '@/components/KeyMetrics';
import HoldingsChart from '@/components/HoldingsChart';
import SectorChart from '@/components/SectorChart';
import DetailedPerformance from '@/components/DetailedPerformance';

// Types for chart data
interface ChartDataPoint {
  date: string;
  fundPercent: number;
  fundPrice: number;
}

interface LoadingState {
  funds: [boolean, boolean, boolean];
  summaries: [boolean, boolean, boolean];
  holdings: [boolean, boolean, boolean];
  priceHistory: [boolean, boolean, boolean];
  etfs: boolean;
}

interface ErrorState {
  funds: [string | null, string | null, string | null];
  summaries: [string | null, string | null, string | null];
  holdings: [string | null, string | null, string | null];
  priceHistory: [string | null, string | null, string | null];
  etfs: string | null;
}

// Helper function to transform price history to chart data
const transformPriceHistoryToChartData = (
  priceHistory: PriceHistory[], 
  period: '1M' | '3M' | 'YTD' | '1Y' | '3Y' | '5Y'
): ChartDataPoint[] => {
  if (!priceHistory || priceHistory.length === 0) return [];
  
  const startPrice = priceHistory[0].close_price;
  
  // Sample data points for better performance and readability
  let sampledData = priceHistory;
  const maxDataPoints = 50; // Maximum number of data points to show
  
  if (priceHistory.length > maxDataPoints) {
    const step = Math.floor(priceHistory.length / maxDataPoints);
    sampledData = priceHistory.filter((_, index) => index % step === 0);
    // Always include the last data point
    if (sampledData[sampledData.length - 1] !== priceHistory[priceHistory.length - 1]) {
      sampledData.push(priceHistory[priceHistory.length - 1]);
    }
  }
  
  return sampledData.map((price) => {
    const fundPercent = (price.close_price / startPrice) * 100;
    const priceDate = new Date(price.date);
    
    // Format date based on time period
    let formattedDate: string;
    
    switch (period) {
      case '1M':
      case '3M':
        // For 1-3 months: Show "Dec 15" format
        formattedDate = priceDate.toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric' 
        });
        break;
        
      case 'YTD':
      case '1Y':
        // For 1 year/YTD: Show "Dec" format (month only)
        formattedDate = priceDate.toLocaleDateString('en-US', { 
          month: 'short'
        });
        break;
        
      case '3Y':
        // For 3 years: Show "Dec 2024" format (month and year)
        formattedDate = priceDate.toLocaleDateString('en-US', { 
          month: 'short',
          year: 'numeric'
        });
        break;
        
      case '5Y':
        // For 5 years: Show only year "2024"
        formattedDate = priceDate.getFullYear().toString();
        break;
        
      default:
        formattedDate = priceDate.toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric' 
        });
    }
    
    return {
      date: formattedDate,
      fundPercent,
      fundPrice: price.close_price
    };
  });
};

export default function MainDashboard() {
  // UI State
  const [holdingsChartType, setHoldingsChartType] = useState<'bar' | 'pie'>('bar');
  const [sectorChartType, setSectorChartType] = useState<'bar' | 'pie'>('bar');
  const [selectedPeriod, setSelectedPeriod] = useState<'1M' | '3M' | 'YTD' | '1Y' | '3Y' | '5Y'>('YTD');
  const [chartValueType, setChartValueType] = useState<'percentage' | 'price'>('percentage');
  const [selectedFunds, setSelectedFunds] = useState<[string | null, string | null, string | null]>([null, null, null]);
  const [activeFundTab, setActiveFundTab] = useState<number>(0); // For switching between fund metrics
  
  // Data State
  const [fundData, setFundData] = useState<[ETF | null, ETF | null, ETF | null]>([null, null, null]);
  const [summaryData, setSummaryData] = useState<[FundSummaryResponse | null, FundSummaryResponse | null, FundSummaryResponse | null]>([null, null, null]);
  const [holdingsData, setHoldingsData] = useState<[Holding[], Holding[], Holding[]]>([[], [], []]);
  const [chartData, setChartData] = useState<[ChartDataPoint[], ChartDataPoint[], ChartDataPoint[]]>([[], [], []]);
  const [etfsList, setEtfsList] = useState<ETF[]>([]);
  
  // Loading State
  const [loading, setLoading] = useState<LoadingState>({
    funds: [false, false, false],
    summaries: [false, false, false],
    holdings: [false, false, false],
    priceHistory: [false, false, false],
    etfs: true
  });
  
  // Error State
  const [errors, setErrors] = useState<ErrorState>({
    funds: [null, null, null],
    summaries: [null, null, null],
    holdings: [null, null, null],
    priceHistory: [null, null, null],
    etfs: null
  });

  // API Data Fetching Functions
  const fetchFundData = async (symbol: string, fundIndex: number) => {
    setLoading(prev => ({
      ...prev,
      funds: prev.funds.map((loading, index) => index === fundIndex ? true : loading) as [boolean, boolean, boolean]
    }));
    setErrors(prev => ({
      ...prev,
      funds: prev.funds.map((error, index) => index === fundIndex ? null : error) as [string | null, string | null, string | null]
    }));
    
    try {
      const data = await getETF(symbol);
      setFundData(prev => {
        const newData = [...prev] as [ETF | null, ETF | null, ETF | null];
        newData[fundIndex] = data;
        return newData;
      });
    } catch (error) {
      const errorMessage = error instanceof APIError ? error.message : 'Failed to fetch fund data';
      setErrors(prev => ({
        ...prev,
        funds: prev.funds.map((err, index) => index === fundIndex ? errorMessage : err) as [string | null, string | null, string | null]
      }));
    } finally {
      setLoading(prev => ({
        ...prev,
        funds: prev.funds.map((loading, index) => index === fundIndex ? false : loading) as [boolean, boolean, boolean]
      }));
    }
  };

  const fetchSummaryData = async (symbol: string, fundIndex: number) => {
    setLoading(prev => ({
      ...prev,
      summaries: prev.summaries.map((loading, index) => index === fundIndex ? true : loading) as [boolean, boolean, boolean]
    }));
    setErrors(prev => ({
      ...prev,
      summaries: prev.summaries.map((error, index) => index === fundIndex ? null : error) as [string | null, string | null, string | null]
    }));
    
    try {
      const data = await getFundSummary(symbol);
      setSummaryData(prev => {
        const newData = [...prev] as [FundSummaryResponse | null, FundSummaryResponse | null, FundSummaryResponse | null];
        newData[fundIndex] = data;
        return newData;
      });
    } catch (error) {
      const errorMessage = error instanceof APIError ? error.message : 'Failed to fetch summary data';
      setErrors(prev => ({
        ...prev,
        summaries: prev.summaries.map((err, index) => index === fundIndex ? errorMessage : err) as [string | null, string | null, string | null]
      }));
    } finally {
      setLoading(prev => ({
        ...prev,
        summaries: prev.summaries.map((loading, index) => index === fundIndex ? false : loading) as [boolean, boolean, boolean]
      }));
    }
  };

  const fetchHoldingsData = async (symbol: string, fundIndex: number) => {
    setLoading(prev => ({
      ...prev,
      holdings: prev.holdings.map((loading, index) => index === fundIndex ? true : loading) as [boolean, boolean, boolean]
    }));
    setErrors(prev => ({
      ...prev,
      holdings: prev.holdings.map((error, index) => index === fundIndex ? null : error) as [string | null, string | null, string | null]
    }));
    
    try {
      const data = await getFundHoldings(symbol);
      // Get top 10 holdings
      setHoldingsData(prev => {
        const newData = [...prev] as [Holding[], Holding[], Holding[]];
        newData[fundIndex] = data.slice(0, 10);
        return newData;
      });
    } catch (error) {
      const errorMessage = error instanceof APIError ? error.message : 'Failed to fetch holdings data';
      setErrors(prev => ({
        ...prev,
        holdings: prev.holdings.map((err, index) => index === fundIndex ? errorMessage : err) as [string | null, string | null, string | null]
      }));
    } finally {
      setLoading(prev => ({
        ...prev,
        holdings: prev.holdings.map((loading, index) => index === fundIndex ? false : loading) as [boolean, boolean, boolean]
      }));
    }
  };

  const fetchPriceHistory = async (symbol: string, period: '1M' | '3M' | 'YTD' | '1Y' | '3Y' | '5Y', fundIndex: number) => {
    setLoading(prev => ({
      ...prev,
      priceHistory: prev.priceHistory.map((loading, index) => index === fundIndex ? true : loading) as [boolean, boolean, boolean]
    }));
    setErrors(prev => ({
      ...prev,
      priceHistory: prev.priceHistory.map((error, index) => index === fundIndex ? null : error) as [string | null, string | null, string | null]
    }));
    
    try {
      let data: PriceHistory[];
      
      switch (period) {
        case '1M':
          data = await getPriceHistoryLastMonth(symbol);
          break;
        case '3M':
          data = await getPriceHistoryLastQuarter(symbol);
          break;
        case 'YTD':
          data = await getPriceHistoryYTD(symbol);
          break;
        case '1Y':
          data = await getPriceHistoryLastYear(symbol);
          break;
        case '3Y':
          // Get 3 years of data
          const threeYearsAgo = new Date();
          threeYearsAgo.setFullYear(threeYearsAgo.getFullYear() - 3);
          data = await getPriceHistoryDateRange(
            symbol, 
            threeYearsAgo.toISOString().split('T')[0],
            new Date().toISOString().split('T')[0]
          );
          break;
        case '5Y':
          // Get 5 years of data
          const fiveYearsAgo = new Date();
          fiveYearsAgo.setFullYear(fiveYearsAgo.getFullYear() - 5);
          data = await getPriceHistoryDateRange(
            symbol, 
            fiveYearsAgo.toISOString().split('T')[0],
            new Date().toISOString().split('T')[0]
          );
          break;
        default:
          data = await getPriceHistoryYTD(symbol);
      }
      
      setChartData(prev => {
        const newData = [...prev] as [ChartDataPoint[], ChartDataPoint[], ChartDataPoint[]];
        newData[fundIndex] = transformPriceHistoryToChartData(data, period);
        return newData;
      });
    } catch (error) {
      const errorMessage = error instanceof APIError ? error.message : 'Failed to fetch price history';
      setErrors(prev => ({
        ...prev,
        priceHistory: prev.priceHistory.map((err, index) => index === fundIndex ? errorMessage : err) as [string | null, string | null, string | null]
      }));
    } finally {
      setLoading(prev => ({
        ...prev,
        priceHistory: prev.priceHistory.map((loading, index) => index === fundIndex ? false : loading) as [boolean, boolean, boolean]
      }));
    }
  };

  const fetchETFs = async () => {
    setLoading(prev => ({ ...prev, etfs: true }));
    setErrors(prev => ({ ...prev, etfs: null }));

    try {
      const data = await listETFs();
      setEtfsList(data);

      // Set default selected symbol to the first ETF if none is selected
      if (data.length > 0 && !selectedFunds[0]) {
        setSelectedFunds([data[0].symbol, null, null]);
      }
    } catch (error) {
      const errorMessage = error instanceof APIError ? error.message : 'Failed to fetch ETFs list';
      setErrors(prev => ({ ...prev, etfs: errorMessage }));
    } finally {
      setLoading(prev => ({ ...prev, etfs: false }));
    }
  };

  // Helper functions for managing selected funds
  const getSelectedFunds = () => selectedFunds.filter(fund => fund !== null) as string[];
  const getActiveFundData = (fundIndex: number = activeFundTab) => {
    const activeFunds = getSelectedFunds();
    if (activeFunds.length === 0 || fundIndex >= activeFunds.length) return null;
    const symbol = activeFunds[fundIndex];
    const actualIndex = selectedFunds.indexOf(symbol);
    return {
      fund: fundData[actualIndex],
      summary: summaryData[actualIndex],
      holdings: holdingsData[actualIndex],
      chart: chartData[actualIndex],
      loading: {
        fund: loading.funds[actualIndex],
        summary: loading.summaries[actualIndex],
        holdings: loading.holdings[actualIndex],
        priceHistory: loading.priceHistory[actualIndex]
      },
      errors: {
        fund: errors.funds[actualIndex],
        summary: errors.summaries[actualIndex],
        holdings: errors.holdings[actualIndex],
        priceHistory: errors.priceHistory[actualIndex]
      },
      symbol
    };
  };

  const updateSelectedFund = (fundIndex: number, symbol: string | null) => {
    setSelectedFunds(prev => {
      const newFunds = [...prev] as [string | null, string | null, string | null];
      newFunds[fundIndex] = symbol;
      return newFunds;
    });
  };

  const fetchAllDataForFund = async (symbol: string, fundIndex: number) => {
    await Promise.all([
      fetchFundData(symbol, fundIndex),
      fetchSummaryData(symbol, fundIndex),
      fetchHoldingsData(symbol, fundIndex),
      fetchPriceHistory(symbol, selectedPeriod, fundIndex)
    ]);
  };

  // Effects
  useEffect(() => {
    // Fetch ETFs list on component mount
    fetchETFs();
  }, []);

  useEffect(() => {
    // Fetch data for each selected fund when selection changes
    selectedFunds.forEach((symbol, index) => {
      if (symbol) {
        fetchAllDataForFund(symbol, index);
      } else {
        // Clear data for this fund index
        setFundData(prev => {
          const newData = [...prev] as [ETF | null, ETF | null, ETF | null];
          newData[index] = null;
          return newData;
        });
        setSummaryData(prev => {
          const newData = [...prev] as [FundSummaryResponse | null, FundSummaryResponse | null, FundSummaryResponse | null];
          newData[index] = null;
          return newData;
        });
        setHoldingsData(prev => {
          const newData = [...prev] as [Holding[], Holding[], Holding[]];
          newData[index] = [];
          return newData;
        });
        setChartData(prev => {
          const newData = [...prev] as [ChartDataPoint[], ChartDataPoint[], ChartDataPoint[]];
          newData[index] = [];
          return newData;
        });
      }
    });
  }, [selectedFunds]);

  useEffect(() => {
    // Fetch price history for all selected funds when period changes
    selectedFunds.forEach((symbol, index) => {
      if (symbol) {
        fetchPriceHistory(symbol, selectedPeriod, index);
      }
    });
  }, [selectedPeriod]);

  useEffect(() => {
    // Update active tab if the current tab's fund is no longer selected
    const activeFunds = getSelectedFunds();
    if (activeFundTab >= activeFunds.length) {
      setActiveFundTab(Math.max(0, activeFunds.length - 1));
    }
  }, [selectedFunds, activeFundTab]);
  
  // Calculate combined chart data for comparison
  const getCombinedChartData = () => {
    const activeFunds = getSelectedFunds();
    if (activeFunds.length === 0) return [];
    
    // Get the chart data for active funds
    const activeChartData = activeFunds.map(symbol => {
      const index = selectedFunds.indexOf(symbol);
      return { symbol, data: chartData[index] };
    }).filter(item => item.data.length > 0);
    
    if (activeChartData.length === 0) return [];
    
    // Find common date range
    const minLength = Math.min(...activeChartData.map(item => item.data.length));
    if (minLength === 0) return [];
    
    // Create combined data points
    const combinedData = [];
    for (let i = 0; i < minLength; i++) {
      const dataPoint: any = {
        date: activeChartData[0].data[i].date
      };
      
      activeChartData.forEach(({ symbol, data }) => {
        if (i < data.length) {
          dataPoint[`${symbol}_percent`] = data[i].fundPercent;
          dataPoint[`${symbol}_price`] = data[i].fundPrice;
        }
      });
      
      combinedData.push(dataPoint);
    }
    
    return combinedData;
  };
  
  const combinedChartData = getCombinedChartData();
  
  // Calculate performance metrics for active fund
  const activeData = getActiveFundData();

  // Loading component
  const LoadingCard = ({ title }: { title: string }) => (
    <div className="flex-1 min-w-0 bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 border-0 shadow-md rounded-lg p-6">
      <div className="flex items-center justify-center space-x-2">
        <Loader2 className="h-4 w-4 animate-spin" />
        <span className="text-sm text-muted-foreground">Loading {title}...</span>
      </div>
    </div>
  );

  // Error component
  const ErrorCard = ({ title, error }: { title: string; error: string }) => (
    <div className="flex-1 min-w-0 bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 border-0 shadow-md rounded-lg p-6 border-red-200">
      <div className="flex items-center space-x-2 text-red-600">
        <AlertCircle className="h-4 w-4" />
        <span className="text-sm">Error loading {title}: {error}</span>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-muted/20">
        <div className="container mx-auto px-4 py-3">
          {/* Top Row - Title and Controls */}
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-foreground">ETF Comparison Dashboard</h1>
              <p className="text-sm text-muted-foreground">
                {getSelectedFunds().length === 0
                  ? 'Select ETFs to compare'
                  : `Comparing: ${getSelectedFunds().join(', ')}`
                }
              </p>
            </div>

            <div className="flex items-center space-x-2 flex-shrink-0">
              <Badge variant="outline" className="px-3 py-1">
                <Activity className="w-3 h-3 mr-1" />
                Live Data
              </Badge>

            </div>
          </div>

          {/* Bottom Row - ETF Selectors */}
          <div className="flex justify-center items-center gap-3">
            <div className="flex gap-3">
              {[0, 1, 2].map((index) => (
                <select
                  key={index}
                  value={selectedFunds[index] || ''}
                  onChange={(e) => updateSelectedFund(index, e.target.value || null)}
                  className="bg-background border border-input rounded-md px-3 py-2 text-sm min-w-[375px] max-w-[375px]"
                  disabled={loading.etfs}
                >
                  <option value="">None</option>
                  {loading.etfs ? (
                    <option disabled>Loading ETFs...</option>
                  ) : errors.etfs ? (
                    <option disabled>Error loading ETFs</option>
                  ) : etfsList.length > 0 ? (
                    etfsList.map((etf) => (
                      <option key={etf.symbol} value={etf.symbol}>
                        {etf.symbol} - {etf.long_name || etf.name || etf.short_name}
                      </option>
                    ))
                  ) : (
                    <option disabled>No ETFs available</option>
                  )}
                </select>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-4">
        {/* ETF Headers */}
        {getSelectedFunds().length > 0 && (
          <div className={`mb-4 flex flex-wrap gap-3 ${getSelectedFunds().length === 3 ? 'gap-2' : 'gap-3'}`}>
            {getSelectedFunds().map((symbol) => {
              const actualIndex = selectedFunds.indexOf(symbol);
              const fund = fundData[actualIndex];
              const isLoading = loading.funds[actualIndex];
              const error = errors.funds[actualIndex];
              const isCompact = getSelectedFunds().length === 3;

              if (isLoading) {
                return <LoadingCard key={symbol} title={`${symbol} data`} />;
              }

              if (error) {
                return <ErrorCard key={symbol} title={`${symbol} data`} error={error} />;
              }

              if (!fund) return null;

              return (
                <ETFCard 
                  key={symbol}
                  fund={fund}
                  isCompact={isCompact}
                />
              );
            })}
          </div>
        )}

        {/* Performance Chart */}
        {getSelectedFunds().length > 0 && (
          <PerformanceChart
            selectedFunds={getSelectedFunds()}
            chartData={getSelectedFunds().map(symbol => {
              const index = selectedFunds.indexOf(symbol);
              return chartData[index];
            })}
            combinedChartData={combinedChartData}
            selectedPeriod={selectedPeriod}
            chartValueType={chartValueType}
            loading={getSelectedFunds().map(symbol => {
              const index = selectedFunds.indexOf(symbol);
              return loading.priceHistory[index];
            })}
            errors={getSelectedFunds().map(symbol => {
              const index = selectedFunds.indexOf(symbol);
              return errors.priceHistory[index];
            })}
            onPeriodChange={setSelectedPeriod}
            onChartValueTypeChange={setChartValueType}
          />
        )}

        {/* Fund Tabs */}
        <FundTabs 
          selectedFunds={getSelectedFunds()}
          activeFundTab={activeFundTab}
          onTabChange={setActiveFundTab}
        />
        
        {/* Key Metrics */}
        {getSelectedFunds().length > 0 && activeData && activeData.fund && (
          <KeyMetrics fund={activeData.fund} />
        )}

        {/* Detailed Analytics */}
        {getSelectedFunds().length > 0 && activeData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Holdings */}
            <HoldingsChart
              holdings={activeData.holdings}
              chartType={holdingsChartType}
              loading={activeData.loading.holdings}
              error={activeData.errors.holdings}
              onChartTypeChange={setHoldingsChartType}
            />

            {/* Sector Allocation */}
            <SectorChart
              sectors={activeData.summary?.top_sectors || []}
              chartType={sectorChartType}
              loading={activeData.loading.summary}
              error={activeData.errors.summary}
              onChartTypeChange={setSectorChartType}
            />
          </div>
        )}

        {/* Detailed Fund Performance */}
        {getSelectedFunds().length > 0 && activeData && activeData.fund && (
          <DetailedPerformance 
            fund={activeData.fund}
            symbol={activeData.symbol}
          />
        )}
      </div>
    </div>
  );
}