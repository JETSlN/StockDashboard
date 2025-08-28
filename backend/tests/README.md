# Stock Dashboard API Tests

Comprehensive test suite for the Stock Dashboard API controllers.

## Test Files

- **`test_fund_controller.py`** - Tests all fund-related endpoints
- **`test_price_controller.py`** - Tests all price-related endpoints  
- **`test_all_controllers.py`** - Runs both controller tests with comprehensive reporting
- **`run_tests.py`** - Quick test runner with command-line options

## Running Tests

### Run All Tests
```bash
python test_all_controllers.py
```

### Run Individual Controller Tests
```bash
# Fund controller only
python test_fund_controller.py

# Price controller only  
python test_price_controller.py
```

### Using the Test Runner
```bash
# All tests (default)
python run_tests.py

# Fund controller only
python run_tests.py fund

# Price controller only
python run_tests.py price

# With custom URL
python run_tests.py --url http://localhost:8080
```

## Test Coverage

### Fund Controller Endpoints
- ✅ `GET /api/funds/` - List all funds
- ✅ `GET /api/funds/{id}` - Get fund details (by symbol or ID)
- ✅ `GET /api/funds/{id}/holdings` - Get fund holdings
- ✅ `GET /api/funds/{id}/sectors` - Get sector allocations
- ✅ `GET /api/funds/{id}/summary` - Get fund summary

### Price Controller Endpoints
- ✅ `GET /api/funds/{id}/prices` - Get price history (with date filtering)
- ✅ `GET /api/funds/{id}/prices/latest` - Get latest price
- ✅ `GET /api/funds/{id}/prices/summary` - Get price summary

### Test Scenarios
- ✅ Valid fund symbols (SPY, QQQ, VOO)
- ✅ Fund lookup by ID  
- ✅ Date range filtering for prices
- ✅ Error handling (404 for invalid funds, 400 for invalid dates)
- ✅ Response format validation
- ✅ Expected field validation

## Prerequisites

1. **Server must be running:**
   ```bash
   cd /Users/jetsin/StockDashboard
   source venv/bin/activate
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Required Python packages:**
   - `requests` (for HTTP testing)
   - `json` (built-in)

## Test Results

The tests validate:
- ✅ HTTP status codes (200, 404, 400)
- ✅ Response format (JSON structure)
- ✅ Required fields presence
- ✅ Data types and content validation
- ✅ Error message clarity

**Latest Results: 27/27 tests passed (100% success rate)**

