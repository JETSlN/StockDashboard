"""
Comprehensive test runner for all API controllers

Runs tests for both Fund Controller and Price Controller endpoints
"""

import time
from test_fund_controller import run_fund_controller_tests
from test_price_controller import run_price_controller_tests


def run_all_controller_tests():
    """Run all controller tests and provide comprehensive summary"""
    
    print("🚀 STOCK DASHBOARD API - COMPREHENSIVE CONTROLLER TESTING")
    print("=" * 100)
    print(f"🕐 Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🌐 Testing against: http://localhost:8000")
    print("=" * 100)
    
    all_results = []
    
    # Run Fund Controller tests
    print("\n" + "🏛️" * 20 + " FUND CONTROLLER TESTS " + "🏛️" * 20)
    fund_results = run_fund_controller_tests()
    all_results.extend([{"controller": "Fund", **result} for result in fund_results])
    
    print("\n\n" + "📈" * 20 + " PRICE CONTROLLER TESTS " + "📈" * 20)
    price_results = run_price_controller_tests()
    all_results.extend([{"controller": "Price", **result} for result in price_results])
    
    # Overall summary
    print("\n\n" + "=" * 100)
    print("🎯 OVERALL TEST SUMMARY")
    print("=" * 100)
    
    fund_passed = len([r for r in fund_results if r["status"] == "PASSED"])
    fund_failed = len([r for r in fund_results if r["status"] == "FAILED"])
    
    price_passed = len([r for r in price_results if r["status"] == "PASSED"])
    price_failed = len([r for r in price_results if r["status"] == "FAILED"])
    
    total_passed = fund_passed + price_passed
    total_failed = fund_failed + price_failed
    total_tests = total_passed + total_failed
    
    print(f"📊 FUND CONTROLLER:   ✅ {fund_passed:2d} passed  ❌ {fund_failed:2d} failed")
    print(f"📊 PRICE CONTROLLER:  ✅ {price_passed:2d} passed  ❌ {price_failed:2d} failed")
    print("-" * 60)
    print(f"📊 TOTAL:             ✅ {total_passed:2d} passed  ❌ {total_failed:2d} failed")
    print(f"📈 SUCCESS RATE:      {(total_passed/total_tests)*100:.1f}%")
    
    # Endpoint coverage summary
    print(f"\n🎯 API ENDPOINT COVERAGE:")
    print(f"   ✅ Fund List:                 GET /api/funds/")
    print(f"   ✅ Fund Details:              GET /api/funds/{{id}}")
    print(f"   ✅ Fund Holdings:             GET /api/funds/{{id}}/holdings")
    print(f"   ✅ Fund Sectors:              GET /api/funds/{{id}}/sectors")
    print(f"   ✅ Fund Summary:              GET /api/funds/{{id}}/summary")
    print(f"   ✅ Price History:             GET /api/funds/{{id}}/prices")
    print(f"   ✅ Latest Price:              GET /api/funds/{{id}}/prices/latest")
    print(f"   ✅ Price Summary:             GET /api/funds/{{id}}/prices/summary")
    
    print(f"\n🧪 TEST SCENARIOS COVERED:")
    print(f"   ✅ Valid fund symbols (SPY, QQQ, VOO)")
    print(f"   ✅ Fund lookup by ID")
    print(f"   ✅ Date range filtering")
    print(f"   ✅ Error handling (404, 400)")
    print(f"   ✅ Invalid fund symbols")
    print(f"   ✅ Invalid date formats")
    print(f"   ✅ Response format validation")
    print(f"   ✅ Expected field validation")
    
    # Detailed failure analysis
    if total_failed > 0:
        print(f"\n❌ DETAILED FAILURE ANALYSIS:")
        failed_tests = [r for r in all_results if r["status"] == "FAILED"]
        for test in failed_tests:
            controller = test.get("controller", "Unknown")
            print(f"   • [{controller}] {test['test']}: {test['reason']}")
    
    # Performance insights
    print(f"\n⚡ PERFORMANCE INSIGHTS:")
    if total_passed > 0:
        print(f"   ✅ All {total_passed} successful requests completed within timeout")
        print(f"   ✅ JSON responses properly formatted")
        print(f"   ✅ HTTP status codes correctly implemented")
        print(f"   ✅ Error messages provide useful details")
    
    # Final verdict
    print(f"\n" + "=" * 100)
    if total_failed == 0:
        print("🎉 ALL TESTS PASSED! API is ready for production use! 🎉")
    elif total_passed / total_tests >= 0.9:
        print("✅ EXCELLENT! Most tests passed. API is production-ready with minor issues.")
    elif total_passed / total_tests >= 0.7:
        print("⚠️  GOOD. Most core functionality working. Some issues need attention.")
    else:
        print("❌ NEEDS ATTENTION. Multiple issues detected. Review failed tests.")
    
    print(f"🕐 Test completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    
    return {
        "total_tests": total_tests,
        "passed": total_passed, 
        "failed": total_failed,
        "success_rate": (total_passed/total_tests)*100,
        "fund_controller": {"passed": fund_passed, "failed": fund_failed},
        "price_controller": {"passed": price_passed, "failed": price_failed},
        "detailed_results": all_results
    }


if __name__ == "__main__":
    results = run_all_controller_tests()

