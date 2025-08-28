"""
YFinance ETF Data Ingestion Script

This script pulls comprehensive ETF data from Yahoo Finance and stores it in the database.
It can ingest basic info, price history, holdings, and other financial data.
"""

import yfinance as yf
import pandas as pd
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import time
import logging
import json
from typing import List, Dict, Any, Optional
import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models import (
    engine, ETF, ETFPriceHistory, ETFHolding, 
    SectorAllocation, FundOperations, EquityMetrics, FundOverview, init_db
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create session
Session = sessionmaker(bind=engine)

class ETFDataIngester:
    """
    Class to handle ETF data ingestion from Yahoo Finance
    """
    
    def __init__(self):
        self.session = Session()
        
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
    
    def get_popular_etfs(self) -> List[str]:
        """
        Returns a list of popular ETF symbols for initial data loading
        """
        # Top 10 most popular ETFs - comprehensive coverage
        return ['SPY', 'QQQ', 'VOO', 'VTI', 'IVV', 'IEMG', 'VEA', 'AGG', 'VWO', 'EFA']
    
    def safe_get_info(self, ticker: yf.Ticker, field: str, default=None):
        """
        Safely extract information from yfinance ticker
        """
        try:
            info = ticker.info
            return info.get(field, default)
        except Exception as e:
            logger.warning(f"Could not get {field}: {e}")
            return default
    
    def ingest_etf_basic_info(self, symbol: str) -> Optional[ETF]:
        """
        Ingest basic ETF information with retry logic for rate limiting
        """
        max_retries = 3
        retry_delay = 30  # seconds - very conservative
        
        for attempt in range(max_retries):
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                # Check if ETF already exists
                existing_etf = self.session.query(ETF).filter(ETF.symbol == symbol).first()
                if existing_etf:
                    logger.info(f"ETF {symbol} already exists, updating...")
                    etf = existing_etf
                else:
                    etf = ETF(symbol=symbol)
                    self.session.add(etf)
                
                # Basic information
                etf.name = self.safe_get_info(ticker, 'longName', symbol)
                etf.category = self.safe_get_info(ticker, 'category')
                etf.family = self.safe_get_info(ticker, 'fundFamily')
                etf.exchange = self.safe_get_info(ticker, 'exchange')
                etf.currency = self.safe_get_info(ticker, 'currency')
                etf.country = self.safe_get_info(ticker, 'country')
                
                # Financial metrics
                etf.net_assets = self.safe_get_info(ticker, 'totalAssets')
                etf.nav = self.safe_get_info(ticker, 'navPrice')
                etf.expense_ratio = self.safe_get_info(ticker, 'annualReportExpenseRatio')
                etf.yield_rate = self.safe_get_info(ticker, 'yield')
                etf.pe_ratio = self.safe_get_info(ticker, 'trailingPE')
                etf.pb_ratio = self.safe_get_info(ticker, 'priceToBook')
                etf.beta = self.safe_get_info(ticker, 'beta')
                
                # Performance metrics
                etf.ytd_return = self.safe_get_info(ticker, 'ytdReturn')
                
                # Additional info
                etf.website = self.safe_get_info(ticker, 'website')
                etf.summary = self.safe_get_info(ticker, 'longBusinessSummary')
                etf.long_name = self.safe_get_info(ticker, 'longName')
                etf.short_name = self.safe_get_info(ticker, 'shortName')
                
                # Technical indicators
                etf.fifty_day_average = self.safe_get_info(ticker, 'fiftyDayAverage')
                etf.two_hundred_day_average = self.safe_get_info(ticker, 'twoHundredDayAverage')
                etf.fifty_two_week_high = self.safe_get_info(ticker, 'fiftyTwoWeekHigh')
                etf.fifty_two_week_low = self.safe_get_info(ticker, 'fiftyTwoWeekLow')
                
                # Volume
                etf.average_volume = self.safe_get_info(ticker, 'averageVolume')
                etf.average_volume_10days = self.safe_get_info(ticker, 'averageVolume10days')
                
                # ===== NEWLY ADDED COMPREHENSIVE YFINANCE FIELDS =====
                
                # Additional basic fields that were missing
                etf.full_exchange_name = self.safe_get_info(ticker, 'fullExchangeName')
                etf.legal_type = self.safe_get_info(ticker, 'legalType')
                etf.three_year_return = self.safe_get_info(ticker, 'threeYearAverageReturn')
                etf.five_year_return = self.safe_get_info(ticker, 'fiveYearAverageReturn')
                etf.trailing_three_month_returns = self.safe_get_info(ticker, 'trailingThreeMonthReturns')
                etf.average_daily_volume_3month = self.safe_get_info(ticker, 'averageDailyVolume3Month')
                etf.shares_outstanding = self.safe_get_info(ticker, 'sharesOutstanding')
                etf.market_cap = self.safe_get_info(ticker, 'marketCap')
                etf.current_price = self.safe_get_info(ticker, 'regularMarketPrice')
                etf.day_high = self.safe_get_info(ticker, 'dayHigh')
                etf.day_low = self.safe_get_info(ticker, 'dayLow')
                etf.previous_close = self.safe_get_info(ticker, 'previousClose')
                etf.trailing_annual_dividend_rate = self.safe_get_info(ticker, 'trailingAnnualDividendRate')
                etf.trailing_annual_dividend_yield = self.safe_get_info(ticker, 'trailingAnnualDividendYield')
                
                # Market Data Fields
                etf.open_price = self.safe_get_info(ticker, 'open')
                etf.regular_market_open = self.safe_get_info(ticker, 'regularMarketOpen')
                etf.regular_market_day_low = self.safe_get_info(ticker, 'regularMarketDayLow')
                etf.regular_market_day_high = self.safe_get_info(ticker, 'regularMarketDayHigh')
                etf.regular_market_previous_close = self.safe_get_info(ticker, 'regularMarketPreviousClose')
                etf.regular_market_price = self.safe_get_info(ticker, 'regularMarketPrice')
                etf.regular_market_volume = self.safe_get_info(ticker, 'regularMarketVolume')
                etf.regular_market_change = self.safe_get_info(ticker, 'regularMarketChange')
                etf.regular_market_change_percent = self.safe_get_info(ticker, 'regularMarketChangePercent')
                etf.regular_market_day_range = self.safe_get_info(ticker, 'regularMarketDayRange')
                
                # Bid/Ask Data
                etf.bid = self.safe_get_info(ticker, 'bid')
                etf.ask = self.safe_get_info(ticker, 'ask')
                etf.bid_size = self.safe_get_info(ticker, 'bidSize')
                etf.ask_size = self.safe_get_info(ticker, 'askSize')
                
                # Post Market Data
                etf.post_market_price = self.safe_get_info(ticker, 'postMarketPrice')
                etf.post_market_change = self.safe_get_info(ticker, 'postMarketChange')
                etf.post_market_change_percent = self.safe_get_info(ticker, 'postMarketChangePercent')
                
                # Additional Volume Data
                etf.volume = self.safe_get_info(ticker, 'volume')
                etf.average_daily_volume_10day = self.safe_get_info(ticker, 'averageDailyVolume10Day')
                
                # 52-Week Performance Calculations
                etf.fifty_two_week_change_percent = self.safe_get_info(ticker, 'fiftyTwoWeekChangePercent')
                etf.fifty_two_week_low_change = self.safe_get_info(ticker, 'fiftyTwoWeekLowChange')
                etf.fifty_two_week_low_change_percent = self.safe_get_info(ticker, 'fiftyTwoWeekLowChangePercent')
                etf.fifty_two_week_high_change = self.safe_get_info(ticker, 'fiftyTwoWeekHighChange')
                etf.fifty_two_week_high_change_percent = self.safe_get_info(ticker, 'fiftyTwoWeekHighChangePercent')
                etf.fifty_two_week_range = self.safe_get_info(ticker, 'fiftyTwoWeekRange')
                
                # Moving Average Changes
                etf.fifty_day_average_change = self.safe_get_info(ticker, 'fiftyDayAverageChange')
                etf.fifty_day_average_change_percent = self.safe_get_info(ticker, 'fiftyDayAverageChangePercent')
                etf.two_hundred_day_average_change = self.safe_get_info(ticker, 'twoHundredDayAverageChange')
                etf.two_hundred_day_average_change_percent = self.safe_get_info(ticker, 'twoHundredDayAverageChangePercent')
                
                # Additional Fund Data
                etf.book_value = self.safe_get_info(ticker, 'bookValue')
                etf.dividend_yield = self.safe_get_info(ticker, 'dividendYield')
                etf.trailing_three_month_nav_returns = self.safe_get_info(ticker, 'trailingThreeMonthNavReturns')
                etf.eps_trailing_twelve_months = self.safe_get_info(ticker, 'epsTrailingTwelveMonths')
                etf.trailing_peg_ratio = self.safe_get_info(ticker, 'trailingPegRatio')
                etf.total_assets = self.safe_get_info(ticker, 'totalAssets')
                etf.net_expense_ratio = self.safe_get_info(ticker, 'netExpenseRatio')
                etf.price_to_book = self.safe_get_info(ticker, 'priceToBook')
                
                # Market Metadata
                etf.quote_type = self.safe_get_info(ticker, 'quoteType')
                etf.market = self.safe_get_info(ticker, 'market')
                etf.exchange_timezone_name = self.safe_get_info(ticker, 'exchangeTimezoneName')
                etf.exchange_timezone_short_name = self.safe_get_info(ticker, 'exchangeTimezoneShortName')
                etf.gmt_offset_milliseconds = self.safe_get_info(ticker, 'gmtOffSetMilliseconds')
                etf.market_state = self.safe_get_info(ticker, 'marketState')
                etf.language = self.safe_get_info(ticker, 'language')
                etf.region = self.safe_get_info(ticker, 'region')
                etf.type_disp = self.safe_get_info(ticker, 'typeDisp')
                etf.quote_source_name = self.safe_get_info(ticker, 'quoteSourceName')
                
                # Trading Metadata
                etf.tradeable = self.safe_get_info(ticker, 'tradeable')
                etf.crypto_tradeable = self.safe_get_info(ticker, 'cryptoTradeable')
                etf.has_pre_post_market_data = self.safe_get_info(ticker, 'hasPrePostMarketData')
                etf.triggerable = self.safe_get_info(ticker, 'triggerable')
                etf.esg_populated = self.safe_get_info(ticker, 'esgPopulated')
                
                # Technical Data
                etf.price_hint = self.safe_get_info(ticker, 'priceHint')
                etf.source_interval = self.safe_get_info(ticker, 'sourceInterval')
                etf.exchange_data_delayed_by = self.safe_get_info(ticker, 'exchangeDataDelayedBy')
                etf.max_age = self.safe_get_info(ticker, 'maxAge')
                
                # Timestamps
                etf.first_trade_date_milliseconds = self.safe_get_info(ticker, 'firstTradeDateMilliseconds')
                etf.regular_market_time = self.safe_get_info(ticker, 'regularMarketTime')
                etf.post_market_time = self.safe_get_info(ticker, 'postMarketTime')
                
                # Additional Identifiers
                etf.message_board_id = self.safe_get_info(ticker, 'messageBoardId')
                etf.financial_currency = self.safe_get_info(ticker, 'financialCurrency')
                
                # Confidence and Alert Data
                etf.custom_price_alert_confidence = self.safe_get_info(ticker, 'customPriceAlertConfidence')
                
                # Update timestamps
                etf.updated_at = datetime.utcnow()
                etf.last_data_update = datetime.utcnow()
                
                self.session.commit()
                logger.info(f"Successfully ingested basic info for {symbol}")
                return etf
                
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limited for {symbol}, waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        logger.error(f"Max retries exceeded for {symbol} due to rate limiting")
                        self.session.rollback()
                        return None
                else:
                    logger.error(f"Error ingesting basic info for {symbol}: {e}")
                    self.session.rollback()
                    return None
        
        return None
    

    
    def ingest_price_history(self, etf: ETF, period: str = "5y") -> None:
        """
        Ingest historical price data
        """
        try:
            ticker = yf.Ticker(etf.symbol)
            
            # Get historical data
            hist = ticker.history(period=period)
            
            if hist.empty:
                logger.warning(f"No historical data found for {etf.symbol}")
                return
            
            # Clear existing data for this period (optional - or do incremental updates)
            # self.session.query(ETFPriceHistory).filter(ETFPriceHistory.etf_id == etf.id).delete()
            
            for date, row in hist.iterrows():
                # Check if this date already exists
                existing = self.session.query(ETFPriceHistory).filter(
                    ETFPriceHistory.etf_id == etf.id,
                    ETFPriceHistory.date == date.date()
                ).first()
                
                if existing:
                    continue  # Skip if already exists
                
                price_data = ETFPriceHistory(
                    etf_id=etf.id,
                    date=date.date(),
                    open_price=float(row['Open']) if pd.notna(row['Open']) else None,
                    high_price=float(row['High']) if pd.notna(row['High']) else None,
                    low_price=float(row['Low']) if pd.notna(row['Low']) else None,
                    close_price=float(row['Close']) if pd.notna(row['Close']) else None,
                    volume=int(row['Volume']) if pd.notna(row['Volume']) else None,
                )
                
                self.session.add(price_data)
            
            self.session.commit()
            logger.info(f"Successfully ingested price history for {etf.symbol}")
            
        except Exception as e:
            logger.error(f"Error ingesting price history for {etf.symbol}: {e}")
            self.session.rollback()
    
    def ingest_holdings(self, etf: ETF) -> None:
        """
        Ingest ETF holdings data using funds_data.top_holdings
        """
        try:
            ticker = yf.Ticker(etf.symbol)
            
            # Clear existing holdings for this ETF
            self.session.query(ETFHolding).filter(ETFHolding.etf_id == etf.id).delete()
            
            # Get holdings data from funds_data
            try:
                funds_data = ticker.funds_data
                if hasattr(funds_data, 'top_holdings'):
                    top_holdings = funds_data.top_holdings
                    
                    if isinstance(top_holdings, pd.DataFrame) and not top_holdings.empty:
                        logger.info(f"Found {len(top_holdings)} holdings for {etf.symbol}")
                        
                        for symbol, row in top_holdings.iterrows():
                            holding = ETFHolding(
                                etf_id=etf.id,
                                symbol=str(symbol),
                                name=row.get('Name', ''),
                                weight=float(row.get('Holding Percent', 0)) if row.get('Holding Percent') else None,
                                as_of_date=datetime.now().date()
                            )
                            self.session.add(holding)
                        
                        self.session.commit()
                        logger.info(f"Successfully stored {len(top_holdings)} holdings for {etf.symbol}")
                    else:
                        logger.info(f"No holdings data available for {etf.symbol}")
                else:
                    logger.info(f"No top_holdings attribute for {etf.symbol}")
                    
            except Exception as holdings_error:
                logger.warning(f"Could not retrieve holdings for {etf.symbol}: {holdings_error}")
                
        except Exception as e:
            logger.error(f"Error ingesting holdings for {etf.symbol}: {e}")
    
    def ingest_sector_allocations(self, etf: ETF) -> None:
        """
        Ingest ETF sector allocation data using funds_data.sector_weightings
        """
        try:
            ticker = yf.Ticker(etf.symbol)
            
            # Clear existing sector allocations for this ETF
            self.session.query(SectorAllocation).filter(SectorAllocation.etf_id == etf.id).delete()
            
            # Get sector weightings data from funds_data
            try:
                funds_data = ticker.funds_data
                if hasattr(funds_data, 'sector_weightings'):
                    sector_weightings = funds_data.sector_weightings
                    
                    # sector_weightings is a dictionary, not a DataFrame
                    if isinstance(sector_weightings, dict) and sector_weightings:
                        logger.info(f"Found {len(sector_weightings)} sector allocations for {etf.symbol}")
                        
                        for sector_name, weight in sector_weightings.items():
                            if weight is not None and weight > 0:
                                # Clean up sector name for display
                                clean_sector = sector_name.replace('_', ' ').title()
                                
                                allocation = SectorAllocation(
                                    etf_id=etf.id,
                                    sector_name=clean_sector,
                                    allocation_percentage=float(weight) * 100,  # Convert to percentage
                                    as_of_date=datetime.now().date()
                                )
                                self.session.add(allocation)
                        
                        self.session.commit()
                        logger.info(f"Successfully stored {len(sector_weightings)} sector allocations for {etf.symbol}")
                    else:
                        logger.info(f"No sector weightings data available for {etf.symbol}")
                else:
                    logger.info(f"No sector_weightings attribute for {etf.symbol}")
                    
            except Exception as sector_error:
                logger.warning(f"Could not retrieve sector weightings for {etf.symbol}: {sector_error}")
                
        except Exception as e:
            logger.error(f"Error ingesting sector allocations for {etf.symbol}: {e}")
    

    def ingest_fund_operations(self, etf: ETF) -> None:
        """
        Ingest ETF fund operations data using funds_data.fund_operations
        """
        try:
            ticker = yf.Ticker(etf.symbol)
            
            # Clear existing fund operations for this ETF
            self.session.query(FundOperations).filter(FundOperations.etf_id == etf.id).delete()
            
            # Get fund operations data from funds_data
            try:
                funds_data = ticker.funds_data
                if hasattr(funds_data, 'fund_operations'):
                    fund_ops = funds_data.fund_operations
                    
                    if isinstance(fund_ops, pd.DataFrame) and not fund_ops.empty:
                        logger.info(f"Found fund operations data for {etf.symbol}")
                        
                        operations = FundOperations(etf_id=etf.id, as_of_date=datetime.now().date())
                        
                        # Extract data from the DataFrame - column structure: [Fund, Category Average]
                        if etf.symbol in fund_ops.columns:
                            fund_col = fund_ops[etf.symbol]
                            
                            operations.annual_report_expense_ratio = self._safe_float(fund_col.get('Annual Report Expense Ratio'))
                            operations.annual_holdings_turnover = self._safe_float(fund_col.get('Annual Holdings Turnover'))
                            operations.total_net_assets = self._safe_float(fund_col.get('Total Net Assets'))
                            
                            # Category averages if available
                            if 'Category Average' in fund_ops.columns:
                                cat_col = fund_ops['Category Average']
                                operations.category_average_expense_ratio = self._safe_float(cat_col.get('Annual Report Expense Ratio'))
                                operations.category_average_turnover = self._safe_float(cat_col.get('Annual Holdings Turnover'))
                        
                        self.session.add(operations)
                        self.session.commit()
                        logger.info(f"Successfully stored fund operations for {etf.symbol}")
                    else:
                        logger.info(f"No fund operations data available for {etf.symbol}")
                else:
                    logger.info(f"No fund_operations attribute for {etf.symbol}")
                    
            except Exception as ops_error:
                logger.warning(f"Could not retrieve fund operations for {etf.symbol}: {ops_error}")
                
        except Exception as e:
            logger.error(f"Error ingesting fund operations for {etf.symbol}: {e}")
    
    def ingest_equity_metrics(self, etf: ETF) -> None:
        """
        Ingest ETF equity holdings metrics using funds_data.equity_holdings
        """
        try:
            ticker = yf.Ticker(etf.symbol)
            
            # Clear existing equity metrics for this ETF
            self.session.query(EquityMetrics).filter(EquityMetrics.etf_id == etf.id).delete()
            
            # Get equity holdings data from funds_data
            try:
                funds_data = ticker.funds_data
                if hasattr(funds_data, 'equity_holdings'):
                    equity_holdings = funds_data.equity_holdings
                    
                    if isinstance(equity_holdings, pd.DataFrame) and not equity_holdings.empty:
                        logger.info(f"Found equity metrics data for {etf.symbol}")
                        
                        metrics = EquityMetrics(etf_id=etf.id, as_of_date=datetime.now().date())
                        
                        # Extract data from the DataFrame
                        if etf.symbol in equity_holdings.columns:
                            fund_col = equity_holdings[etf.symbol]
                            
                            metrics.fund_price_earnings = self._safe_float(fund_col.get('Price/Earnings'))
                            metrics.fund_price_book = self._safe_float(fund_col.get('Price/Book'))
                            metrics.fund_price_sales = self._safe_float(fund_col.get('Price/Sales'))
                            metrics.fund_price_cashflow = self._safe_float(fund_col.get('Price/Cashflow'))
                            metrics.fund_median_market_cap = self._safe_float(fund_col.get('Median Market Cap'))
                            metrics.fund_geometric_mean_market_cap = self._safe_float(fund_col.get('Geometric Mean Market Cap'))
                            
                            # Category averages if available
                            if 'Category Average' in equity_holdings.columns:
                                cat_col = equity_holdings['Category Average']
                                metrics.category_price_earnings = self._safe_float(cat_col.get('Price/Earnings'))
                                metrics.category_price_book = self._safe_float(cat_col.get('Price/Book'))
                                metrics.category_price_sales = self._safe_float(cat_col.get('Price/Sales'))
                        
                        self.session.add(metrics)
                        self.session.commit()
                        logger.info(f"Successfully stored equity metrics for {etf.symbol}")
                    else:
                        logger.info(f"No equity holdings data available for {etf.symbol}")
                else:
                    logger.info(f"No equity_holdings attribute for {etf.symbol}")
                    
            except Exception as equity_error:
                logger.warning(f"Could not retrieve equity holdings for {etf.symbol}: {equity_error}")
                
        except Exception as e:
            logger.error(f"Error ingesting equity metrics for {etf.symbol}: {e}")
    
    def ingest_fund_overview(self, etf: ETF) -> None:
        """
        Ingest ETF fund overview and description using funds_data.fund_overview and funds_data.description
        """
        try:
            ticker = yf.Ticker(etf.symbol)
            
            # Clear existing fund overview for this ETF
            self.session.query(FundOverview).filter(FundOverview.etf_id == etf.id).delete()
            
            # Get fund overview data from funds_data
            try:
                funds_data = ticker.funds_data
                overview = FundOverview(etf_id=etf.id)
                
                # Get fund overview dict
                if hasattr(funds_data, 'fund_overview'):
                    fund_overview = funds_data.fund_overview
                    if isinstance(fund_overview, dict):
                        overview.category_name = fund_overview.get('categoryName')
                        overview.family = fund_overview.get('family')
                        overview.legal_type = fund_overview.get('legalType')
                
                # Get description
                if hasattr(funds_data, 'description'):
                    description = funds_data.description
                    if isinstance(description, str) and description:
                        overview.description = description
                
                self.session.add(overview)
                self.session.commit()
                logger.info(f"Successfully stored fund overview for {etf.symbol}")
                    
            except Exception as overview_error:
                logger.warning(f"Could not retrieve fund overview for {etf.symbol}: {overview_error}")
                
        except Exception as e:
            logger.error(f"Error ingesting fund overview for {etf.symbol}: {e}")
    
    def _safe_float(self, value) -> Optional[float]:
        """
        Safely convert value to float, handling None and invalid values
        """
        try:
            if value is None or pd.isna(value):
                return None
            return float(value)
        except (ValueError, TypeError):
            return None
    

    def ingest_single_etf(self, symbol: str, include_history: bool = True) -> bool:
        """
        Ingest all available data for a single ETF
        """
        logger.info(f"Starting ingestion for {symbol}")
        
        # Ingest basic info
        etf = self.ingest_etf_basic_info(symbol)
        if not etf:
            return False
        
        
        # Ingest price history
        if include_history:
            self.ingest_price_history(etf)
        
        # Ingest holdings (if available)
        self.ingest_holdings(etf)
        
        # Ingest sector allocations (if available)
        self.ingest_sector_allocations(etf)
        
        # Ingest fund operations (if available)
        self.ingest_fund_operations(etf)
        
        # Ingest equity metrics (if available)
        self.ingest_equity_metrics(etf)
        
        # Ingest fund overview and description (if available)
        self.ingest_fund_overview(etf)
        
        # Ultra-conservative delay to avoid rate limiting

        
        return True
    
    def ingest_popular_etfs(self, include_history: bool = True) -> None:
        """
        Ingest data for all popular ETFs
        """
        etfs = self.get_popular_etfs()
        total = len(etfs)
        
        logger.info(f"Starting ingestion of {total} popular ETFs")
        
        for i, symbol in enumerate(etfs, 1):
            logger.info(f"Processing {i}/{total}: {symbol}")
            
            success = self.ingest_single_etf(symbol, include_history)
            if success:
                logger.info(f"✓ Successfully processed {symbol}")
            else:
                logger.error(f"✗ Failed to process {symbol}")
            
            # Extra delay between ETFs to be very respectful to Yahoo Finance
            if i < total:  # Not the last one
                logger.info(f"Taking a break before next ETF ({i+1}/{total})...")

        
        logger.info("Completed ingestion of popular ETFs")

def main():
    """
    Main function to run ETF data ingestion
    """
    # Initialize database
    init_db()
    
    # Wait much longer before starting to avoid immediate rate limiting
    logger.info("Waiting 60 seconds before starting data ingestion...")

    
    # Create ingester
    ingester = ETFDataIngester()
    
    # Ingest popular ETFs
    ingester.ingest_popular_etfs(include_history=True)
    
    logger.info("ETF data ingestion completed!")

if __name__ == "__main__":
    main()
