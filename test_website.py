import requests
from bs4 import BeautifulSoup
import time

class WebsiteTester:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.pages = ['', 'about.html', 'products.html', 'contact.html']
        self.results = []
        self.start_time = time.time()
    
    def log_result(self, test_name, status, message=''):
        """Log test results with timing."""
        elapsed = f"{time.time() - self.start_time:.2f}s"
        status_icon = '✓' if status == 'PASS' else '✗'
        self.results.append(f"[{status_icon}] {test_name} - {status} - {elapsed} {message}")
    
    def test_page_loads(self):
        """Test if all pages load successfully."""
        for page in self.pages:
            url = f"{self.base_url}/{page}" if page else self.base_url
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    self.log_result(f"Page Load: {url}", 'PASS', f"Status: {response.status_code}")
                else:
                    self.log_result(f"Page Load: {url}", 'FAIL', f"Status: {response.status_code}")
            except Exception as e:
                self.log_result(f"Page Load: {url}", 'ERROR', str(e))
    
    def test_navigation_links(self):
        """Test all navigation links on each page."""
        for page in self.pages:
            url = f"{self.base_url}/{page}" if page else self.base_url
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                nav_links = [a['href'] for a in soup.select('nav a[href]')]
                
                for link in set(nav_links):  # Remove duplicates
                    if link.startswith(('http', '#')):
                        continue
                    full_url = f"{self.base_url}/{link}" if not link.startswith('/') else f"{self.base_url}{link}"
                    try:
                        link_response = requests.get(full_url, timeout=5)
                        if link_response.status_code == 200:
                            self.log_result(f"Nav Link: {url} -> {link}", 'PASS')
                        else:
                            self.log_result(f"Nav Link: {url} -> {link}", 'FAIL', f"Status: {link_response.status_code}")
                    except Exception as e:
                        self.log_result(f"Nav Link: {url} -> {link}", 'ERROR', str(e))
            except Exception as e:
                self.log_result(f"Nav Test Setup: {url}", 'ERROR', str(e))
    
    def test_images(self):
        """Test if all images load correctly."""
        for page in self.pages:
            url = f"{self.base_url}/{page}" if page else self.base_url
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                images = [img['src'] for img in soup.find_all('img', src=True)]
                
                for img_src in set(images):
                    if img_src.startswith(('http', 'data:')):
                        continue
                    img_url = f"{self.base_url}/{img_src}" if not img_src.startswith('/') else f"{self.base_url}{img_src}"
                    try:
                        img_response = requests.head(img_url, timeout=5)
                        if img_response.status_code == 200:
                            self.log_result(f"Image: {img_src}", 'PASS')
                        else:
                            self.log_result(f"Image: {img_src}", 'FAIL', f"Status: {img_response.status_code}")
                    except Exception as e:
                        self.log_result(f"Image: {img_src}", 'ERROR', str(e))
            except Exception as e:
                self.log_result(f"Image Test Setup: {url}", 'ERROR', str(e))
    
    def run_tests(self):
        """Run all tests and print results."""
        print("🚀 Starting website tests...\n")
        
        print("🔍 Testing page loads...")
        self.test_page_loads()
        
        print("🔗 Testing navigation links...")
        self.test_navigation_links()
        
        print("🖼️  Testing images...")
        self.test_images()
        
        # Print summary
        print("\n📊 Test Results:")
        print("=" * 50)
        for result in self.results:
            print(result)
        
        # Count results
        passed = sum(1 for r in self.results if '[✓]' in r)
        failed = sum(1 for r in self.results if '[✗]' in r)
        total = len(self.results)
        
        print("\n📈 Summary:")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ({(passed/total)*100:.1f}%)")
        print(f"Failed: {failed} ({(failed/total)*100:.1f}%)")
        print("=" * 50)
        
        return failed == 0

if __name__ == "__main__":
    tester = WebsiteTester()
    success = tester.run_tests()
    exit(0 if success else 1)
