"""
Test suite for Price Controller API endpoints

Tests all price-related API endpoints defined in price_controller.py
"""

import requests
import json
from typing import Dict, List, Any


class TestPriceController:
    """Test class for Price Controller endpoints"""
    
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
                response = requests.get(f"{self.base_url}{endpoint}", timeout=15)
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
                # Show date range for price history
                if len(data) > 0 and 'date' in data[0]:
                    print(f"   📅 Date range: {data[0]['date']} to {data[-1]['date']}")
            elif isinstance(data, dict):
                print(f"   ✅ SUCCESS: Returned dict with {len(data)} keys")
                
                # Show useful price info
                if 'date' in data and 'close_price' in data:
                    print(f"   💰 Price: ${data['close_price']} on {data['date']}")
                elif 'latest_price' in data and isinstance(data['latest_price'], dict):
                    latest = data['latest_price']
                    if 'close_price' in latest and 'date' in latest:
                        print(f"   💰 Latest Price: ${latest['close_price']} on {latest['date']}")
                elif 'fund_symbol' in data:
                    print(f"   📊 Price summary for: {data['fund_symbol']}")
            
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

    def test_all_price_endpoints(self):
        """Test all price controller endpoints"""
        print("🧪 TESTING PRICE CONTROLLER ENDPOINTS")
        print("=" * 80)
        
        # Test 1: Get latest price by symbol
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices/latest", 
            "Get SPY latest price",
            expected_status=200,
            expected_keys=["date", "close_price", "adjusted_close", "volume"],
            should_be_list=False
        )
        
        # Test 2: Get latest price by ID
        self._test_endpoint(
            "GET", "/api/funds/1/prices/latest",
            "Get latest price by fund ID (1)",
            expected_status=200,
            expected_keys=["date", "close_price", "volume"],
            should_be_list=False
        )
        
        # Test 3: Get full price history
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices",
            "Get SPY full price history",
            expected_status=200,
            expected_keys=["date", "close_price", "open_price", "high_price", "low_price"],
            should_be_list=True
        )
        
        # Test 4: Get price history with date range
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices?start=2024-01-01&end=2024-01-31",
            "Get SPY price history for January 2024",
            expected_status=200,
            expected_keys=["date", "close_price"],
            should_be_list=True
        )
        
        # Test 5: Get price history with only start date
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices?start=2024-12-01",
            "Get SPY price history from December 2024",
            expected_status=200,
            should_be_list=True
        )
        
        # Test 6: Get price history with only end date
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices?end=2024-02-29",
            "Get SPY price history until February 2024",
            expected_status=200,
            should_be_list=True
        )
        
        # Test 7: Get price summary
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices/summary",
            "Get SPY price summary",
            expected_status=200,
            expected_keys=["fund_symbol", "fund_name", "latest_price", "price_statistics", "recent_history"],
            should_be_list=False
        )
        
        # Test 8: Test other fund symbols
        self._test_endpoint(
            "GET", "/api/funds/QQQ/prices/latest",
            "Get QQQ latest price",
            expected_status=200,
            expected_keys=["date", "close_price"],
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/VOO/prices/summary",
            "Get VOO price summary",
            expected_status=200,
            expected_keys=["fund_symbol", "latest_price"],
            should_be_list=False
        )
        
        # Test 9: Test year-to-date price history
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices?start=2024-01-01",
            "Get SPY YTD price history (2024)",
            expected_status=200,
            should_be_list=True
        )
        
        # Test 10: Error cases - Invalid dates
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices?start=invalid-date",
            "Test invalid start date format (should return 400)",
            expected_status=400,
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices?end=2024-13-45",
            "Test invalid end date (should return 400)",
            expected_status=400,
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/SPY/prices?start=2024-12-01&end=invalid",
            "Test invalid date range (should return 400)",
            expected_status=400,
            should_be_list=False
        )
        
        # Test 11: Error cases - Invalid fund
        self._test_endpoint(
            "GET", "/api/funds/INVALID/prices/latest",
            "Test latest price for invalid fund (should return 404)",
            expected_status=404,
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/999999/prices",
            "Test price history for invalid fund ID (should return 404)",
            expected_status=404,
            should_be_list=False
        )
        
        self._test_endpoint(
            "GET", "/api/funds/NONEXISTENT/prices/summary",
            "Test price summary for invalid fund (should return 404)",
            expected_status=404,
            should_be_list=False
        )

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 PRICE CONTROLLER TEST SUMMARY")
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


def run_price_controller_tests():
    """Run all price controller tests"""
    tester = TestPriceController()
    tester.test_all_price_endpoints()
    tester.print_summary()
    return tester.test_results


if __name__ == "__main__":
    run_price_controller_tests()

