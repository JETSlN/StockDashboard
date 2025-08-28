"""
Price API Controller

FastAPI router for price-related endpoints that expose the price service functions.
"""

from typing import List, Dict, Any, Union, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from datetime import date

from db.models import get_db
from services.price_service import get_price_history, get_latest_price
from services.fund_service import get_fund  # For fund existence check

router = APIRouter(
    prefix="/api/funds",
    tags=["prices"],
    responses={404: {"description": "Fund not found"}}
)


def _parse_symbol_or_id(symbol_or_id: str) -> Union[str, int]:
    """
    Parse path parameter to determine if it's a symbol (string) or ID (int)
    """
    # If it's all digits, treat as ID, otherwise as symbol
    if symbol_or_id.isdigit():
        return int(symbol_or_id)
    return symbol_or_id.upper()  # Normalize symbols to uppercase


@router.get("/{symbol_or_id}/prices", response_model=List[Dict[str, Any]])
async def get_fund_price_history(
    symbol_or_id: str = Path(..., description="ETF symbol (e.g., 'SPY') or ETF ID (e.g., '1')"),
    start: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Get price history for an ETF. Returns full history if no date filters provided.
    
    Args:
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (e.g., 1)
        start: Optional start date in YYYY-MM-DD format
        end: Optional end date in YYYY-MM-DD format
        
    Returns:
        List of price history dictionaries ordered by date (ascending)
        
    Raises:
        404: Fund not found
        400: Invalid date format
    """
    try:
        parsed_id = _parse_symbol_or_id(symbol_or_id)
        
        # Validate date formats if provided
        if start:
            try:
                # Validate date format
                date.fromisoformat(start)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid start date format: {start}. Use YYYY-MM-DD"
                )
        
        if end:
            try:
                # Validate date format
                date.fromisoformat(end)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid end date format: {end}. Use YYYY-MM-DD"
                )
        
        # Get price history
        price_history = get_price_history(db, parsed_id, start, end)
        
        # Check if the fund exists by checking if we got any results or if fund exists
        if not price_history:
            # Verify fund exists
            fund = get_fund(db, parsed_id)
            if not fund:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Fund not found: {symbol_or_id}"
                )
            # Fund exists but no price data for the date range
            return []
        
        return price_history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol_or_id}/prices/latest", response_model=Dict[str, Any])
async def get_fund_latest_price(
    symbol_or_id: str = Path(..., description="ETF symbol (e.g., 'SPY') or ETF ID (e.g., '1')"),
    db: Session = Depends(get_db)
):
    """
    Get the most recent price data for an ETF.
    
    Args:
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (e.g., 1)
        
    Returns:
        Latest price data dictionary
        
    Raises:
        404: Fund not found or no price data available
    """
    try:
        parsed_id = _parse_symbol_or_id(symbol_or_id)
        
        # Get latest price
        latest_price = get_latest_price(db, parsed_id)
        
        if not latest_price:
            # Check if fund exists
            fund = get_fund(db, parsed_id)
            if not fund:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Fund not found: {symbol_or_id}"
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"No price data available for fund: {symbol_or_id}"
                )
        
        return latest_price
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol_or_id}/prices/summary", response_model=Dict[str, Any])
async def get_fund_price_summary(
    symbol_or_id: str = Path(..., description="ETF symbol (e.g., 'SPY') or ETF ID (e.g., '1')"),
    db: Session = Depends(get_db)
):
    """
    Get price summary including latest price and recent history (last 30 days).
    Convenience endpoint that provides key price metrics.
    
    Args:
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (e.g., 1)
        
    Returns:
        Dictionary with latest price, recent history, and summary statistics
        
    Raises:
        404: Fund not found
    """
    try:
        parsed_id = _parse_symbol_or_id(symbol_or_id)
        
        # Check if fund exists
        fund = get_fund(db, parsed_id)
        if not fund:
            raise HTTPException(
                status_code=404, 
                detail=f"Fund not found: {symbol_or_id}"
            )
        
        # Get latest price
        latest_price = get_latest_price(db, parsed_id)
        
        # Get recent history (full history, we'll slice on the frontend if needed)
        price_history = get_price_history(db, parsed_id)
        
        # Calculate some basic statistics if we have price history
        stats = {}
        if price_history and len(price_history) > 0:
            prices = [p['close_price'] for p in price_history if p['close_price'] is not None]
            if prices:
                stats = {
                    "total_records": len(price_history),
                    "price_range": {
                        "min": min(prices),
                        "max": max(prices)
                    },
                    "date_range": {
                        "start": price_history[0]['date'],  # First record (chronological order)
                        "end": price_history[-1]['date']   # Last record
                    }
                }
        
        return {
            "fund_symbol": fund['symbol'],
            "fund_name": fund['name'],
            "latest_price": latest_price,
            "price_statistics": stats,
            "recent_history": price_history[-10:] if price_history else []  # Last 10 records
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

