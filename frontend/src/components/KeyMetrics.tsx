import React from 'react';
import { DollarSign, Users, Activity, Calendar, Target, TrendingUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import type { ETF } from '@/types';

interface KeyMetricsProps {
  fund: ETF;
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

export default function KeyMetrics({ fund }: KeyMetricsProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3 mb-4">
      <Card className="border-0 shadow-sm">
        <CardContent className="p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted-foreground">Net Assets</span>
            <DollarSign className="h-3 w-3 text-blue-500" />
          </div>
          <div className="text-lg font-bold">
            {fund?.net_assets ? formatCurrency(fund.net_assets) : 'N/A'}
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-sm">
        <CardContent className="p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted-foreground">YTD Monthly Total Return</span>
            <Activity className="h-3 w-3 text-green-500" />
          </div>
          <div className={`text-lg font-bold ${(fund?.ytd_return || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {fund?.ytd_return ? formatPercentage(fund.ytd_return) : 'N/A'}
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-sm">
        <CardContent className="p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted-foreground">3Y Monthly Total Return</span>
            <Calendar className="h-3 w-3 text-cyan-500" />
          </div>
          <div className={`text-lg font-bold ${(fund?.three_year_return || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {fund?.three_year_return ? formatPercentage(fund.three_year_return * 100) : 'N/A'}
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-sm">
        <CardContent className="p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted-foreground">5Y Monthly Total Return</span>
            <TrendingUp className="h-3 w-3 text-emerald-500" />
          </div>
          <div className={`text-lg font-bold ${(fund?.five_year_return || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {fund?.five_year_return ? formatPercentage(fund.five_year_return * 100) : 'N/A'}
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-sm">
        <CardContent className="p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted-foreground">Expense Ratio</span>
            <Users className="h-3 w-3 text-orange-500" />
          </div>
          <div className="text-lg font-bold">
            {fund?.net_expense_ratio ? `${(fund.net_expense_ratio * 100).toFixed(2)}%` : 'N/A'}
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-sm">
        <CardContent className="p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted-foreground">Dividend Yield</span>
            <Target className="h-3 w-3 text-indigo-500" />
          </div>
          <div className="text-lg font-bold">
            {fund?.dividend_yield ? `${fund.dividend_yield.toFixed(2)}%` : 'N/A'}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
