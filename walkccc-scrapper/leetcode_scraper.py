import json
import re
import random
import signal
import sys
import os
import webbrowser
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from bs4 import BeautifulSoup
import pyperclip  # For copying to clipboard


# Load environment variables
load_dotenv()


# Set up logging with reduced verbosity
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LeetCodeScraper:
    def __init__(self):
        self.scraping_driver = None
        self.problems_data = []
        self.existing_problems = {}  # Track existing problems by number
        self.json_filename = "leetcode_problems_with_solutions.json"
        self.interrupted = False
        
        # Get credentials from .env file
        self.login_email = os.getenv('LOGIN_MAIL')
        self.login_password = os.getenv('LOGIN_PASS')
        
        # Load existing problems from JSON file
        self.load_existing_problems()
        
        # Set up signal handler for graceful interruption
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def load_existing_problems(self):
        """Load existing problems from JSON file to avoid duplicates based on number field"""
        try:
            if os.path.exists(self.json_filename):
                with open(self.json_filename, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    
                # Create a dictionary with problem numbers as keys (from the "number" field)
                for problem in existing_data:
                    problem_number = problem.get('number')  # Get the "number" field
                    if problem_number:
                        self.existing_problems[problem_number] = problem
                        
                print(f"📁 Loaded {len(self.existing_problems)} existing problems from {self.json_filename}")
                print(f"🔢 Existing problem numbers: {sorted(self.existing_problems.keys(), key=int)}")
            else:
                print("📁 No existing JSON file found. Starting fresh.")
        except Exception as e:
            print(f"⚠️ Warning: Could not load existing JSON file: {e}")
            self.existing_problems = {}
    
    def problem_exists(self, problem_number):
        """Check if a problem number already exists in the loaded data"""
        exists = problem_number in self.existing_problems
        if exists:
            print(f"✅ Problem {problem_number} found in existing data")
        else:
            print(f"🆕 Problem {problem_number} is new")
        return exists
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Interruption detected! Saving current progress...")
        self.interrupted = True
        self.save_to_json()
        self.cleanup()
        sys.exit(0)
        
    def setup_scraping_driver(self):
        """Initialize the Chrome driver for walkccc.me scraping"""
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--log-level=3")
            
            self.scraping_driver = webdriver.Chrome(options=chrome_options)
            self.scraping_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver initialized successfully for walkccc.me scraping")
            return True
        except Exception as e:
            print(f"❌ Error initializing scraping Chrome driver: {e}")
            return False
    
    def convert_name_to_hyphen_format(self, problem_name):
        """Convert problem name to hyphen-separated lowercase format"""
        try:
            clean_name = re.sub(r'[^\w\s-]', '', problem_name)
            hyphen_name = clean_name.lower().replace(' ', '-')
            hyphen_name = re.sub(r'-+', '-', hyphen_name)
            hyphen_name = hyphen_name.strip('-')
            return hyphen_name
        except Exception as e:
            return problem_name.lower().replace(' ', '-')
    
    def extract_first_solution(self, solution_url):
        """Extract the first available solution from the solution page"""
        try:
            # Navigate to solution page
            self.scraping_driver.get(solution_url)
            time.sleep(random.uniform(2, 3))
            
            # Wait for page to load
            WebDriverWait(self.scraping_driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for code content to load
            time.sleep(random.uniform(1, 2))
            
            # Try to find any code block first
            page_source = self.scraping_driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Look for code blocks in order of preference
            code_selectors = [
                'code',
                'pre code',
                '.highlight code',
                'pre',
                '.codehilite'
            ]
            
            solution_code = ""
            for selector in code_selectors:
                try:
                    code_elements = soup.select(selector)
                    for code_element in code_elements:
                        # Remove spans with class="c1" before extracting text
                        comment_spans = code_element.find_all('span', class_='c1')
                        for span in comment_spans:
                            span.decompose()  # Remove the span completely
                        
                        code_text = code_element.get_text().strip()
                        if len(code_text) > 50:  # Minimum length for a solution
                            # Extract all remaining span text with spaces if spans exist
                            spans = code_element.find_all('span')
                            if spans:
                                # Filter out any remaining spans with class="c1"
                                filtered_spans = [span for span in spans if not span.get('class') or 'c1' not in span.get('class')]
                                solution_code = ' '.join(span.get_text() for span in filtered_spans)
                            else:
                                solution_code = code_text
                            
                            # Clean up the solution text
                            solution_code = ' '.join(solution_code.split())
                            
                            # Additional check to remove any remaining comment lines
                            lines = solution_code.split('\n')
                            filtered_lines = []
                            for line in lines:
                                # Skip lines that are purely comments
                                stripped_line = line.strip()
                                if not (stripped_line.startswith('//') or 
                                       stripped_line.startswith('/*') or 
                                       stripped_line.startswith('*') or
                                       stripped_line.endswith('*/')):
                                    filtered_lines.append(line)
                            
                            solution_code = '\n'.join(filtered_lines)
                            solution_code = ' '.join(solution_code.split())
                            
                            return solution_code
                except Exception:
                    continue
            
            return ""
                
        except Exception as e:
            return ""
    
    def save_to_json(self):
        """Save the extracted problems to a JSON file, merging with existing data"""
        try:
            print(f"\n💾 Saving to JSON file...")
            print(f"📊 Current problems_data count: {len(self.problems_data)}")
            print(f"📊 Current existing_problems count: {len(self.existing_problems)}")
            
            # Combine existing problems with newly scraped ones
            all_problems = {}
            
            # Add existing problems first
            for problem_num, problem_data in self.existing_problems.items():
                all_problems[problem_num] = problem_data
                
            # Add newly scraped problems (will overwrite if same number exists)
            for problem in self.problems_data:
                all_problems[problem['number']] = problem
                print(f"➕ Adding problem {problem['number']} to final JSON")
            
            # Convert back to list and sort by problem number
            final_problems = list(all_problems.values())
            final_problems.sort(key=lambda x: int(x['number']))
            
            print(f"📊 Total problems to save: {len(final_problems)}")
            
            # Create backup of existing file
            if os.path.exists(self.json_filename):
                backup_filename = f"{self.json_filename}.backup"
                import shutil
                shutil.copy2(self.json_filename, backup_filename)
                print(f"📋 Created backup: {backup_filename}")
            
            # Write to JSON file
            with open(self.json_filename, 'w', encoding='utf-8') as f:
                json.dump(final_problems, f, indent=2, ensure_ascii=False)
            
            # Verify the file was written correctly
            if os.path.exists(self.json_filename):
                with open(self.json_filename, 'r', encoding='utf-8') as f:
                    verification_data = json.load(f)
                print(f"✅ JSON file saved successfully with {len(verification_data)} problems")
                
                # Show the newly added problems
                if self.problems_data:
                    print(f"🆕 Newly added problems:")
                    for problem in self.problems_data:
                        print(f"   - {problem['number']}: {problem['name']}")
            else:
                print(f"❌ Failed to create JSON file")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error saving to JSON file: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def extract_problem_info_with_solution(self, li_element):
        """Extract problem information and solution from a single <li> element"""
        try:
            # Find the anchor tag within the li element
            anchor = li_element.find('a')
            if not anchor:
                return None
            
            # Get the href attribute (original solution link)
            solution_link = anchor.get('href', '')
            
            # Get the text content
            problem_text = anchor.get_text(strip=True)
            
            # Extract problem number and name using regex
            match = re.match(r'^(\d+)\.\s*(.+)$', problem_text)
            if not match:
                return None
            
            problem_number = match.group(1)  # This is the "number" field we're checking
            problem_name = match.group(2)
            
            print(f"🔍 Checking problem number: {problem_number}")
            
            # Check if this problem number already exists in JSON
            if self.problem_exists(problem_number):
                print(f"⏭️ Problem {problem_number}: {problem_name} already exists in JSON, skipping...")
                return None
            
            # Convert name to hyphen format
            hyphen_name = self.convert_name_to_hyphen_format(problem_name)
            
            # Create LeetCode problem URL
            leetcode_url = f"https://leetcode.com/problems/{hyphen_name}/"
            
            # Convert relative solution link to absolute URL
            if solution_link.startswith('../../../problems/'):
                solution_path = solution_link.replace('../../../problems/', '')
                absolute_solution_url = f"https://walkccc.me/LeetCode/problems/{solution_path}"
            else:
                absolute_solution_url = solution_link
            
            # Extract solution
            print(f"🔄 Extracting solution for NEW Problem {problem_number}: {problem_name}")
            solution_code = self.extract_first_solution(absolute_solution_url)
            
            problem_data = {
                "number": problem_number,  # This is the key field we're checking against
                "name": problem_name,
                "link": leetcode_url,
                "solution": solution_code,
                "submitted": False
            }
            
            # CRITICAL FIX: Update existing_problems to include newly processed problem
            self.existing_problems[problem_number] = problem_data
            print(f"➕ Added problem {problem_number} to existing_problems cache")
            
            return problem_data
            
        except Exception as e:
            print(f"❌ Error in extract_problem_info_with_solution: {e}")
            return None
    
    def open_problem_for_submission(self, problem_data):
        """Open LeetCode problem and copy solution to clipboard"""
        try:
            print(f"\n🚀 Opening Problem {problem_data['number']}: {problem_data['name']}")
            print(f"🔗 Link: {problem_data['link']}")
            
            # Copy solution to clipboard
            pyperclip.copy(problem_data['solution'])
            print("📋 Solution copied to clipboard!")
            
            # Open the problem in browser
            webbrowser.open(problem_data['link'])
            
            # Display solution for reference
            print(f"💻 Solution ({len(problem_data['solution'])} chars):")
            print("=" * 80)
            print(problem_data['solution'])
            print("=" * 80)
            
            print("\n📝 Instructions:")
            print("1. The solution is already copied to your clipboard")
            print("2. In the opened LeetCode page, paste the solution (Ctrl+V)")
            print("3. Click Submit")
            print("4. Wait for the result")
            
            # Wait for user to submit
            print("\n⏳ Waiting 20 seconds for you to submit...")
            time.sleep(20)
            
            # Mark as submitted
            problem_data['submitted'] = True
            print("✅ Moving to next problem...")
            
            return True
                
        except Exception as e:
            print(f"❌ Error opening problem: {e}")
            return False
    
    def debug_existing_problems(self):
        """Debug method to show what problems are currently cached"""
        print(f"\n🔍 DEBUG: Currently cached problem numbers:")
        if self.existing_problems:
            for num in sorted(self.existing_problems.keys(), key=int):
                problem = self.existing_problems[num]
                print(f"  - {num}: {problem['name']}")
        else:
            print("  - No problems cached")
        print(f"📊 Total cached: {len(self.existing_problems)}\n")
    
    def scrape_and_assist_submission(self, url):
        """Scrape problems and assist with submission"""
        try:
            if not self.scraping_driver:
                return False
            
            # Debug: Show currently cached problems
            self.debug_existing_problems()
            
            print(f"🌐 Navigating to {url}")
            self.scraping_driver.get(url)
            time.sleep(random.uniform(3, 4))
            
            # Wait for page to load
            WebDriverWait(self.scraping_driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(random.uniform(2, 3))
            
            # Get page source and parse with BeautifulSoup
            html_content = self.scraping_driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all li elements that contain problem links
            li_elements = soup.find_all('li')
            
            print(f"🔍 Found {len(li_elements)} li elements")
            
            problems_found = 0
            problems_skipped = 0
            problems_processed = 0
            valid_problems = []
            
            # First, collect all valid problem links
            for li in li_elements:
                anchor = li.find('a')
                if anchor:
                    href = anchor.get('href', '')
                    if ('../../../problems/' in href or '/problems/' in href):
                        valid_problems.append(li)
            
            print(f"📊 Found {len(valid_problems)} valid problems to check")
            print("🚀 Starting solution extraction and assisted submission...")
            print("🧹 Filtering out comment spans with class='c1'")
            print("⏭️ Skipping problems that already exist in JSON")
            print("\n🔐 Please make sure you're logged into LeetCode in your browser")
            
            # Process each valid problem
            for i, li in enumerate(valid_problems):
                if self.interrupted:
                    break
                    
                print(f"\n🎯 Checking problem {i+1}/{len(valid_problems)}")
                problem_data = self.extract_problem_info_with_solution(li)
                
                if problem_data is None:
                    # Problem was skipped (already exists)
                    problems_skipped += 1
                    continue
                
                if problem_data:
                    self.problems_data.append(problem_data)
                    problems_found += 1
                    problems_processed += 1
                    
                    # Show progress
                    solution_length = len(problem_data['solution'])
                    print(f"📝 Problem {problem_data['number']}: {problem_data['name']} (Solution: {solution_length} chars)")
                    
                    # Open problem for submission
                    if problem_data['solution']:
                        self.open_problem_for_submission(problem_data)
                    else:
                        print(f"⚠️ No solution found for Problem {problem_data['number']}")
                    
                    # Save to JSON after each problem (real-time update)
                    print(f"💾 Saving progress after problem {problem_data['number']}...")
                    if self.save_to_json():
                        print(f"✅ Progress saved successfully!")
                    else:
                        print(f"❌ Failed to save progress!")
                    
                    # Add delay between problems
                    time.sleep(random.uniform(2, 3))
            
            print(f"\n🎉 Processing completed!")
            print(f"📊 Problems processed: {problems_processed}")
            print(f"⏭️ Problems skipped (already exist): {problems_skipped}")
            print(f"✅ New problems found: {problems_found}")
            return True
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.scraping_driver:
            self.scraping_driver.quit()
            print("🔒 Scraping driver closed successfully")


def main():
    scraper = LeetCodeScraper()
    
    try:
        print("🚀 Starting LeetCode scraper with duplicate checking...")
        print("📝 Press Ctrl+C to interrupt and save current progress")
        print("\n📋 How this works:")
        print("1. Loads existing problems from JSON file by checking 'number' field")
        print("2. Chrome driver scrapes solutions from walkccc.me")
        print("3. Skips problems that already exist in JSON")
        print("4. Updates cache with newly processed problems to prevent re-processing")
        print("5. Filters out comment spans with class='c1'")
        print("6. Each new problem opens in your default browser")
        print("7. Solution is automatically copied to clipboard")
        print("8. You paste and submit manually in LeetCode")
        print("9. Process continues automatically after 20 seconds")
        print("10. JSON file is updated after each new problem")
        print("\n🔐 Make sure you're logged into LeetCode in your browser first!")
        
        # Wait for user confirmation
        input("\nPress Enter to continue...")
        
        # Initialize scraping driver
        if not scraper.setup_scraping_driver():
            print("Failed to initialize scraping driver")
            return
        
        # Start scraping and assisted submission
        url = "https://walkccc.me/LeetCode/topics/data-structures/fundamental/"
        if scraper.scrape_and_assist_submission(url):
            print("✅ Successfully completed all scraping and assisted submissions")
        
        # Final statistics
        total_in_json = len(scraper.existing_problems)
        new_problems = len(scraper.problems_data)
        
        print(f"\n📊 Final Summary:")
        print(f"📋 Total problems in JSON: {total_in_json}")
        print(f"🆕 New problems added: {new_problems}")
        
        if scraper.problems_data:
            solutions_count = sum(1 for p in scraper.problems_data if p['solution'])
            submitted_count = sum(1 for p in scraper.problems_data if p.get('submitted', False))
            print(f"💡 Solutions found: {solutions_count}/{new_problems}")
            print(f"🚀 Assisted submissions: {submitted_count}/{new_problems}")
        
        # Final save to JSON file
        print(f"\n💾 Performing final save...")
        if scraper.save_to_json():
            print("✅ Final data saved successfully!")
        else:
            print("❌ Final save failed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user!")
        scraper.save_to_json()
    except Exception as e:
        print(f"❌ Main execution error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()
