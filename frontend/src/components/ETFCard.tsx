import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Card, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { ETF } from '@/types';

interface ETFCardProps {
  fund: ETF;
  isCompact: boolean;
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

export default function ETFCard({ fund, isCompact }: ETFCardProps) {
  return (
    <Card className="bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 border-0 shadow-md flex-1 min-w-0">
      <CardHeader className={`${isCompact ? 'pb-2 pt-2 px-4' : 'pb-3 pt-3'}`}>
        <div className="flex items-center justify-between min-w-0">
          <div className={`flex items-center ${isCompact ? 'space-x-2' : 'space-x-4'} min-w-0 flex-1`}>
            <div className={`flex items-center justify-center ${isCompact ? 'w-10 h-10' : 'w-12 h-12'} bg-blue-100 dark:bg-blue-900 rounded-lg flex-shrink-0`}>
              <span className={`${isCompact ? 'text-base' : 'text-lg'} font-bold text-blue-600 dark:text-blue-300`}>{fund.symbol}</span>
            </div>
            <div className="min-w-0 flex-1">
              <h2 className={`${isCompact ? 'text-lg' : 'text-xl'} font-bold text-foreground mb-0 ${isCompact ? 'truncate' : ''}`} title={fund.long_name || fund.name}>{fund.long_name || fund.name}</h2>
              <p className={`${isCompact ? 'text-xs' : 'text-sm'} text-muted-foreground ${isCompact ? 'truncate' : ''}`} title={fund.short_name || fund.name}>{fund.short_name || fund.name}</p>
              <div className={`flex items-center ${isCompact ? 'space-x-1 mt-0.5' : 'space-x-2 mt-1'}`}>
                {fund.beta && (
                  <Badge variant="outline" className={`${isCompact ? 'text-xs px-1 py-0' : 'text-xs px-2 py-0'}`}>
                    β: {fund.beta}
                  </Badge>
                )}
                {fund.pe_ratio && (
                  <Badge variant="outline" className={`${isCompact ? 'text-xs px-1 py-0' : 'text-xs px-2 py-0'}`}>
                    P/E: {fund.pe_ratio}
                  </Badge>
                )}
                {fund.dividend_yield && (
                  <Badge variant={fund.dividend_yield > 1 ? "default" : "secondary"} className={`${isCompact ? 'text-xs px-1 py-0' : 'text-xs px-2 py-0'}`}>
                    Yield: {fund.dividend_yield.toFixed(2)}%
                  </Badge>
                )}
              </div>
            </div>
          </div>
          <div className="text-right flex-shrink-0 ml-2">
            <div className={`${isCompact ? 'text-xl' : 'text-2xl'} font-bold text-foreground ${isCompact ? 'mb-0.5' : 'mb-1'}`}>
              ${(fund.nav || fund.regular_market_price || fund.current_price || 0).toFixed(2)}
            </div>
            {fund.regular_market_change_percent !== undefined && (
              <div className={`flex items-center justify-end ${fund.regular_market_change_percent > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {fund.regular_market_change_percent > 0 ? <TrendingUp className={`${isCompact ? 'w-3 h-3' : 'w-4 h-4'} mr-1`} /> : <TrendingDown className={`${isCompact ? 'w-3 h-3' : 'w-4 h-4'} mr-1`} />}
                <span className={`${isCompact ? 'text-xs' : 'text-sm'} font-semibold`}>{formatPercentage(fund.regular_market_change_percent)}</span>
                {fund.regular_market_change && (
                  <span className={`ml-1 ${isCompact ? 'text-xs' : 'text-xs'}`}>{formatCurrency(fund.regular_market_change)}</span>
                )}
              </div>
            )}
            {fund.previous_close && (
              <div className={`${isCompact ? 'text-xs' : 'text-xs'} text-muted-foreground`}>
                Prev: ${fund.previous_close.toFixed(2)}
              </div>
            )}
          </div>
        </div>
      </CardHeader>
    </Card>
  );
}
