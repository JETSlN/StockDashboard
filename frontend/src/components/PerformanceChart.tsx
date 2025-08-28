import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { TrendingUp as TrendingUpIcon, Loader2, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface ChartDataPoint {
  date: string;
  fundPercent: number;
  fundPrice: number;
}

interface PerformanceChartProps {
  selectedFunds: string[];
  chartData: ChartDataPoint[][];
  combinedChartData: any[];
  selectedPeriod: '1M' | '3M' | 'YTD' | '1Y' | '3Y' | '5Y';
  chartValueType: 'percentage' | 'price';
  loading: boolean[];
  errors: (string | null)[];
  onPeriodChange: (period: '1M' | '3M' | 'YTD' | '1Y' | '3Y' | '5Y') => void;
  onChartValueTypeChange: (type: 'percentage' | 'price') => void;
}

// Chart colors for consistency
const CHART_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316', '#6B7280', '#EC4899', '#14B8A6'];

export default function PerformanceChart({
  selectedFunds,
  chartData,
  combinedChartData,
  selectedPeriod,
  chartValueType,
  loading,
  errors,
  onPeriodChange,
  onChartValueTypeChange
}: PerformanceChartProps) {
  // Calculate Y-axis domain for better scaling across all funds
  const getYAxisDomain = () => {
    if (combinedChartData.length === 0) return ['auto', 'auto'];
    
    const allValues: number[] = [];
    
    combinedChartData.forEach(dataPoint => {
      selectedFunds.forEach(symbol => {
        const value = chartValueType === 'percentage' 
          ? dataPoint[`${symbol}_percent`] 
          : dataPoint[`${symbol}_price`];
        if (typeof value === 'number' && !isNaN(value)) {
          allValues.push(value);
        }
      });
    });
    
    if (allValues.length === 0) return ['auto', 'auto'];
    
    const minValue = Math.min(...allValues);
    const maxValue = Math.max(...allValues);
    const range = maxValue - minValue;
    
    // Use different padding strategies based on data type
    if (chartValueType === 'percentage') {
      const padding = Math.max(range * 0.1, 2); // At least 2% padding for percentage view
      return [
        Math.round((Math.max(90, minValue - padding)) / 10) * 10, // Round to nearest 10
        Math.round((maxValue + padding) / 10) * 10
      ];
    } else {
      const padding = range * 0.05; // 5% padding for price view
      return [
        Math.round((Math.max(0, minValue - padding)) / 10) * 10, // Round to nearest 10
        Math.round((maxValue + padding) / 10) * 10
      ];
    }
  };

  // Calculate X-axis tick interval based on period to avoid overcrowding
  const getXAxisInterval = () => {
    const dataLength = combinedChartData.length;
    switch (selectedPeriod) {
      case '1M':
        return Math.max(0, Math.floor(dataLength / 8)); // Show ~8 ticks
      case '3M':
        return Math.max(0, Math.floor(dataLength / 10)); // Show ~10 ticks
      case 'YTD':
      case '1Y':
        return Math.max(0, Math.floor(dataLength / 12)); // Show ~12 ticks (months)
      case '3Y':
        return Math.max(0, Math.floor(dataLength / 15)); // Show ~15 ticks
      case '5Y':
        return Math.max(0, Math.floor(dataLength / 5)); // Show ~5 ticks (years)
      default:
        return Math.max(0, Math.floor(dataLength / 8));
    }
  };

  return (
    <Card className="mb-4 border-0 shadow-md">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between mb-3">
          <CardTitle className="flex items-center text-lg">
            <TrendingUpIcon className="w-4 h-4 mr-2 text-green-500" />
            Price Performance Comparison
          </CardTitle>
          <div className="flex items-center space-x-2">
            {/* Value Type Toggle */}
            <div className="flex items-center border rounded-lg p-1">
              <Button
                variant={chartValueType === 'percentage' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => onChartValueTypeChange('percentage')}
                className="h-6 px-2 text-xs"
              >
                %
              </Button>
              <Button
                variant={chartValueType === 'price' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => onChartValueTypeChange('price')}
                className="h-6 px-2 text-xs"
              >
                $
              </Button>
            </div>
          </div>
        </div>
        
        {/* Performance Metrics Display */}
        <div className="flex items-center justify-between mb-4 p-3 bg-muted/30 rounded-lg">
          <div className="flex items-center space-x-6 overflow-x-auto">
            {selectedFunds.map((symbol, displayIndex) => {
              const chartDataForFund = chartData[displayIndex] || [];
              const currentData = chartDataForFund.length > 0 ? chartDataForFund[chartDataForFund.length - 1] : null;
              const startData = chartDataForFund.length > 0 ? chartDataForFund[0] : null;
              
              const fundPeriodReturn = currentData && startData 
                ? chartValueType === 'percentage' 
                  ? ((currentData.fundPercent - startData.fundPercent) / startData.fundPercent) * 100
                  : currentData.fundPrice - startData.fundPrice
                : 0;
              
              return (
                <React.Fragment key={symbol}>
                  {displayIndex > 0 && <div className="h-8 w-px bg-border flex-shrink-0"></div>}
                  <div className="flex-shrink-0">
                    <div className="text-xs text-muted-foreground">{symbol} ({selectedPeriod})</div>
                    <div className={`text-lg font-bold ${fundPeriodReturn >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {chartValueType === 'percentage' 
                        ? `${fundPeriodReturn >= 0 ? '+' : ''}${fundPeriodReturn.toFixed(2)}%`
                        : `${fundPeriodReturn >= 0 ? '+' : ''}$${Math.abs(fundPeriodReturn).toFixed(2)}`
                      }
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Current: ${currentData?.fundPrice?.toFixed(2) || 'N/A'}
                    </div>
                  </div>
                </React.Fragment>
              );
            })}
          </div>
        </div>

        {/* Time Period Buttons */}
        <div className="flex items-center space-x-2 mb-4">
          {(['1M', '3M', 'YTD', '1Y', '3Y', '5Y'] as const).map((period) => (
            <Button
              key={period}
              variant={selectedPeriod === period ? 'default' : 'outline'}
              size="sm"
              onClick={() => onPeriodChange(period)}
              className="h-7 px-3 text-xs"
            >
              {period}
            </Button>
          ))}
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        {loading.some(Boolean) ? (
          <div className="h-[240px] flex items-center justify-center">
            <div className="flex items-center space-x-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="text-sm text-muted-foreground">Loading price data...</span>
            </div>
          </div>
        ) : errors.some(error => error !== null) ? (
          <div className="h-[240px] flex items-center justify-center">
            <div className="flex items-center space-x-2 text-red-600">
              <AlertCircle className="h-4 w-4" />
              <span className="text-sm">Error loading price data</span>
            </div>
          </div>
        ) : (
          <div className="h-[240px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={combinedChartData}>
                <defs>
                  {selectedFunds.map((symbol, index) => (
                    <linearGradient key={symbol} id={`${symbol}Gradient`} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={CHART_COLORS[index % CHART_COLORS.length]} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={CHART_COLORS[index % CHART_COLORS.length]} stopOpacity={0.1}/>
                    </linearGradient>
                  ))}
                </defs>
                <CartesianGrid strokeDasharray="3 3" className="opacity-20" />
                <XAxis 
                  dataKey="date" 
                  className="text-xs" 
                  tick={{ fontSize: 10 }}
                  height={40}
                  interval={getXAxisInterval()}
                  angle={selectedPeriod === '3Y' ? -45 : 0}
                  textAnchor={selectedPeriod === '3Y' ? 'end' : 'middle'}
                />
                <YAxis 
                  className="text-xs" 
                  tick={{ fontSize: 10 }}
                  width={60}
                  domain={getYAxisDomain()}
                  tickFormatter={(value) => 
                    chartValueType === 'percentage' 
                      ? `${Math.round(value / 10) * 10}%` 
                      : `$${Math.round(value / 10) * 10}`
                  }
                />
                <Tooltip 
                  formatter={(value: number, name: string) => {
                    const symbol = name.replace(/_(percent|price)$/, '');
                    const formattedValue = chartValueType === 'percentage' 
                      ? `${value.toFixed(1)}%` 
                      : `$${value.toFixed(2)}`;
                    return [formattedValue, symbol];
                  }}
                  labelStyle={{ color: '#374151', fontSize: '12px' }}
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                    border: 'none', 
                    borderRadius: '8px',
                    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                    fontSize: '12px'
                  }}
                />
                {selectedFunds.map((symbol, index) => (
                  <Area 
                    key={symbol}
                    type="monotone" 
                    dataKey={chartValueType === 'percentage' ? `${symbol}_percent` : `${symbol}_price`}
                    stroke={CHART_COLORS[index % CHART_COLORS.length]} 
                    strokeWidth={2}
                    fillOpacity={selectedFunds.length === 1 ? 1 : 0} 
                    fill={selectedFunds.length === 1 ? `url(#${symbol}Gradient)` : 'none'} 
                  />
                ))}
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
