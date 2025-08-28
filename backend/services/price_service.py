"""
Price Service - Read-only ETF price data retrieval

All functions accept either symbol (str) or id (int) for ETF lookup.
Minimal filters focused on date ranges for price history.
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime, date
from sqlalchemy.orm import Session
from db.models import ETF, ETFPriceHistory


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


def get_price_history(
    db: Session, 
    symbol_or_id: Union[str, int], 
    start: Optional[str] = None, 
    end: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Return ETFPriceHistory ordered by date.
    Optional start/end are the ONLY filters (use when you truly need to bound the series).
    If omitted, return the full history.
    
    Args:
        db: Database session
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (int)
        start: Optional start date in YYYY-MM-DD format
        end: Optional end date in YYYY-MM-DD format
        
    Returns:
        List of dicts containing price history, ordered by date ascending
    """
    etf = _get_etf_by_symbol_or_id(db, symbol_or_id)
    if not etf:
        return []
    
    # Start with base query
    query = db.query(ETFPriceHistory).filter(ETFPriceHistory.etf_id == etf.id)
    
    # Apply date filters if provided
    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            query = query.filter(ETFPriceHistory.date >= start_date)
        except ValueError:
            # Invalid date format, skip filter
            pass
    
    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            query = query.filter(ETFPriceHistory.date <= end_date)
        except ValueError:
            # Invalid date format, skip filter
            pass
    
    # Order by date ascending (chronological)
    price_history = query.order_by(ETFPriceHistory.date.asc()).all()
    
    return [
        {
            "id": price.id,
            "etf_id": price.etf_id,
            "etf_symbol": etf.symbol,  # Include for convenience
            
            # Date
            "date": price.date.isoformat(),
            
            # OHLC data
            "open_price": price.open_price,
            "high_price": price.high_price,
            "low_price": price.low_price,
            "close_price": price.close_price,
            "adjusted_close": price.adjusted_close,
            
            # Volume
            "volume": price.volume,
            
            # Calculated metrics
            "daily_return": price.daily_return,
            "cumulative_return": price.cumulative_return,
            
            # Metadata
            "created_at": price.created_at.isoformat() if price.created_at else None
        }
        for price in price_history
    ]


def get_latest_price(db: Session, symbol_or_id: Union[str, int]) -> Optional[Dict[str, Any]]:
    """
    Return the most recent ETFPriceHistory row (close/adj_close/volume + date).
    
    Args:
        db: Database session
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (int)
        
    Returns:
        Dict containing the most recent price data, or None if not found
    """
    etf = _get_etf_by_symbol_or_id(db, symbol_or_id)
    if not etf:
        return None
    
    # Get most recent price record
    latest_price = db.query(ETFPriceHistory).filter(
        ETFPriceHistory.etf_id == etf.id
    ).order_by(ETFPriceHistory.date.desc()).first()
    
    if not latest_price:
        return None
    
    return {
        "id": latest_price.id,
        "etf_id": latest_price.etf_id,
        "etf_symbol": etf.symbol,  # Include for convenience
        
        # Date
        "date": latest_price.date.isoformat(),
        
        # OHLC data
        "open_price": latest_price.open_price,
        "high_price": latest_price.high_price,
        "low_price": latest_price.low_price,
        "close_price": latest_price.close_price,
        "adjusted_close": latest_price.adjusted_close,
        
        # Volume
        "volume": latest_price.volume,
        
        # Calculated metrics
        "daily_return": latest_price.daily_return,
        "cumulative_return": latest_price.cumulative_return,
        
        # Metadata
        "created_at": latest_price.created_at.isoformat() if latest_price.created_at else None
    }

