import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { DollarSign, BarChart3, PieChart as PieChartIcon, Loader2, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import type { Holding } from '@/types';

interface HoldingsChartProps {
  holdings: Holding[];
  chartType: 'bar' | 'pie';
  loading: boolean;
  error: string | null;
  onChartTypeChange: (type: 'bar' | 'pie') => void;
}

// Chart colors for consistency
const CHART_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316', '#6B7280', '#EC4899', '#14B8A6'];

export default function HoldingsChart({ 
  holdings, 
  chartType, 
  loading, 
  error, 
  onChartTypeChange 
}: HoldingsChartProps) {
  return (
    <Card className="border-0 shadow-md">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center text-base">
            <DollarSign className="w-4 h-4 mr-2 text-blue-500" />
            Top Holdings
          </CardTitle>
          <div className="flex items-center space-x-1">
            <Button
              variant={chartType === 'bar' ? 'default' : 'outline'}
              size="sm"
              onClick={() => onChartTypeChange('bar')}
              className="h-7 px-2"
            >
              <BarChart3 className="w-3 h-3" />
            </Button>
            <Button
              variant={chartType === 'pie' ? 'default' : 'outline'}
              size="sm"
              onClick={() => onChartTypeChange('pie')}
              className="h-7 px-2"
            >
              <PieChartIcon className="w-3 h-3" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        {loading ? (
          <div className="h-[200px] flex items-center justify-center">
            <div className="flex items-center space-x-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="text-sm text-muted-foreground">Loading holdings...</span>
            </div>
          </div>
        ) : error ? (
          <div className="h-[200px] flex items-center justify-center">
            <div className="flex items-center space-x-2 text-red-600">
              <AlertCircle className="h-4 w-4" />
              <span className="text-sm">Error loading holdings: {error}</span>
            </div>
          </div>
        ) : holdings && holdings.length > 0 ? (
          chartType === 'bar' ? (
            <div className="space-y-3 max-h-[280px] overflow-y-auto">
              {(() => {
                // Calculate total weight of displayed holdings
                const totalWeight = holdings.reduce((sum, holding) => sum + (holding.weight || 0), 0);

                return holdings.map((holding, index) => {
                  // Calculate percentage relative to displayed holdings
                  const percentage = totalWeight > 0 ? ((holding.weight || 0) / totalWeight) * 100 : 0;

                  return (
                    <div key={holding.symbol || index} className="space-y-1">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white">
                            {index + 1}
                          </div>
                          <div>
                            <div className="font-semibold text-xs">{holding.symbol || 'N/A'}</div>
                            <div className="text-xs text-muted-foreground truncate max-w-[120px]">{holding.name || 'N/A'}</div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-bold text-xs">{holding.weight?.toFixed(2) || '0.00'}%</div>
                        </div>
                      </div>
                      <Progress value={percentage} className="h-1.5" />
                    </div>
                  );
                });
              })()}
            </div>
          ) : (
            <div>
              <div className="h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={holdings}
                      cx="50%"
                      cy="50%"
                      outerRadius={70}
                      fill="#8884d8"
                      dataKey="weight"
                      label={({ weight }) => (weight || 0) > 1.5 ? `${(weight || 0).toFixed(0)}%` : ''}
                      labelLine={false}
                    >
                      {holdings.map((_entry, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value: number, _name: string, props: any) => [
                        `${value.toFixed(2)}%`,
                        props.payload.symbol || props.payload.name
                      ]}
                      contentStyle={{
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        border: 'none',
                        borderRadius: '6px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                        fontSize: '11px'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Legend for pie chart */}
              <div className="grid grid-cols-2 gap-1 mt-2 text-xs">
                {holdings.slice(0, 8).map((holding, index) => (
                  <div key={holding.symbol || index} className="flex items-center space-x-1">
                    <div
                      className="w-2 h-2 rounded-full flex-shrink-0"
                      style={{ backgroundColor: CHART_COLORS[index % CHART_COLORS.length] }}
                    />
                    <span className="text-xs text-muted-foreground truncate">
                      {holding.symbol || holding.name || 'N/A'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )
        ) : (
          <div className="h-[200px] flex items-center justify-center">
            <span className="text-sm text-muted-foreground">No holdings data available</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
