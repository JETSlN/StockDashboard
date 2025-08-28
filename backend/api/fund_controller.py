"""
Fund API Controller

FastAPI router for fund-related endpoints that expose the fund service functions.
"""

from typing import List, Dict, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.models import get_db
from services.fund_service import get_fund, get_fund_list, get_holdings, get_sector_allocations, insert_fund

router = APIRouter(
    prefix="/api/funds",
    tags=["funds"],
    responses={404: {"description": "Fund not found"}}
)


class InsertFundRequest(BaseModel):
    """Request model for inserting a new fund"""
    symbol: str
    include_history: bool = True


def _parse_symbol_or_id(symbol_or_id: str) -> Union[str, int]:
    """
    Parse path parameter to determine if it's a symbol (string) or ID (int)
    """
    # If it's all digits, treat as ID, otherwise as symbol
    if symbol_or_id.isdigit():
        return int(symbol_or_id)
    return symbol_or_id.upper()  # Normalize symbols to uppercase


@router.get("/", response_model=List[Dict[str, Any]])
async def list_funds(db: Session = Depends(get_db)):
    """
    Get list of all ETFs with key information for listings/selection.
    
    Returns:
        List of ETF dictionaries with essential data (id, symbol, name, price, etc.)
    """
    try:
        funds = get_fund_list(db)
        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol_or_id}", response_model=Dict[str, Any])
async def get_fund_details(
    symbol_or_id: str = Path(..., description="ETF symbol (e.g., 'SPY') or ETF ID (e.g., '1')"),
    db: Session = Depends(get_db)
):
    """
    Get detailed fund information including relationships (fund overview, operations, metrics).
    
    Args:
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (e.g., 1)
        
    Returns:
        Complete ETF data dictionary with nested relationships
        
    Raises:
        404: Fund not found
    """
    try:
        parsed_id = _parse_symbol_or_id(symbol_or_id)
        fund = get_fund(db, parsed_id)
        
        if not fund:
            raise HTTPException(
                status_code=404, 
                detail=f"Fund not found: {symbol_or_id}"
            )
        
        return fund
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol_or_id}/holdings", response_model=List[Dict[str, Any]])
async def get_fund_holdings(
    symbol_or_id: str = Path(..., description="ETF symbol (e.g., 'SPY') or ETF ID (e.g., '1')"),
    db: Session = Depends(get_db)
):
    """
    Get all holdings for an ETF (every as_of_date, no filters).
    
    Args:
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (e.g., 1)
        
    Returns:
        List of holding dictionaries ordered by date (desc) and weight (desc)
        
    Raises:
        404: Fund not found
    """
    try:
        parsed_id = _parse_symbol_or_id(symbol_or_id)
        holdings = get_holdings(db, parsed_id)
        
        # Check if the fund exists by trying to get it
        fund = get_fund(db, parsed_id)
        if not fund:
            raise HTTPException(
                status_code=404, 
                detail=f"Fund not found: {symbol_or_id}"
            )
        
        return holdings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol_or_id}/sectors", response_model=List[Dict[str, Any]])
async def get_fund_sector_allocations(
    symbol_or_id: str = Path(..., description="ETF symbol (e.g., 'SPY') or ETF ID (e.g., '1')"),
    db: Session = Depends(get_db)
):
    """
    Get all sector allocations for an ETF (every as_of_date, no filters).
    
    Args:
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (e.g., 1)
        
    Returns:
        List of sector allocation dictionaries ordered by date (desc) and percentage (desc)
        
    Raises:
        404: Fund not found
    """
    try:
        parsed_id = _parse_symbol_or_id(symbol_or_id)
        sectors = get_sector_allocations(db, parsed_id)
        
        # Check if the fund exists by trying to get it
        fund = get_fund(db, parsed_id)
        if not fund:
            raise HTTPException(
                status_code=404, 
                detail=f"Fund not found: {symbol_or_id}"
            )
        
        return sectors
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol_or_id}/summary", response_model=Dict[str, Any])
async def get_fund_summary(
    symbol_or_id: str = Path(..., description="ETF symbol (e.g., 'SPY') or ETF ID (e.g., '1')"),
    db: Session = Depends(get_db)
):
    """
    Get fund summary with basic info, top holdings, and top sectors.
    Convenience endpoint that combines multiple service calls.
    
    Args:
        symbol_or_id: ETF symbol (e.g., "SPY") or ETF ID (e.g., 1)
        
    Returns:
        Dictionary with fund details, top 5 holdings, and top 5 sectors
        
    Raises:
        404: Fund not found
    """
    try:
        parsed_id = _parse_symbol_or_id(symbol_or_id)
        
        # Get fund details
        fund = get_fund(db, parsed_id)
        if not fund:
            raise HTTPException(
                status_code=404, 
                detail=f"Fund not found: {symbol_or_id}"
            )
        
        # Get top holdings and sectors
        holdings = get_holdings(db, parsed_id)
        sectors = get_sector_allocations(db, parsed_id)
        
        return {
            "fund": fund,
            "top_holdings": holdings[:5],  # Top 5 holdings
            "top_sectors": sectors[:5],    # Top 5 sectors
            "total_holdings": len(holdings),
            "total_sectors": len(sectors)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/", response_model=Dict[str, Any])
async def insert_new_fund(
    request: InsertFundRequest,
    db: Session = Depends(get_db)
):
    """
    Insert a new ETF fund by symbol.
    
    This endpoint fetches comprehensive ETF data from Yahoo Finance and stores it in the database.
    It includes basic fund information, price history, holdings, sector allocations, and other metrics.
    
    Args:
        request: InsertFundRequest containing symbol and optional include_history flag
        
    Returns:
        Dictionary with success status, message, and fund data (if successful)
        
    Raises:
        400: Invalid symbol format or fund already exists
        422: Data retrieval failed (symbol may not exist)
        500: Internal server error
    """
    try:
        result = insert_fund(db, request.symbol, request.include_history)
        
        if result["success"]:
            # Successfully inserted
            return result
        else:
            # Failed to insert - determine appropriate HTTP status
            if "already exists" in result["message"]:
                raise HTTPException(status_code=400, detail=result["message"])
            elif "Invalid symbol" in result["message"]:
                raise HTTPException(status_code=400, detail=result["message"])
            elif "Failed to retrieve data" in result["message"]:
                raise HTTPException(status_code=422, detail=result["message"])
            else:
                raise HTTPException(status_code=500, detail=result["message"])
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

