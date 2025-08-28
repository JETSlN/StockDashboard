# Stock Dashboard API Client

This directory contains the frontend API client for the Stock Dashboard application. It provides TypeScript-typed functions to interact with the backend FastAPI endpoints.

## Structure

```
src/api/
├── config.ts          # API configuration and base client
├── fundService.ts     # Fund-related API functions
├── priceService.ts    # Price-related API functions
├── examples.ts        # Usage examples
├── index.ts          # Main export file
└── README.md         # This file

src/types/
├── fund.ts           # TypeScript type definitions
└── index.ts          # Types export file
```

## Quick Start

```typescript
import { listETFs, getETF, getPriceHistory } from '@/api';

// List all ETFs
const etfs = await listETFs();

// Get specific ETF details
const spy = await getETF('SPY');

// Get price history
const prices = await getPriceHistory('SPY', {
  start: '2024-01-01',
  end: '2024-12-31'
});
```

## Available Functions

### Fund Functions

- `listETFs()` - Get all ETFs
- `getETF(symbolOrId)` - Get specific ETF details
- `getFundSummary(symbolOrId)` - Get fund summary with top holdings/sectors
- `getFundHoldings(symbolOrId)` - Get all fund holdings
- `getFundSectorAllocations(symbolOrId)` - Get sector allocations
- `searchETFs(query)` - Search ETFs by symbol/name

### Price Functions

- `getPriceHistory(symbolOrId, params?)` - Get price history with optional date range
- `getLatestPrice(symbolOrId)` - Get most recent price
- `getPriceSummary(symbolOrId)` - Get price summary with statistics
- `getPriceHistoryLastMonth(symbolOrId)` - Convenience function for last 30 days
- `getPriceHistoryLastYear(symbolOrId)` - Convenience function for last 365 days
- `getPriceHistoryYTD(symbolOrId)` - Year-to-date price history

### Utility Functions

- `calculatePriceChange(priceHistory)` - Calculate price change and percentage
- `calculateTotalReturn(priceHistory)` - Calculate total return over period
- `findPriceExtremes(priceHistory)` - Find highest and lowest prices

## Configuration

Set your API base URL via environment variable:

```bash
# .env
VITE_API_URL=http://localhost:8000
```

If not set, it defaults to `http://localhost:8000`.

## Error Handling

All functions throw `APIError` instances for HTTP errors:

```typescript
import { getETF, APIError } from '@/api';

try {
  const etf = await getETF('INVALID');
} catch (error) {
  if (error instanceof APIError) {
    console.log('Status:', error.status);
    console.log('Message:', error.message);
  }
}
```

## TypeScript Types

Import types from the types module:

```typescript
import type { ETF, PriceHistory, Holding } from '@/types';

const etf: ETF = await getETF('SPY');
const prices: PriceHistory[] = await getPriceHistory('SPY');
```

## React Usage Example

```typescript
import { useEffect, useState } from 'react';
import { getETF, getPriceHistory } from '@/api';
import type { ETF, PriceHistory } from '@/types';

function ETFDetails({ symbol }: { symbol: string }) {
  const [etf, setETF] = useState<ETF | null>(null);
  const [prices, setPrices] = useState<PriceHistory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [etfData, priceData] = await Promise.all([
          getETF(symbol),
          getPriceHistory(symbol)
        ]);
        setETF(etfData);
        setPrices(priceData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [symbol]);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>{etf?.name} ({etf?.symbol})</h1>
      <p>Current Price: ${etf?.current_price}</p>
      <p>Price History: {prices.length} records</p>
    </div>
  );
}
```

## Backend API Mapping

| Frontend Function | Backend Endpoint | Description |
|------------------|------------------|-------------|
| `listETFs()` | `GET /api/funds/` | List all ETFs |
| `getETF(id)` | `GET /api/funds/{id}` | Get ETF details |
| `getFundSummary(id)` | `GET /api/funds/{id}/summary` | Get fund summary |
| `getFundHoldings(id)` | `GET /api/funds/{id}/holdings` | Get holdings |
| `getFundSectorAllocations(id)` | `GET /api/funds/{id}/sectors` | Get sectors |
| `getPriceHistory(id)` | `GET /api/funds/{id}/prices` | Get price history |
| `getLatestPrice(id)` | `GET /api/funds/{id}/prices/latest` | Get latest price |
| `getPriceSummary(id)` | `GET /api/funds/{id}/prices/summary` | Get price summary |

## Notes

- All functions support both symbol (e.g., 'SPY') and ID (e.g., 1) parameters
- Date parameters should be in YYYY-MM-DD format
- Functions return Promises and should be used with async/await or .then()
- Consider using a data fetching library like React Query or SWR for production apps
