import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_basic_contact_form_test():
    print("🚀 Starting basic contact form test...")
    
    # Set up Chrome options
    chrome_options = Options()
    # Disable headless mode for debugging
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Test 1: Load the contact page
        print("🔍 Loading contact page...")
        driver.get("http://localhost:8000/contact.html")
        
        # Take a screenshot
        driver.save_screenshot("contact_page_loaded.png")
        print("✓ Contact page loaded successfully")
        
        # Test 2: Check if form elements are present
        print("🔍 Checking form elements...")
        required_fields = ["name", "email", "message"]
        for field in required_fields:
            element = wait.until(EC.presence_of_element_located((By.ID, field)))
            print(f"✓ Found form field: {field}")
        
        # Test 3: Test form validation
        print("🔍 Testing form validation...")
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # Check for error messages
        time.sleep(1)
        error_elements = driver.find_elements(By.CSS_SELECTOR, ".error-message")
        if error_elements:
            print(f"✓ Form validation errors shown: {len(error_elements)} error messages displayed")
        else:
            print("✗ No validation errors shown")
        
        # Test 4: Fill out the form
        print("📝 Filling out the form...")
        test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+1 (234) 567-8901",
            "message": "This is a test message for the contact form."
        }
        
        for field, value in test_data.items():
            try:
                element = wait.until(EC.presence_of_element_located((By.NAME, field)))
                element.clear()
                element.send_keys(value)
                print(f"✓ Filled {field} field")
            except Exception as e:
                print(f"✗ Error filling {field}: {str(e)}")
        
        # Check privacy checkbox
        try:
            privacy_checkbox = wait.until(EC.presence_of_element_located((By.ID, "privacy")))
            if not privacy_checkbox.is_selected():
                driver.execute_script("arguments[0].click();", privacy_checkbox)
            print("✓ Checked privacy policy")
        except Exception as e:
            print(f"✗ Error with privacy checkbox: {str(e)}")
        
        # Submit the form
        print("📤 Submitting the form...")
        driver.save_screenshot("before_submit.png")
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # Wait for submission to complete
        time.sleep(2)
        driver.save_screenshot("after_submit.png")
        
        # Check for success message
        try:
            success_msg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success")))
            print(f"✓ Form submitted successfully: {success_msg.text[:50]}...")
            return True
        except:
            print("✗ Form submission may have failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        driver.save_screenshot("test_error.png")
        return False
        
    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    success = run_basic_contact_form_test()
    if success:
        print("\n✅ All tests completed successfully!")
        exit(0)
    else:
        print("\n❌ Some tests failed. Check the output for details.")
        exit(1)
