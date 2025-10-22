import requests
import json
from datetime import datetime

def test_extension_data_flow():
    """Test that simulates what the VS Code extension would send"""
    
    server_url = "http://localhost:8001/debug-data"
    
    # Clear existing data first
    print("Testing debug data flow to MCP server...")
    
    # Test 1: Session started
    session_data = {
        "sessionStarted": {
            "name": "test_debug.py",
            "type": "debugpy",
            "id": "test-session-123",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    response = requests.post(server_url, json=session_data)
    print(f"✅ Session start sent: {response.status_code}")
    
    # Test 2: Variables data
    variables_data = {
        "variables": {
            "x": 10,
            "y": 20,
            "test_list": [1, 2, 3, 4, 5],
            "test_dict": {"name": "test", "value": 42}
        }
    }
    
    response = requests.post(server_url, json=variables_data)
    print(f"✅ Variables sent: {response.status_code}")
    
    # Test 3: Console output
    console_data = {
        "debugEvent": {
            "event": "output",
            "body": {
                "category": "stdout",
                "output": "Starting debug test...\n"
            },
            "timestamp": datetime.now().isoformat(),
            "sessionId": "test-session-123"
        }
    }
    
    response = requests.post(server_url, json=console_data)
    print(f"✅ Console output sent: {response.status_code}")
    
    # Test 4: Stack trace
    stack_data = {
        "stack": [
            {
                "id": 1,
                "name": "main",
                "line": 25,
                "source": "test_debug.py"
            },
            {
                "id": 2,
                "name": "calculate_sum",
                "line": 7,
                "source": "test_debug.py"
            }
        ]
    }
    
    response = requests.post(server_url, json=stack_data)
    print(f"✅ Stack trace sent: {response.status_code}")
    
    # Test 5: Breakpoints
    breakpoint_data = {
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
    
    response = requests.post(server_url, json=breakpoint_data)
    print(f"✅ Breakpoints sent: {response.status_code}")
    
    # Check final state
    print("\n📊 Final debug data state:")
    response = requests.get(server_url)
    data = response.json()
    
    print(f"Variables: {len(data.get('variables', {})) if data.get('variables') else 0} items")
    print(f"Stack frames: {len(data.get('stack', [])) if data.get('stack') else 0} items")
    print(f"Breakpoints: {len(data.get('breakpoints', [])) if data.get('breakpoints') else 0} items")
    
    if 'sessionStarted' in data:
        print(f"Session: {data['sessionStarted']['name']}")
    
    if 'debugEvent' in data:
        print(f"Last debug event: {data['debugEvent']['event']}")
    
    print("\n🎉 Extension data flow test completed successfully!")
    return True

if __name__ == "__main__":
    test_extension_data_flow()