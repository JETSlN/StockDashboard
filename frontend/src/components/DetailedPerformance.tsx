import React from 'react';
import { Activity } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ETF } from '@/types';

interface DetailedPerformanceProps {
  fund: ETF;
  symbol: string;
}

const formatCurrency = (value: number) => {
  if (value >= 1e12) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    }).format(value / 1e12) + 'T';
  } else if (value >= 1e9) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    }).format(value / 1e9) + 'B';
  } else if (value >= 1e6) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    }).format(value / 1e6) + 'M';
  }
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

const formatPercentage = (value: number) => {
  return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
};

const formatVolume = (value: number) => {
  if (value >= 1e9) {
    return (value / 1e9).toFixed(1) + 'B';
  } else if (value >= 1e6) {
    return (value / 1e6).toFixed(1) + 'M';
  } else if (value >= 1e3) {
    return (value / 1e3).toFixed(1) + 'K';
  }
  return value.toLocaleString();
};

export default function DetailedPerformance({ fund, symbol }: DetailedPerformanceProps) {
  return (
    <Card className="mt-4 border-0 shadow-md">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center text-lg">
          <Activity className="w-5 h-5 mr-2 text-blue-500" />
          Detailed {symbol} Performance & Statistics
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          
          {/* Performance Metrics */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-muted-foreground border-b pb-2">Performance Returns</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">YTD Monthly Total Return</span>
                <span className={`text-xs font-semibold ${(fund?.ytd_return || 0) > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {fund?.ytd_return ? formatPercentage(fund.ytd_return) : 'N/A'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">3Y Monthly Total Return</span>
                <span className={`text-xs font-semibold ${(fund?.three_year_return || 0) > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {fund?.three_year_return ? formatPercentage(fund.three_year_return * 100) : 'N/A'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">5Y Monthly Total Return</span>
                <span className={`text-xs font-semibold ${(fund?.five_year_return || 0) > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {fund?.five_year_return ? formatPercentage(fund.five_year_return * 100) : 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* Risk & Valuation */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-muted-foreground border-b pb-2">Risk & Valuation</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Beta</span>
                <span className="text-xs font-semibold">{fund?.beta || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">P/E Ratio</span>
                <span className="text-xs font-semibold">{fund?.pe_ratio || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">P/B Ratio</span>
                <span className="text-xs font-semibold">{fund?.pb_ratio || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">52W High</span>
                <span className="text-xs font-semibold">{fund?.fifty_two_week_high ? `$${fund.fifty_two_week_high.toFixed(2)}` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">52W Low</span>
                <span className="text-xs font-semibold">{fund?.fifty_two_week_low ? `$${fund.fifty_two_week_low.toFixed(2)}` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">52W Change</span>
                <span className={`text-xs font-semibold ${(fund?.fifty_two_week_change_percent || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {fund?.fifty_two_week_change_percent ? formatPercentage(fund.fifty_two_week_change_percent) : 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* Fund Operations */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-muted-foreground border-b pb-2">Fund Operations</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Net Assets</span>
                <span className="text-xs font-semibold">{fund?.net_assets ? formatCurrency(fund.net_assets) : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Market Cap</span>
                <span className="text-xs font-semibold">{fund?.market_cap ? formatCurrency(fund.market_cap) : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Expense Ratio</span>
                <span className="text-xs font-semibold">{fund?.net_expense_ratio ? `${(fund.net_expense_ratio * 100).toFixed(2)}%` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Dividend Yield</span>
                <span className="text-xs font-semibold">{fund?.dividend_yield ? `${fund.dividend_yield.toFixed(2)}%` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Fund Family</span>
                <span className="text-xs font-semibold">{fund?.family || 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* Trading & Volume */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-muted-foreground border-b pb-2">Trading & Volume</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Current Price</span>
                <span className="text-xs font-semibold">{fund?.regular_market_price ? `$${fund.regular_market_price.toFixed(2)}` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Previous Close</span>
                <span className="text-xs font-semibold">{fund?.previous_close ? `$${fund.previous_close.toFixed(2)}` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Day Change</span>
                <span className={`text-xs font-semibold ${(fund?.regular_market_change || 0) > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {fund?.regular_market_change && fund?.regular_market_change_percent 
                    ? `${formatCurrency(fund.regular_market_change)} (${formatPercentage(fund.regular_market_change_percent)})` 
                    : 'N/A'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Volume</span>
                <span className="text-xs font-semibold">{fund?.volume ? formatVolume(fund.volume) : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Avg Volume</span>
                <span className="text-xs font-semibold">{fund?.average_volume ? formatVolume(fund.average_volume) : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">Volume Ratio</span>
                <span className="text-xs font-semibold">
                  {fund?.volume && fund?.average_volume 
                    ? `${(fund.volume / fund.average_volume).toFixed(2)}x` 
                    : 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* Technical Indicators */}
          <div className="space-y-3 md:col-span-2 lg:col-span-1">
            <h4 className="font-semibold text-sm text-muted-foreground border-b pb-2">Technical Indicators</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">50D Average</span>
                <span className="text-xs font-semibold">{fund?.fifty_day_average ? `$${fund.fifty_day_average.toFixed(2)}` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">200D Average</span>
                <span className="text-xs font-semibold">{fund?.two_hundred_day_average ? `$${fund.two_hundred_day_average.toFixed(2)}` : 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">50D vs Price</span>
                <span className={`text-xs font-semibold ${
                  (fund?.current_price || fund?.regular_market_price) && fund?.fifty_day_average && 
                  (fund.current_price || fund.regular_market_price || 0) > fund.fifty_day_average 
                    ? 'text-green-600' : 'text-red-600'
                }`}>
                  {(fund?.current_price || fund?.regular_market_price) && fund?.fifty_day_average 
                    ? formatPercentage((((fund.current_price || fund.regular_market_price || 0) - fund.fifty_day_average) / fund.fifty_day_average) * 100)
                    : 'N/A'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">200D vs Price</span>
                <span className={`text-xs font-semibold ${
                  (fund?.current_price || fund?.regular_market_price) && fund?.two_hundred_day_average && 
                  (fund.current_price || fund.regular_market_price || 0) > fund.two_hundred_day_average 
                    ? 'text-green-600' : 'text-red-600'
                }`}>
                  {(fund?.current_price || fund?.regular_market_price) && fund?.two_hundred_day_average 
                    ? formatPercentage((((fund.current_price || fund.regular_market_price || 0) - fund.two_hundred_day_average) / fund.two_hundred_day_average) * 100)
                    : 'N/A'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
