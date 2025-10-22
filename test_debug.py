#!/usr/bin/env python3
"""
Simple test script for debugging with the VS Code extension
"""

def calculate_sum(a, b):
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    return result

def calculate_product(a, b):
    result = a * b
    print(f"Multiplying {a} * {b} = {result}")
    return result

def main():
    print("Starting debug test...")
    
    x = 10
    y = 20
    
    # Set breakpoint here to test debug data collection
    sum_result = calculate_sum(x, y)
    product_result = calculate_product(x, y)
    
    print(f"Final results: sum={sum_result}, product={product_result}")
    
    # Test some variables for debugging
    test_list = [1, 2, 3, 4, 5]
    test_dict = {"name": "test", "value": 42}
    
    print("Debug test completed!")

if __name__ == "__main__":
    main()