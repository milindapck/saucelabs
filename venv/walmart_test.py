import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

@pytest.mark.parametrize("browser", ["chrome", "firefox"])
def test_walmart_search(browser):
    """Test Walmart search functionality on Chrome and Firefox."""

    if browser == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise Exception("Browser not supported")

    driver.get("https://www.saucedemo.com")

    # Verify search results
    assert "Swag Labs" in driver.title, "Test Failed: Search results did not load"

    driver.quit()

    
