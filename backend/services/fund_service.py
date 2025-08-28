"""
Fund Service - ETF fund data retrieval and insertion

All functions accept either symbol (str) or id (int) for ETF lookup.
Minimal filters, comprehensive data shaped to match the database schema.
"""

import re
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from db.models import ETF, ETFHolding, SectorAllocation, FundOverview, FundOperations, EquityMetrics
from db.ingest_yfinance import ETFDataIngester


def _get_etf_by_symbol_or_id(db: Session, symbol_or_id: Union[str, int]) -> Optional[ETF]:
    """
    Helper function to get ETF by symbol or ID
    """
    if isinstance(symbol_or_id, int):
        return db.query(ETF).filter(ETF.id == symbol_or_id).first()
    elif isinstance(symbol_or_id, str):
        return db.query(ETF).filter(ETF.symbol == symbol_or_id.upper()).first()
    else:
        return None


def get_fund(db: Session, symbol_or_id: Union[str, int]) -> Optional[Dict[str, Any]]:
    """
    Return one ETF row + attached one-to-ones (FundOverview, FundOperations, EquityMetrics).
    
    Args:
        db: Database session
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (int)
        
    Returns:
        Dict containing ETF data with nested relationships, or None if not found
    """
    # Query with eager loading of one-to-one relationships
    etf = db.query(ETF).options(
        joinedload(ETF.fund_overview),
        joinedload(ETF.fund_operations), 
        joinedload(ETF.equity_metrics)
    ).filter(
        ETF.id == symbol_or_id if isinstance(symbol_or_id, int) 
        else ETF.symbol == symbol_or_id.upper()
    ).first()
    
    if not etf:
        return None
    
    # Convert to dict with relationships
    result = {
        # Basic ETF data
        "id": etf.id,
        "symbol": etf.symbol,
        "name": etf.name,
        "category": etf.category,
        "family": etf.family,
        "exchange": etf.exchange,
        "full_exchange_name": etf.full_exchange_name,
        "currency": etf.currency,
        "country": etf.country,
        "legal_type": etf.legal_type,
        
        # Financial metrics
        "net_assets": etf.net_assets,
        "nav": etf.nav,
        "expense_ratio": etf.expense_ratio,
        "yield_rate": etf.yield_rate,
        "pe_ratio": etf.pe_ratio,
        "pb_ratio": etf.pb_ratio,
        "beta": etf.beta,
        
        # Performance metrics
        "ytd_return": etf.ytd_return,
        "three_year_return": etf.three_year_return,
        "five_year_return": etf.five_year_return,
        "inception_date": etf.inception_date.isoformat() if etf.inception_date else None,
        
        # Price info
        "current_price": etf.current_price,
        "day_high": etf.day_high,
        "day_low": etf.day_low,
        "previous_close": etf.previous_close,
        "market_cap": etf.market_cap,
        
        # Volume
        "volume": etf.volume,
        "average_volume": etf.average_volume,
        
        # 52-week performance
        "fifty_two_week_low": etf.fifty_two_week_low,
        "fifty_two_week_high": etf.fifty_two_week_high,
        "fifty_two_week_change_percent": etf.fifty_two_week_change_percent,
        
        # Technical indicators
        "fifty_day_average": etf.fifty_day_average,
        "two_hundred_day_average": etf.two_hundred_day_average,
        "fifty_day_average_change": etf.fifty_day_average_change,
        "fifty_day_average_change_percent": etf.fifty_day_average_change_percent,
        "two_hundred_day_average_change": etf.two_hundred_day_average_change,
        "two_hundred_day_average_change_percent": etf.two_hundred_day_average_change_percent,
        
        # Additional market data
        "regular_market_change": etf.regular_market_change,
        "regular_market_change_percent": etf.regular_market_change_percent,
        "dividend_yield": etf.dividend_yield,
        "net_expense_ratio": etf.net_expense_ratio,
        "trailing_annual_dividend_yield": etf.trailing_annual_dividend_yield,
        
        # Timestamps
        "created_at": etf.created_at.isoformat() if etf.created_at else None,
        "updated_at": etf.updated_at.isoformat() if etf.updated_at else None,
        "last_data_update": etf.last_data_update.isoformat() if etf.last_data_update else None,
        
        # One-to-one relationships
        "fund_overview": None,
        "fund_operations": None, 
        "equity_metrics": None
    }
    
    # Add fund overview if exists
    if etf.fund_overview:
        result["fund_overview"] = {
            "id": etf.fund_overview.id,
            "category_name": etf.fund_overview.category_name,
            "family": etf.fund_overview.family,
            "legal_type": etf.fund_overview.legal_type,
            "description": etf.fund_overview.description,
            "created_at": etf.fund_overview.created_at.isoformat() if etf.fund_overview.created_at else None,
            "updated_at": etf.fund_overview.updated_at.isoformat() if etf.fund_overview.updated_at else None
        }
    
    # Add fund operations if exists
    if etf.fund_operations:
        result["fund_operations"] = {
            "id": etf.fund_operations.id,
            "annual_report_expense_ratio": etf.fund_operations.annual_report_expense_ratio,
            "annual_holdings_turnover": etf.fund_operations.annual_holdings_turnover,
            "total_net_assets": etf.fund_operations.total_net_assets,
            "category_average_expense_ratio": etf.fund_operations.category_average_expense_ratio,
            "category_average_turnover": etf.fund_operations.category_average_turnover,
            "as_of_date": etf.fund_operations.as_of_date.isoformat() if etf.fund_operations.as_of_date else None,
            "created_at": etf.fund_operations.created_at.isoformat() if etf.fund_operations.created_at else None,
            "updated_at": etf.fund_operations.updated_at.isoformat() if etf.fund_operations.updated_at else None
        }
    
    # Add equity metrics if exists
    if etf.equity_metrics:
        result["equity_metrics"] = {
            "id": etf.equity_metrics.id,
            "fund_price_earnings": etf.equity_metrics.fund_price_earnings,
            "fund_price_book": etf.equity_metrics.fund_price_book,
            "fund_price_sales": etf.equity_metrics.fund_price_sales,
            "fund_price_cashflow": etf.equity_metrics.fund_price_cashflow,
            "fund_median_market_cap": etf.equity_metrics.fund_median_market_cap,
            "fund_geometric_mean_market_cap": etf.equity_metrics.fund_geometric_mean_market_cap,
            "category_price_earnings": etf.equity_metrics.category_price_earnings,
            "category_price_book": etf.equity_metrics.category_price_book,
            "category_price_sales": etf.equity_metrics.category_price_sales,
            "as_of_date": etf.equity_metrics.as_of_date.isoformat() if etf.equity_metrics.as_of_date else None,
            "created_at": etf.equity_metrics.created_at.isoformat() if etf.equity_metrics.created_at else None,
            "updated_at": etf.equity_metrics.updated_at.isoformat() if etf.equity_metrics.updated_at else None
        }
    
    return result


