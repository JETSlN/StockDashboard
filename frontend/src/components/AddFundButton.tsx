import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Plus, Loader2, Check, AlertCircle, X } from 'lucide-react';
import { insertETF } from '../api/fundService';

interface AddFundButtonProps {
  onFundAdded?: () => void; // Callback to refresh the fund list
}

export const AddFundButton: React.FC<AddFundButtonProps> = ({ 
  onFundAdded
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [symbol, setSymbol] = useState('');
  const [includeHistory, setIncludeHistory] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{
    type: 'success' | 'error' | null;
    text: string;
  }>({ type: null, text: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!symbol.trim()) {
      setMessage({ type: 'error', text: 'Please enter a fund symbol' });
      return;
    }

    setIsLoading(true);
    setMessage({ type: null, text: '' });

    try {
      const result = await insertETF(symbol.trim(), includeHistory);
      
      if (result.success) {
        setMessage({ 
          type: 'success', 
          text: `Successfully added ${symbol.toUpperCase()}!` 
        });
        setSymbol('');
        
        // Call the callback to refresh the fund list
        if (onFundAdded) {
          onFundAdded();
        }
        
        // Close the form after a brief delay
        setTimeout(() => {
          setIsOpen(false);
          setMessage({ type: null, text: '' });
        }, 2000);
      } else {
        setMessage({ 
          type: 'error', 
          text: result.message || 'Failed to add fund' 
        });
      }
    } catch (error: any) {
      console.error('Error adding fund:', error);
      setMessage({ 
        type: 'error', 
        text: error.message || 'An error occurred while adding the fund' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setIsOpen(false);
    setSymbol('');
    setIncludeHistory(false);
    setMessage({ type: null, text: '' });
  };

  return (
    <>
      {/* Badge Button - same size as Live Data */}
      <Badge 
        className="px-3 py-1 bg-black text-white hover:bg-gray-800 cursor-pointer transition-colors"
        onClick={() => setIsOpen(true)}
      >
        <Plus className="w-3 h-3 mr-1" />
        Add Fund
      </Badge>

      {/* Modal Overlay */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-black/50" 
            onClick={handleCancel}
          />
          
          {/* Modal Content */}
          <Card className="relative w-full max-w-md mx-4 bg-white shadow-xl">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg flex items-center">
                  <Plus className="w-5 h-5 mr-2" />
                  Add New Fund
                </CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCancel}
                  className="h-6 w-6 p-0"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="symbol" className="block text-sm font-medium mb-1">
                    Fund Symbol
                  </label>
                  <Input
                    id="symbol"
                    type="text"
                    value={symbol}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSymbol(e.target.value.toUpperCase())}
                    placeholder="e.g., TLT, ARKK, SCHD (ETFs only)"
                    disabled={isLoading}
                    className="uppercase"
                    maxLength={10}
                    autoFocus
                  />
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    id="includeHistory"
                    type="checkbox"
                    checked={includeHistory}
                    onChange={(e) => setIncludeHistory(e.target.checked)}
                    disabled={isLoading}
                    className="rounded"
                  />
                  <label htmlFor="includeHistory" className="text-sm">
                    Include price history (slower)
                  </label>
                </div>

                {message.text && (
                  <div className={`flex items-center space-x-2 p-2 rounded text-sm ${
                    message.type === 'success' 
                      ? 'bg-green-50 text-green-700 border border-green-200' 
                      : 'bg-red-50 text-red-700 border border-red-200'
                  }`}>
                    {message.type === 'success' ? (
                      <Check className="w-4 h-4" />
                    ) : (
                      <AlertCircle className="w-4 h-4" />
                    )}
                    <span>{message.text}</span>
                  </div>
                )}

                <div className="flex space-x-2">
                  <Button
                    type="submit"
                    disabled={isLoading || !symbol.trim()}
                    className="flex-1"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Adding...
                      </>
                    ) : (
                      <>
                        <Plus className="w-4 h-4 mr-2" />
                        Add Fund
                      </>
                    )}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleCancel}
                    disabled={isLoading}
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </>
  );
};
