#!/usr/bin/env python3
"""
Quick test runner for Stock Dashboard API Controllers

Usage:
    python run_tests.py               # Run all tests
    python run_tests.py fund          # Run only fund controller tests
    python run_tests.py price         # Run only price controller tests
"""

import sys
import argparse
from test_fund_controller import run_fund_controller_tests
from test_price_controller import run_price_controller_tests
from test_all_controllers import run_all_controller_tests


def main():
    parser = argparse.ArgumentParser(description='Run Stock Dashboard API Controller Tests')
    parser.add_argument('controller', nargs='?', choices=['fund', 'price', 'all'], 
                        default='all', help='Controller to test (default: all)')
    parser.add_argument('--url', default='http://localhost:8000', 
                        help='Base URL for API (default: http://localhost:8000)')
    
    args = parser.parse_args()
    
    print(f"🧪 Running {args.controller.upper()} controller tests against {args.url}")
    print("=" * 80)
    
    if args.controller == 'fund':
        print("🏛️  TESTING FUND CONTROLLER ONLY")
        results = run_fund_controller_tests()
        passed = len([r for r in results if r["status"] == "PASSED"])
        total = len(results)
        print(f"\n🎯 FUND CONTROLLER RESULT: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
    elif args.controller == 'price':
        print("📈 TESTING PRICE CONTROLLER ONLY")
        results = run_price_controller_tests()
        passed = len([r for r in results if r["status"] == "PASSED"])
        total = len(results)
        print(f"\n🎯 PRICE CONTROLLER RESULT: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
    else:
        print("🚀 TESTING ALL CONTROLLERS")
        summary = run_all_controller_tests()
        print(f"\n🎯 FINAL RESULT: {summary['passed']}/{summary['total_tests']} tests passed ({summary['success_rate']:.1f}%)")
    
    print("\n✅ Testing complete!")


if __name__ == "__main__":
    main()

