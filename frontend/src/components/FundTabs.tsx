import React from 'react';
import { Button } from '@/components/ui/button';

interface FundTabsProps {
  selectedFunds: string[];
  activeFundTab: number;
  onTabChange: (index: number) => void;
}

export default function FundTabs({ selectedFunds, activeFundTab, onTabChange }: FundTabsProps) {
  if (selectedFunds.length <= 1) return null;

  return (
    <div className="mb-4">
      <div className="flex space-x-1 bg-muted/30 p-1 rounded-lg inline-flex">
        {selectedFunds.map((symbol, index) => (
          <Button
            key={symbol}
            variant={activeFundTab === index ? 'default' : 'ghost'}
            size="sm"
            onClick={() => onTabChange(index)}
            className="h-8 px-3 text-sm"
          >
            {symbol}
          </Button>
        ))}
      </div>
    </div>
  );
}
