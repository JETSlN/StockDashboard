"""
SQLAlchemy models for ETF data storage

This module contains comprehensive database models for storing ETF information,
price history, holdings, and other financial data.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/stock_dashboard.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ETF(Base):
    """
    Main ETF information table
    """
    __tablename__ = "etfs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    
    # Basic Info
    category = Column(String(100))  # yfinance: category
    family = Column(String(100))    # yfinance: fundFamily
    exchange = Column(String(20))   # yfinance: exchange
    full_exchange_name = Column(String(100))  # yfinance: fullExchangeName
    currency = Column(String(10))   # yfinance: currency
    country = Column(String(50))    # yfinance: region
    legal_type = Column(String(50)) # yfinance: legalType
    
    # Financial Metrics
    net_assets = Column(Float)  # Total net assets
    nav = Column(Float)  # Net Asset Value
    expense_ratio = Column(Float)
    yield_rate = Column(Float)  # Dividend yield
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    beta = Column(Float)
    
    # Performance Metrics (yfinance available)
    ytd_return = Column(Float)                    # yfinance: ytdReturn
    three_year_return = Column(Float)             # yfinance: threeYearAverageReturn
    five_year_return = Column(Float)              # yfinance: fiveYearAverageReturn
    trailing_three_month_returns = Column(Float)  # yfinance: trailingThreeMonthReturns
    
    # Inception and Management
    inception_date = Column(Date)        # Custom calculated field
    fund_inception_date = Column(Date)   # yfinance: fundInceptionDate
    
    # Additional Info (yfinance available)
    website = Column(String(255))        # Not directly available
    summary = Column(Text)               # yfinance: longBusinessSummary  
    long_name = Column(String(255))      # yfinance: longName
    short_name = Column(String(100))     # yfinance: shortName
    
    # Technical Indicators
    fifty_day_average = Column(Float)
    two_hundred_day_average = Column(Float)
    fifty_two_week_high = Column(Float)
    fifty_two_week_low = Column(Float)
    
    # Volume and Trading (yfinance available)
    average_volume = Column(Float)               # yfinance: averageVolume
    average_volume_10days = Column(Float)        # yfinance: averageVolume10days
    average_daily_volume_3month = Column(Float)  # yfinance: averageDailyVolume3Month
    shares_outstanding = Column(Float)           # yfinance: sharesOutstanding
    market_cap = Column(Float)                   # yfinance: marketCap
    
    # Current Trading Data
    current_price = Column(Float)                # yfinance: regularMarketPrice
    day_high = Column(Float)                     # yfinance: dayHigh
    day_low = Column(Float)                      # yfinance: dayLow
    previous_close = Column(Float)               # yfinance: previousClose
    
    # Dividend Information
    trailing_annual_dividend_rate = Column(Float)  # yfinance: trailingAnnualDividendRate
    trailing_annual_dividend_yield = Column(Float) # yfinance: trailingAnnualDividendYield
    
    # MISSING FIELDS - NOW ADDED FROM YFINANCE JSON
    
    # Market Data Fields
    open_price = Column(Float)  # yfinance: open
    regular_market_open = Column(Float)  # yfinance: regularMarketOpen
    regular_market_day_low = Column(Float)  # yfinance: regularMarketDayLow
    regular_market_day_high = Column(Float)  # yfinance: regularMarketDayHigh
    regular_market_previous_close = Column(Float)  # yfinance: regularMarketPreviousClose
    regular_market_price = Column(Float)  # yfinance: regularMarketPrice
    regular_market_volume = Column(Float)  # yfinance: regularMarketVolume
    regular_market_change = Column(Float)  # yfinance: regularMarketChange
    regular_market_change_percent = Column(Float)  # yfinance: regularMarketChangePercent
    regular_market_day_range = Column(String(50))  # yfinance: regularMarketDayRange
    
    # Bid/Ask Data
    bid = Column(Float)  # yfinance: bid
    ask = Column(Float)  # yfinance: ask
    bid_size = Column(Integer)  # yfinance: bidSize
    ask_size = Column(Integer)  # yfinance: askSize
    
    # Post Market Data
    post_market_price = Column(Float)  # yfinance: postMarketPrice
    post_market_change = Column(Float)  # yfinance: postMarketChange
    post_market_change_percent = Column(Float)  # yfinance: postMarketChangePercent
    
    # Additional Volume Data
    volume = Column(Float)  # yfinance: volume
    average_daily_volume_10day = Column(Float)  # yfinance: averageDailyVolume10Day
    
    # 52-Week Performance Calculations
    fifty_two_week_change_percent = Column(Float)  # yfinance: fiftyTwoWeekChangePercent
    fifty_two_week_low_change = Column(Float)  # yfinance: fiftyTwoWeekLowChange
    fifty_two_week_low_change_percent = Column(Float)  # yfinance: fiftyTwoWeekLowChangePercent
    fifty_two_week_high_change = Column(Float)  # yfinance: fiftyTwoWeekHighChange
    fifty_two_week_high_change_percent = Column(Float)  # yfinance: fiftyTwoWeekHighChangePercent
    fifty_two_week_range = Column(String(50))  # yfinance: fiftyTwoWeekRange
    
    # Moving Average Changes
    fifty_day_average_change = Column(Float)  # yfinance: fiftyDayAverageChange
    fifty_day_average_change_percent = Column(Float)  # yfinance: fiftyDayAverageChangePercent
    two_hundred_day_average_change = Column(Float)  # yfinance: twoHundredDayAverageChange
    two_hundred_day_average_change_percent = Column(Float)  # yfinance: twoHundredDayAverageChangePercent
    
    # Additional Fund Data
    book_value = Column(Float)  # yfinance: bookValue
    dividend_yield = Column(Float)  # yfinance: dividendYield
    trailing_three_month_nav_returns = Column(Float)  # yfinance: trailingThreeMonthNavReturns
    eps_trailing_twelve_months = Column(Float)  # yfinance: epsTrailingTwelveMonths
    trailing_peg_ratio = Column(Float)  # yfinance: trailingPegRatio
    total_assets = Column(Float)  # yfinance: totalAssets
    net_expense_ratio = Column(Float)  # yfinance: netExpenseRatio
    price_to_book = Column(Float)  # yfinance: priceToBook
    
    # Market Metadata
    quote_type = Column(String(20))  # yfinance: quoteType
    market = Column(String(50))  # yfinance: market
    exchange_timezone_name = Column(String(100))  # yfinance: exchangeTimezoneName
    exchange_timezone_short_name = Column(String(10))  # yfinance: exchangeTimezoneShortName
    gmt_offset_milliseconds = Column(Integer)  # yfinance: gmtOffSetMilliseconds
    market_state = Column(String(20))  # yfinance: marketState
    language = Column(String(10))  # yfinance: language
    region = Column(String(10))  # yfinance: region
    type_disp = Column(String(20))  # yfinance: typeDisp
    quote_source_name = Column(String(100))  # yfinance: quoteSourceName
    
    # Trading Metadata
    tradeable = Column(Boolean)  # yfinance: tradeable
    crypto_tradeable = Column(Boolean)  # yfinance: cryptoTradeable
    has_pre_post_market_data = Column(Boolean)  # yfinance: hasPrePostMarketData
    triggerable = Column(Boolean)  # yfinance: triggerable
    esg_populated = Column(Boolean)  # yfinance: esgPopulated
    
    # Technical Data
    price_hint = Column(Integer)  # yfinance: priceHint
    source_interval = Column(Integer)  # yfinance: sourceInterval
    exchange_data_delayed_by = Column(Integer)  # yfinance: exchangeDataDelayedBy
    max_age = Column(Integer)  # yfinance: maxAge
    
    # Timestamps
    first_trade_date_milliseconds = Column(Integer)  # yfinance: firstTradeDateMilliseconds
    regular_market_time = Column(Integer)  # yfinance: regularMarketTime
    post_market_time = Column(Integer)  # yfinance: postMarketTime
    
    # Additional Identifiers
    message_board_id = Column(String(50))  # yfinance: messageBoardId
    financial_currency = Column(String(10))  # yfinance: financialCurrency
    
    # Confidence and Alert Data
    custom_price_alert_confidence = Column(String(20))  # yfinance: customPriceAlertConfidence
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_data_update = Column(DateTime)
    
    # Relationships
    price_history = relationship("ETFPriceHistory", back_populates="etf", cascade="all, delete-orphan")
    holdings = relationship("ETFHolding", back_populates="etf", cascade="all, delete-orphan")
    sector_allocations = relationship("SectorAllocation", cascade="all, delete-orphan")
    fund_operations = relationship("FundOperations", uselist=False, cascade="all, delete-orphan")
    equity_metrics = relationship("EquityMetrics", uselist=False, cascade="all, delete-orphan")
    fund_overview = relationship("FundOverview", uselist=False, cascade="all, delete-orphan")

class ETFPriceHistory(Base):
    """
    Historical price data for ETFs
    """
    __tablename__ = "etf_price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    etf_id = Column(Integer, ForeignKey("etfs.id"), nullable=False)
    
    date = Column(Date, nullable=False, index=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float, nullable=False)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    
    # Calculated fields
    daily_return = Column(Float)  # Daily return percentage
    cumulative_return = Column(Float)  # Cumulative return from inception
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    etf = relationship("ETF", back_populates="price_history")
    
    # Composite index for efficient queries
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

class ETFHolding(Base):
    """
    ETF holdings/composition data
    """
    __tablename__ = "etf_holdings"
    
    id = Column(Integer, primary_key=True, index=True)
    etf_id = Column(Integer, ForeignKey("etfs.id"), nullable=False)
    
    # Holding details
    symbol = Column(String(20), index=True)
    name = Column(String(255))
    weight = Column(Float)  # Portfolio weight percentage
    shares = Column(Float)  # Number of shares held
    market_value = Column(Float)  # Market value of holding
    
    # Sector and geographic allocation
    sector = Column(String(100))
    industry = Column(String(100))
    country = Column(String(50))
    region = Column(String(50))
    
    # Asset classification
    asset_class = Column(String(50))  # Equity, Bond, Cash, etc.
    security_type = Column(String(50))  # Common Stock, Corporate Bond, etc.
    
    # Metadata
    as_of_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    etf = relationship("ETF", back_populates="holdings")



class SectorAllocation(Base):
    """
    ETF sector allocation data
    """
    __tablename__ = "sector_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    etf_id = Column(Integer, ForeignKey("etfs.id"), nullable=False)
    
    sector_name = Column(String(100), nullable=False)
    allocation_percentage = Column(Float, nullable=False)
    
    as_of_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)


class FundOperations(Base):
    """
    ETF fund operations data (from funds_data.fund_operations)
    """
    __tablename__ = "fund_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    etf_id = Column(Integer, ForeignKey("etfs.id"), nullable=False, unique=True)
    
    annual_report_expense_ratio = Column(Float)     # funds_data.fund_operations
    annual_holdings_turnover = Column(Float)        # funds_data.fund_operations  
    total_net_assets = Column(Float)                # funds_data.fund_operations
    category_average_expense_ratio = Column(Float)  # Category comparison
    category_average_turnover = Column(Float)       # Category comparison
    
    as_of_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EquityMetrics(Base):
    """
    ETF equity holdings metrics (from funds_data.equity_holdings)
    """
    __tablename__ = "equity_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    etf_id = Column(Integer, ForeignKey("etfs.id"), nullable=False, unique=True)
    
    # Fund-level equity metrics
    fund_price_earnings = Column(Float)             # Price/Earnings ratio
    fund_price_book = Column(Float)                 # Price/Book ratio  
    fund_price_sales = Column(Float)                # Price/Sales ratio
    fund_price_cashflow = Column(Float)             # Price/Cashflow ratio
    fund_median_market_cap = Column(Float)          # Median market cap
    fund_geometric_mean_market_cap = Column(Float)  # Geometric mean market cap
    
    # Category averages for comparison
    category_price_earnings = Column(Float)
    category_price_book = Column(Float)
    category_price_sales = Column(Float)
    
    as_of_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FundOverview(Base):
    """
    ETF fund overview data (from funds_data.fund_overview)
    """
    __tablename__ = "fund_overview"
    
    id = Column(Integer, primary_key=True, index=True)
    etf_id = Column(Integer, ForeignKey("etfs.id"), nullable=False, unique=True)
    
    category_name = Column(String(100))             # funds_data.fund_overview['categoryName']
    family = Column(String(100))                    # funds_data.fund_overview['family']
    legal_type = Column(String(50))                 # funds_data.fund_overview['legalType']
    description = Column(Text)                      # funds_data.description
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



def get_db():
    """
    Database session dependency
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database tables
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
