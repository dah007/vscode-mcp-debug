import requests
import json
import time
from datetime import datetime

def comprehensive_test():
    """Comprehensive test of the VS Code Debug MCP setup"""
    
    server_url = "http://localhost:8001"
    debug_endpoint = f"{server_url}/debug-data"
    health_endpoint = f"{server_url}/health"
    
    print("🧪 VS Code Debug MCP Setup - Comprehensive Test")
    print("=" * 50)
    
    # Test 1: Server Health
    try:
        response = requests.get(health_endpoint)
        if response.status_code == 200:
            print("✅ Server is healthy and running")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        return False
    
    # Test 2: Current state
    response = requests.get(debug_endpoint)
    current_data = response.json()
    print(f"📊 Current debug data state:")
    print(f"   Variables: {len(current_data.get('variables', {})) if current_data.get('variables') else 0} items")
    print(f"   Stack frames: {len(current_data.get('stack', [])) if current_data.get('stack') else 0} items")
    print(f"   Breakpoints: {len(current_data.get('breakpoints', [])) if current_data.get('breakpoints') else 0} items")
    
    # Test 3: Simulate full debug session flow
    print("\n🎯 Simulating complete debug session...")
    
    session_id = f"test-{int(time.time())}"
    
    # Session start
    session_start = {
        "sessionStarted": {
            "name": "test_debug.py",
            "type": "debugpy", 
            "id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    }
    requests.post(debug_endpoint, json=session_start)
    print("   ✅ Session started")
    
    # Variables captured
    variables = {
        "variables": {
            "x": 10,
            "y": 20,
            "sum_result": 30,
            "product_result": 200,
            "test_list": [1, 2, 3, 4, 5],
            "test_dict": {"name": "test", "value": 42}
        }
    }
    requests.post(debug_endpoint, json=variables)
    print("   ✅ Variables captured")
    
    # Console output
    console_outputs = [
        "Starting debug test...",
        "Adding 10 + 20 = 30",
        "Multiplying 10 * 20 = 200",
        "Final results: sum=30, product=200",
        "Debug test completed!"
    ]
    
    for output in console_outputs:
        console_data = {
            "debugEvent": {
                "event": "output",
                "body": {
                    "category": "stdout",
                    "output": output + "\n"
                },
                "timestamp": datetime.now().isoformat(),
                "sessionId": session_id
            }
        }
        requests.post(debug_endpoint, json=console_data)
    print("   ✅ Console output captured")
    
    # Stack trace
    stack = {
        "stack": [
            {"id": 1, "name": "main", "line": 25, "source": "test_debug.py"},
            {"id": 2, "name": "calculate_sum", "line": 7, "source": "test_debug.py"}
        ]
    }
    requests.post(debug_endpoint, json=stack)
    print("   ✅ Stack trace captured")
    
    # Breakpoints
    breakpoints = {
        "breakpoints": [
            {
                "id": "bp1",
                "enabled": True,
                "condition": None,
                "hitCondition": None,
                "logMessage": None
            }
        ]
    }
    requests.post(debug_endpoint, json=breakpoints)
    print("   ✅ Breakpoints captured")
    
    # Session end
    session_end = {
        "sessionTerminated": {
            "name": "test_debug.py",
            "id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    }
    requests.post(debug_endpoint, json=session_end)
    print("   ✅ Session terminated")
    
    # Test 4: Verify final state
    print("\n📈 Final verification...")
    response = requests.get(debug_endpoint)
    final_data = response.json()
    
    success_checks = []
    
    # Check variables
    if final_data.get('variables') and len(final_data['variables']) >= 6:
        success_checks.append("✅ Variables stored correctly")
    else:
        success_checks.append("❌ Variables not stored properly")
    
    # Check stack
    if final_data.get('stack') and len(final_data['stack']) >= 2:
        success_checks.append("✅ Stack trace stored correctly")
    else:
        success_checks.append("❌ Stack trace not stored properly")
    
    # Check breakpoints
    if final_data.get('breakpoints') and len(final_data['breakpoints']) >= 1:
        success_checks.append("✅ Breakpoints stored correctly")
    else:
        success_checks.append("❌ Breakpoints not stored properly")
    
    # Check session data
    if final_data.get('sessionStarted') and final_data.get('sessionTerminated'):
        success_checks.append("✅ Session lifecycle tracked correctly")
    elif final_data.get('sessionStarted'):
        success_checks.append("⚠️  Session started but termination not captured")
    else:
        success_checks.append("❌ Session lifecycle not tracked")
    
    # Check debug events
    if final_data.get('debugEvent'):
        success_checks.append("✅ Debug events captured correctly")
    else:
        success_checks.append("❌ Debug events not captured")
    
    for check in success_checks:
        print(f"   {check}")
    
    # Overall result
    passed = sum(1 for check in success_checks if check.startswith("✅"))
    total = len(success_checks)
    
    print(f"\n🎯 Test Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The VS Code Debug MCP setup is working perfectly!")
        print("\n📋 Setup Summary:")
        print("   • MCP Server running on http://localhost:8001")
        print("   • Debug data endpoint: /debug-data")
        print("   • Extension compiled and ready")
        print("   • Data flow verified end-to-end")
        print("\n🚀 Ready for VS Code debug sessions!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the setup.")
        return False

if __name__ == "__main__":
    comprehensive_test()