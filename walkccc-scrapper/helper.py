# test_scraper.py
import json
import requests
from urllib.parse import urljoin

def test_leetcode_links(json_file="leetcode_problems.json"):
    """Test if the generated LeetCode links are valid"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        
        print(f"Testing {len(problems)} problems...")
        
        valid_count = 0
        invalid_count = 0
        
        for problem in problems[:10]:  # Test first 10 problems
            url = problem['link']
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    print(f"✓ {problem['number']}: {problem['name']} - Valid")
                    valid_count += 1
                else:
                    print(f"✗ {problem['number']}: {problem['name']} - Invalid ({response.status_code})")
                    invalid_count += 1
            except requests.RequestException as e:
                print(f"✗ {problem['number']}: {problem['name']} - Error: {e}")
                invalid_count += 1
        
        print(f"\nResults: {valid_count} valid, {invalid_count} invalid")
        
    except Exception as e:
        print(f"Error testing links: {e}")

if __name__ == "__main__":
    test_leetcode_links()
