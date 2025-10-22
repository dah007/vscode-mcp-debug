import asyncio
from tools import mcp
from store import debug_data

async def test_mcp_tools():
    """Test the MCP tools functionality"""
    print("Testing MCP tools...")
    
    # Test the functions directly first
    print("\n📊 Current debug_data store:")
    print(f"Variables: {debug_data.get('variables', {})}")
    print(f"Stack: {debug_data.get('stack', [])}")
    print(f"Breakpoints: {debug_data.get('breakpoints', [])}")
    
    # Test each tool function directly
    print("\n🧪 Testing get_variables function:")
    from tools import get_variables
    result = get_variables()
    print(f"Variables: {result}")
    
    print("\n🧪 Testing get_stack_trace function:")
    from tools import get_stack_trace
    result = get_stack_trace()
    print(f"Stack trace: {result}")
    
    print("\n🧪 Testing get_breakpoints function:")
    from tools import get_breakpoints
    result = get_breakpoints()
    print(f"Breakpoints: {result}")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())