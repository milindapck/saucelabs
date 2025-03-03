import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get credentials from environment variables
SAUCE_USERNAME = os.getenv("SAUCE_USERNAME")
SAUCE_ACCESS_KEY = os.getenv("SAUCE_ACCESS_KEY")

# Verify if credentials are being retrieved
if not SAUCE_USERNAME or not SAUCE_ACCESS_KEY:
    raise Exception("Sauce Labs credentials are missing! Ensure SAUCE_USERNAME and SAUCE_ACCESS_KEY are set.")

SAUCE_URL = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"

@pytest.fixture(scope="function")
def driver():
    """Setup Sauce Labs Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    sauce_options = {
        "username": SAUCE_USERNAME,
        "accessKey": SAUCE_ACCESS_KEY,
        "browserName": "chrome",
        "platformName": "Windows 10",
        "browserVersion": "latest",
        "name": "Walmart Search Test",
        "build": "Walmart-Automation"
    }
    options.set_capability("sauce:options", sauce_options)

    driver = webdriver.Remote(command_executor=SAUCE_URL, options=options)
    yield driver
    driver.quit()

def test_sauce(driver):
    driver.get('http://www.saucedemo.com/v1')

    username_locator = (By.CSS_SELECTOR, '#user-name')
    password_locator = (By.CSS_SELECTOR, '#password')
    submit_locator = (By.CSS_SELECTOR, '.btn_action')

    wait = WebDriverWait(driver, 10)
    wait.until(lambda x: driver.find_element(by=username_locator[0], value=username_locator[1]).is_displayed)

    username_element = driver.find_element(by=username_locator[0], value=username_locator[1])
    password_element = driver.find_element(by=password_locator[0], value=password_locator[1])
    submit_element = driver.find_element(by=submit_locator[0], value=submit_locator[1])

    username_element.send_keys('standard_user')
    password_element.send_keys('secret_sauce')
    submit_element.click()

    urlIsCorrect = "/inventory.html" in driver.current_url
    jobStatus = "passed" if urlIsCorrect else "failed"
    driver.execute_script("sauce:job-result=" + jobStatus)
    '''
    """Test searching for a product on Walmart's website."""
    driver.get("https://www.walmart.com/")
    driver.maximize_window()

    # Wait until the search box is visible
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))  # Updated locator
        )
    except:
        driver.save_screenshot("search_box_not_found.png")  # Capture screenshot for debugging
        assert False, "Search box not found on Walmart homepage"
    search_box.send_keys("Laptop")
    search_box.send_keys(Keys.RETURN)
    title = driver.title
    titleIsCorrect = "Swag Labs" in title
    jobStatus = "passed" if titleIsCorrect else "failed"

    # end the session
    driver.execute_script("sauce:job-result=" + jobStatus)
    driver.quit()

    # Wait for Human or Robot Popup
    """
    try:
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Close']"))
        )
        close_popup.click()
    except:
        print("No popup found, continuing test.")

    #assert "laptop" in driver.title.lower(), "Search results page did not load correctly"
    """
    '''

if __name__ == "__main__":
    pytest.main()
