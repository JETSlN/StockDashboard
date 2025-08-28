# Stock Dashboard Backend

A comprehensive ETF data management backend built with FastAPI and SQLAlchemy.

## Features

- **Comprehensive ETF Data Models**: Store detailed ETF information, price history, holdings, and financial metrics
- **YFinance Integration**: Automated data ingestion from Yahoo Finance
- **FastAPI REST API**: Modern, fast web API with automatic OpenAPI documentation
- **SQLite Database**: Lightweight database for development and testing
- **Data Seeding**: Tools for loading demo data or real market data

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   └── main.py                  # FastAPI entrypoint
├── db/
│   ├── __init__.py
│   ├── models.py               # SQLAlchemy models
│   ├── ingest_yfinance.py     # ETF data ingestion
│   └── seed.py                # Database seeding
├── requirements.txt
└── README.md
```

## Setup

1. **Create and activate virtual environment** (if not already done):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   cd backend
   python -c "from db.models import init_db; init_db()"
   ```

## Usage

### Running the API Server

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Data Management

#### Seed with Demo Data
```bash
cd backend
python db/seed.py --mode demo --init-db
```

#### Ingest Real ETF Data
```bash
cd backend
python db/seed.py --mode real --init-db
```

#### Full ETF Data Ingestion (80+ popular ETFs)
```bash
cd backend
python db/ingest_yfinance.py
```

#### Clear Database
```bash
cd backend
python db/seed.py --mode clear
```

## Database Models

### ETF
Main ETF information including:
- Basic info (symbol, name, category, exchange)
- Financial metrics (expense ratio, yield, PE ratio, etc.)
- Performance metrics (returns, technical indicators)
- Trading data (volume, price ranges)

### ETFPriceHistory
Historical price data with:
- OHLCV data
- Calculated returns
- Daily and cumulative performance

### ETFInfo
Extended ETF information:
- Investment strategy and objectives
- Risk metrics
- Distribution information
- Raw yfinance data storage

### Additional Models
- **ETFHolding**: Portfolio composition data
- **SectorAllocation**: Sector breakdown
- **GeographicAllocation**: Geographic distribution

## API Endpoints

- `GET /`: Health check
- `GET /health`: System health status
- Additional endpoints can be added as needed

## Data Sources

- **Yahoo Finance**: Primary data source via yfinance library
- **Popular ETFs**: Pre-configured list of 80+ popular ETFs including:
  - Large cap (SPY, VOO, VTI)
  - International (VEA, VWO, VXUS)
  - Sector ETFs (XLK, XLF, XLV, etc.)
  - Bonds (BND, AGG, TLT)
  - Factor ETFs (VTV, VUG, MTUM)
  - Commodities (GLD, SLV, DBC)
  - Real Estate (VNQ, VNQI)

## Development

The backend is designed to be:
- **Extensible**: Easy to add new data sources and models
- **Robust**: Comprehensive error handling and logging
- **Scalable**: Prepared for production deployment
- **Well-documented**: Clear code structure and documentation

## Next Steps

1. Add API endpoints for data retrieval
2. Implement data filtering and aggregation
3. Add authentication and user management
4. Set up automated data updates
5. Add data validation and quality checks

