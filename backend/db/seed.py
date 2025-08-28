"""
Database seeding script for Stock Dashboard

This script loads demo/sample data into the database for development and testing purposes.
"""

import os
import sys
from datetime import datetime, timedelta
import logging

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models import init_db, SessionLocal, ETF, ETFPriceHistory
from db.ingest_yfinance import ETFDataIngester

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_sample_etfs():
    """
    Create sample ETF data for development/demo purposes
    """
    session = SessionLocal()
    
    try:
        # Define a small set of popular ETFs for demo
        demo_etfs = [
            {
                'symbol': 'SPY',
                'name': 'SPDR S&P 500 ETF Trust',
                'category': 'Large Blend',
                'expense_ratio': 0.0945,
                'net_assets': 400000000000.0,  # $400B
                'summary': 'The SPDR S&P 500 ETF Trust seeks to provide investment results that correspond to the price and yield performance of the S&P 500 Index.'
            },
            {
                'symbol': 'QQQ',
                'name': 'Invesco QQQ Trust',
                'category': 'Large Growth',
                'expense_ratio': 0.20,
                'net_assets': 200000000000.0,  # $200B
                'summary': 'The Invesco QQQ Trust tracks the Nasdaq-100 Index, which includes 100 of the largest domestic and international non-financial companies listed on the Nasdaq Stock Market.'
            },
            {
                'symbol': 'VTI',
                'name': 'Vanguard Total Stock Market ETF',
                'category': 'Large Blend',
                'expense_ratio': 0.03,
                'net_assets': 350000000000.0,  # $350B
                'summary': 'The Vanguard Total Stock Market ETF seeks to track the performance of the CRSP US Total Market Index, which measures the investment return of the overall stock market.'
            },
            {
                'symbol': 'BND',
                'name': 'Vanguard Total Bond Market ETF',
                'category': 'Intermediate Core Bond',
                'expense_ratio': 0.035,
                'net_assets': 100000000000.0,  # $100B
                'summary': 'The Vanguard Total Bond Market ETF seeks to track the performance of the Bloomberg Aggregate Float Adjusted Index.'
            },
            {
                'symbol': 'VEA',
                'name': 'Vanguard FTSE Developed Markets ETF',
                'category': 'Foreign Large Blend',
                'expense_ratio': 0.05,
                'net_assets': 80000000000.0,  # $80B
                'summary': 'The Vanguard FTSE Developed Markets ETF seeks to track the performance of the FTSE Developed All Cap ex US Index.'
            }
        ]
        
        for etf_data in demo_etfs:
            # Check if ETF already exists
            existing = session.query(ETF).filter(ETF.symbol == etf_data['symbol']).first()
            if existing:
                logger.info(f"ETF {etf_data['symbol']} already exists, skipping...")
                continue
            
            etf = ETF(
                symbol=etf_data['symbol'],
                name=etf_data['name'],
                category=etf_data['category'],
                expense_ratio=etf_data['expense_ratio'],
                net_assets=etf_data['net_assets'],
                summary=etf_data['summary'],
                exchange='NASDAQ' if etf_data['symbol'] in ['QQQ'] else 'NYSE',
                currency='USD',
                country='US',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            session.add(etf)
            logger.info(f"Added demo ETF: {etf_data['symbol']}")
        
        session.commit()
        logger.info("Successfully created demo ETFs")
        
    except Exception as e:
        logger.error(f"Error creating demo ETFs: {e}")
        session.rollback()
    finally:
        session.close()

def create_sample_price_data():
    """
    Create sample price history data for demo ETFs
    """
    session = SessionLocal()
    
    try:
        # Get demo ETFs
        etfs = session.query(ETF).limit(5).all()
        
        for etf in etfs:
            # Check if price data already exists
            existing_count = session.query(ETFPriceHistory).filter(ETFPriceHistory.etf_id == etf.id).count()
            if existing_count > 0:
                logger.info(f"Price data for {etf.symbol} already exists, skipping...")
                continue
            
            # Generate sample price data for the last 30 days
            base_price = 100.0  # Starting price
            
            for i in range(30):
                date = datetime.now().date() - timedelta(days=i)
                
                # Simple random walk for demo data
                import random
                daily_change = random.uniform(-0.02, 0.02)  # ±2% daily change
                base_price *= (1 + daily_change)
                
                price_data = ETFPriceHistory(
                    etf_id=etf.id,
                    date=date,
                    open_price=base_price * random.uniform(0.995, 1.005),
                    high_price=base_price * random.uniform(1.005, 1.02),
                    low_price=base_price * random.uniform(0.98, 0.995),
                    close_price=base_price,
                    volume=random.randint(1000000, 10000000),
                    created_at=datetime.utcnow()
                )
                
                session.add(price_data)
            
            logger.info(f"Added demo price data for {etf.symbol}")
        
        session.commit()
        logger.info("Successfully created demo price data")
        
    except Exception as e:
        logger.error(f"Error creating demo price data: {e}")
        session.rollback()
    finally:
        session.close()

def seed_with_real_data():
    """
    Seed database with real ETF data using the yfinance ingester
    """
    logger.info("Seeding database with real ETF data...")
    
    # Use a smaller subset for seeding
    seed_etfs = ['SPY', 'QQQ', 'VOO', 'VTI', 'IVV', 'IEMG', 'VEA', 'AGG', 'VWO', 'EFA']
    
    ingester = ETFDataIngester()
    
    for symbol in seed_etfs:
        logger.info(f"Seeding real data for {symbol}")
        success = ingester.ingest_single_etf(symbol, include_history=True)
        if success:
            logger.info(f"✓ Successfully seeded {symbol}")
        else:
            logger.error(f"✗ Failed to seed {symbol}")

def clear_database():
    """
    Clear all data from the database (use with caution!)
    """
    session = SessionLocal()
    
    try:
        # Delete all records (cascading deletes will handle related tables)
        session.query(ETFPriceHistory).delete()
        session.query(ETF).delete()
        
        session.commit()
        logger.info("Database cleared successfully")
        
    except Exception as e:
        logger.error(f"Error clearing database: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    """
    Main seeding function
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed the Stock Dashboard database')
    parser.add_argument('--mode', choices=['demo', 'real', 'clear'], default='demo',
                       help='Seeding mode: demo (sample data), real (from yfinance), or clear (remove all data)')
    parser.add_argument('--init-db', action='store_true', help='Initialize database tables first')
    
    args = parser.parse_args()
    
    # Initialize database if requested
    if args.init_db:
        logger.info("Initializing database...")
        init_db()
    
    # Execute based on mode
    if args.mode == 'clear':
        logger.info("Clearing database...")
        clear_database()
    elif args.mode == 'demo':
        logger.info("Seeding with demo data...")
        create_sample_etfs()
        create_sample_price_data()
    elif args.mode == 'real':
        logger.info("Seeding with real data...")
        seed_with_real_data()
    
    logger.info("Seeding completed!")

if __name__ == "__main__":
    main()