def get_fund_list(db: Session) -> List[Dict[str, Any]]:
    """
    Return all ETFs (id, symbol, name, category, family, expense_ratio, market_cap, etc.).
    
    Args:
        db: Database session
        
    Returns:
        List of dicts containing key ETF information for listing/selection
    """
    etfs = db.query(ETF).order_by(ETF.symbol).all()
    
    return [
        {
            "id": etf.id,
            "symbol": etf.symbol,
            "name": etf.name,
            "category": etf.category,
            "family": etf.family,
            "exchange": etf.exchange,
            "currency": etf.currency,
            "country": etf.country,
            "legal_type": etf.legal_type,
            
            # Key financial metrics for listing
            "expense_ratio": etf.expense_ratio,
            "market_cap": etf.market_cap,
            "net_assets": etf.net_assets,
            "nav": etf.nav,
            "current_price": etf.current_price,
            "yield_rate": etf.yield_rate,
            "ytd_return": etf.ytd_return,
            
            # Performance summary
            "three_year_return": etf.three_year_return,
            "five_year_return": etf.five_year_return,
            
            # 52-week performance
            "fifty_two_week_low": etf.fifty_two_week_low,
            "fifty_two_week_high": etf.fifty_two_week_high,
            "fifty_two_week_change_percent": etf.fifty_two_week_change_percent,
            
            # Volume indicators
            "volume": etf.volume,
            "average_volume": etf.average_volume,
            
            # Data freshness
            "last_data_update": etf.last_data_update.isoformat() if etf.last_data_update else None
        }
        for etf in etfs
    ]


def get_holdings(db: Session, symbol_or_id: Union[str, int]) -> List[Dict[str, Any]]:
    """
    Return ALL ETFHolding rows for this ETF (every as_of_date, no filters).
    
    Args:
        db: Database session
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (int)
        
    Returns:
        List of dicts containing all holdings data for the ETF
    """
    etf = _get_etf_by_symbol_or_id(db, symbol_or_id)
    if not etf:
        return []
    
    holdings = db.query(ETFHolding).filter(
        ETFHolding.etf_id == etf.id
    ).order_by(
        ETFHolding.as_of_date.desc(),
        ETFHolding.weight.desc()
    ).all()
    
    return [
        {
            "id": holding.id,
            "etf_id": holding.etf_id,
            "etf_symbol": etf.symbol,  # Include for convenience
            
            # Security identification
            "symbol": holding.symbol,
            "name": holding.name,
            
            # Position details
            "shares": holding.shares,
            "market_value": holding.market_value,
            "weight": holding.weight,
            
            # Classification
            "sector": holding.sector,
            "industry": holding.industry,
            "country": holding.country,
            "region": holding.region,
            "asset_class": holding.asset_class,
            "security_type": holding.security_type,
            
            # Metadata
            "as_of_date": holding.as_of_date.isoformat() if holding.as_of_date else None,
            "created_at": holding.created_at.isoformat() if holding.created_at else None,
            "updated_at": holding.updated_at.isoformat() if holding.updated_at else None
        }
        for holding in holdings
    ]


