"""
Test suite for Fund Controller API endpoints

Tests all fund-related API endpoints defined in fund_controller.py
"""

import requests
import json
from typing import Dict, List, Any


class TestFundController:
    """Test class for Fund Controller endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    def _test_endpoint(self, method: str, endpoint: str, description: str, 
                      expected_status: int = 200, expected_keys: List[str] = None,
                      should_be_list: bool = None) -> bool:
        """
        Test a single endpoint and validate response
        """
        try:
            print(f"\n🔍 Testing: {description}")
            print(f"   URL: {method} {self.base_url}{endpoint}")
            
            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            print(f"   Status Code: {response.status_code}")
            
            # Check status code
            if response.status_code != expected_status:
                print(f"   ❌ FAILED: Expected {expected_status}, got {response.status_code}")
                if response.status_code >= 400:
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                    except:
                        print(f"   Raw error: {response.text[:200]}")
                self.test_results.append({
                    "test": description,
                    "status": "FAILED",
                    "reason": f"Status code mismatch: {response.status_code} != {expected_status}"
                })
                return False
            
            # Parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"   ❌ FAILED: Invalid JSON response")
                self.test_results.append({
                    "test": description,
                    "status": "FAILED",
                    "reason": "Invalid JSON response"
                })
                return False
            
            # Validate response type
            if should_be_list is not None:
                if should_be_list and not isinstance(data, list):
                    print(f"   ❌ FAILED: Expected list, got {type(data)}")
                    self.test_results.append({
                        "test": description,
                        "status": "FAILED",
                        "reason": f"Expected list, got {type(data)}"
                    })
                    return False
                elif not should_be_list and not isinstance(data, dict):
                    print(f"   ❌ FAILED: Expected dict, got {type(data)}")
                    self.test_results.append({
                        "test": description,
                        "status": "FAILED",
                        "reason": f"Expected dict, got {type(data)}"
                    })
                    return False
            
            # Validate expected keys
            if expected_keys and isinstance(data, dict):
                missing_keys = [key for key in expected_keys if key not in data]
                if missing_keys:
                    print(f"   ⚠️  Missing keys: {missing_keys}")
                else:
                    print(f"   ✅ All expected keys present: {expected_keys}")
            elif expected_keys and isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, dict):
                    missing_keys = [key for key in expected_keys if key not in first_item]
                    if missing_keys:
                        print(f"   ⚠️  Missing keys in first item: {missing_keys}")
                    else:
                        print(f"   ✅ All expected keys present in list items")
            
            # Show success info
            if isinstance(data, list):
                print(f"   ✅ SUCCESS: Returned {len(data)} items")
            elif isinstance(data, dict):
                print(f"   ✅ SUCCESS: Returned dict with {len(data)} keys")
                
                # Show some useful info
                if 'symbol' in data and 'name' in data:
                    print(f"   📊 Fund: {data['symbol']} - {data['name'][:50]}")
                elif 'fund' in data and isinstance(data['fund'], dict):
                    fund_info = data['fund']
                    print(f"   📊 Summary for: {fund_info.get('symbol', 'N/A')} - {fund_info.get('name', 'N/A')[:30]}")
            
            self.test_results.append({
                "test": description,
                "status": "PASSED",
                "data_type": type(data).__name__,
                "data_size": len(data) if isinstance(data, (list, dict)) else 0
            })
            return True
            
        except requests.exceptions.ConnectionError:
            print(f"   ❌ FAILED: Connection error - is server running on {self.base_url}?")
            self.test_results.append({
                "test": description,
                "status": "FAILED",
                "reason": "Connection error"
            })
            return False
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)[:100]}")
            self.test_results.append({
                "test": description,
                "status": "FAILED",
                "reason": str(e)[:100]
            })
            return False

    def test_all_fund_endpoints(self):
        """Test all fund controller endpoints"""
        print("🧪 TESTING FUND CONTROLLER ENDPOINTS")
        print("=" * 80)
        
        # Test 1: List all funds
        self._test_endpoint(
            "GET", "/api/funds/", 
            "List all funds",
            expected_status=200,
            expected_keys=["id", "symbol", "name", "current_price"],
            should_be_list=True
        )
        
        # Test 2: Get fund details by symbol
        self._test_endpoint(
            "GET", "/api/funds/SPY",
            "Get SPY fund details by symbol",
            expected_status=200,
            expected_keys=["id", "symbol", "name", "fund_overview", "fund_operations", "equity_metrics"],
            should_be_list=False
        )
        
        # Test 3: Get fund details by ID
        self._test_endpoint(
            "GET", "/api/funds/1",
            "Get fund details by ID (1)",
            expected_status=200,
            expected_keys=["id", "symbol", "name"],
            should_be_list=False
        )
        
        # Test 4: Get fund holdings
        self._test_endpoint(
            "GET", "/api/funds/SPY/holdings",
            "Get SPY holdings",
            expected_status=200,
            should_be_list=True
        )
        
        # Test 5: Get fund sector allocations
        self._test_endpoint(
            "GET", "/api/funds/SPY/sectors",
            "Get SPY sector allocations",
            expected_status=200,
            should_be_list=True
        )
        
        # Test 6: Get fund summary
        self._test_endpoint(
            "GET", "/api/funds/SPY/summary",
            "Get SPY summary",
            expected_status=200,
            expected_keys=["fund", "top_holdings", "top_sectors", "total_holdings", "total_sectors"],
            should_be_list=False
        )
        
        # Test 7: Test other fund symbols
        self._test_endpoint(
            "GET", "/api/funds/QQQ",
            "Get QQQ fund details",
            expected_status=200,
            expected_keys=["id", "symbol", "name"],
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/VOO/holdings",
            "Get VOO holdings",
            expected_status=200,
            should_be_list=True
        )
        
        # Test 8: Error cases - Invalid fund
        self._test_endpoint(
            "GET", "/api/funds/INVALID",
            "Test invalid fund symbol (should return 404)",
            expected_status=404,
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/999999",
            "Test invalid fund ID (should return 404)",
            expected_status=404,
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/INVALID/holdings",
            "Test holdings for invalid fund (should return 404)",
            expected_status=404,
            should_be_list=False
        )

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 FUND CONTROLLER TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = [r for r in self.test_results if r["status"] == "PASSED"]
        failed_tests = [r for r in self.test_results if r["status"] == "FAILED"]
        
        print(f"✅ Passed: {len(passed_tests)}")
        print(f"❌ Failed: {len(failed_tests)}")
        print(f"📈 Success Rate: {(len(passed_tests) / len(self.test_results)) * 100:.1f}%")
        
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['reason']}")
        
        print("\n✅ PASSED TESTS:")
        for test in passed_tests:
            print(f"   • {test['test']}")
        
        print("=" * 80)


def run_fund_controller_tests():
    """Run all fund controller tests"""
    tester = TestFundController()
    tester.test_all_fund_endpoints()
    tester.print_summary()
    return tester.test_results


if __name__ == "__main__":
    run_fund_controller_tests()

