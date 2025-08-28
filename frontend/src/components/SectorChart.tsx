import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { Target, BarChart3, PieChart as PieChartIcon, Loader2, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';

interface Sector {
  sector_name: string;
  allocation_percentage: number;
}

interface SectorChartProps {
  sectors: Sector[];
  chartType: 'bar' | 'pie';
  loading: boolean;
  error: string | null;
  onChartTypeChange: (type: 'bar' | 'pie') => void;
}

// Chart colors for consistency
const CHART_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316', '#6B7280', '#EC4899', '#14B8A6'];

export default function SectorChart({ 
  sectors, 
  chartType, 
  loading, 
  error, 
  onChartTypeChange 
}: SectorChartProps) {
  return (
    <Card className="border-0 shadow-md">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center text-base">
            <Target className="w-4 h-4 mr-2 text-purple-500" />
            Sector Allocation
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
              <span className="text-sm text-muted-foreground">Loading sectors...</span>
            </div>
          </div>
        ) : error ? (
          <div className="h-[200px] flex items-center justify-center">
            <div className="flex items-center space-x-2 text-red-600">
              <AlertCircle className="h-4 w-4" />
              <span className="text-sm">Error loading sectors: {error}</span>
            </div>
          </div>
        ) : sectors && sectors.length > 0 ? (
          chartType === 'bar' ? (
            <div className="space-y-2 max-h-[280px] overflow-y-auto">
              {sectors.map((sector, index) => (
                <div key={sector.sector_name} className="space-y-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div 
                        className="w-3 h-3 rounded-full flex-shrink-0" 
                        style={{ backgroundColor: CHART_COLORS[index % CHART_COLORS.length] }}
                      />
                      <span className="text-xs font-medium truncate">{sector.sector_name}</span>
                    </div>
                    <span className="text-xs font-bold">{sector.allocation_percentage?.toFixed(1) || '0.0'}%</span>
                  </div>
                  <Progress 
                    value={(sector.allocation_percentage || 0) * 3.5} 
                    className="h-1.5" 
                  />
                </div>
              ))}
            </div>
          ) : (
            <div>
              <div className="h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={sectors}
                      cx="50%"
                      cy="50%"
                      outerRadius={70}
                      fill="#8884d8"
                      dataKey="allocation_percentage"
                      label={({ allocation_percentage }) => 
                        (allocation_percentage || 0) > 5 ? `${(allocation_percentage || 0).toFixed(0)}%` : ''
                      }
                      labelLine={false}
                    >
                      {sectors.map((_entry, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value: number, _name: string, props: any) => [
                        `${value.toFixed(1)}%`,
                        props.payload.sector_name
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
                {sectors.slice(0, 8).map((sector, index) => (
                  <div key={sector.sector_name} className="flex items-center space-x-1">
                    <div 
                      className="w-2 h-2 rounded-full flex-shrink-0" 
                      style={{ backgroundColor: CHART_COLORS[index % CHART_COLORS.length] }}
                    />
                    <span className="text-xs text-muted-foreground truncate">
                      {sector.sector_name.replace('Consumer ', '').replace('Financial ', '')}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )
        ) : (
          <div className="h-[200px] flex items-center justify-center">
            <span className="text-sm text-muted-foreground">No sector data available</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