def get_sector_allocations(db: Session, symbol_or_id: Union[str, int]) -> List[Dict[str, Any]]:
    """
    Return ALL SectorAllocation rows for this ETF (every as_of_date, no filters).
    
    Args:
        db: Database session
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (int)
        
    Returns:
        List of dicts containing all sector allocation data for the ETF
    """
    etf = _get_etf_by_symbol_or_id(db, symbol_or_id)
    if not etf:
        return []
    
    sectors = db.query(SectorAllocation).filter(
        SectorAllocation.etf_id == etf.id
    ).order_by(
        SectorAllocation.as_of_date.desc(),
        SectorAllocation.allocation_percentage.desc()
    ).all()
    
    return [
        {
            "id": sector.id,
            "etf_id": sector.etf_id,
            "etf_symbol": etf.symbol,  # Include for convenience
            
            # Sector data
            "sector_name": sector.sector_name,
            "allocation_percentage": sector.allocation_percentage,
            
            # Metadata
            "as_of_date": sector.as_of_date.isoformat() if sector.as_of_date else None,
            "created_at": sector.created_at.isoformat() if sector.created_at else None
        }
        for sector in sectors
    ]


def _validate_symbol(symbol: str) -> str:
    """
    Validate and sanitize ETF symbol to prevent SQL injection and ensure valid format.
    
    Args:
        symbol: Raw symbol input
        
    Returns:
        Sanitized symbol string
        
    Raises:
        ValueError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    # Remove whitespace and convert to uppercase
    symbol = symbol.strip().upper()
    
    # Validate symbol format: 1-10 alphanumeric characters, possibly with single dots/hyphens
    # This covers most ETF symbols like SPY, QQQ, VTI, BRK.B, etc.
    # Prevent multiple consecutive special characters or SQL injection patterns
    if not re.match(r'^[A-Z0-9]+([.-][A-Z0-9]+)*$', symbol) or len(symbol) > 10:
        raise ValueError(f"Invalid symbol format: {symbol}. Must be 1-10 alphanumeric characters with optional single dots or hyphens.")
    
    return symbol


def insert_fund(db: Session, symbol: str, include_history: bool = True) -> Dict[str, Any]:
    """
    Insert a new ETF fund by symbol using the YFinance data ingester.
    
    Args:
        db: Database session
        symbol: ETF symbol (e.g., "SPY", "QQQ")
        include_history: Whether to include price history data (default: True)
        
    Returns:
        Dict containing the result status and fund data or error message
        
    Raises:
        ValueError: If symbol is invalid
        SQLAlchemyError: If database operation fails
    """
    try:
        # Validate and sanitize the symbol
        clean_symbol = _validate_symbol(symbol)
        
        # Check if fund already exists
        existing_fund = db.query(ETF).filter(ETF.symbol == clean_symbol).first()
        if existing_fund:
            return {
                "success": False,
                "message": f"Fund {clean_symbol} already exists",
                "fund": get_fund(db, clean_symbol)
            }
        
        # Create ingester instance (it will use the provided db session indirectly)
        ingester = ETFDataIngester()
        
        # Attempt to ingest the fund data
        success = ingester.ingest_single_etf(clean_symbol, include_history)
        
        if not success:
            return {
                "success": False,
                "message": f"Invalid symbol '{clean_symbol}'. Please ensure this is a valid ETF or mutual fund symbol.",
                "fund": None
            }
        
        # Refresh the session to get the newly inserted data
        db.commit()
        
        # Get the newly inserted fund data
        new_fund = get_fund(db, clean_symbol)
        
        if new_fund:
            return {
                "success": True,
                "message": f"Successfully inserted fund {clean_symbol}",
                "fund": new_fund
            }
        else:
            return {
                "success": False,
                "message": f"Fund {clean_symbol} was processed but could not be retrieved",
                "fund": None
            }
            
    except ValueError as e:
        # Symbol validation error
        return {
            "success": False,
            "message": f"Invalid symbol: {str(e)}",
            "fund": None
        }
    except SQLAlchemyError as e:
        # Database error
        db.rollback()
        return {
            "success": False,
            "message": f"Database error: {str(e)}",
            "fund": None
        }
    except Exception as e:
        # Unexpected error
        db.rollback()
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "fund": None
        }
