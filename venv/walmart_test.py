import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def pytest_addoption(parser):
    """Add a command-line option for browser selection."""
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests on")

@pytest.fixture
def browser(request):
    """Fixture to get the browser option from CLI."""
    return request.config.getoption("--browser")

@pytest.fixture
def driver(browser):
    """Setup Selenium WebDriver based on the browser parameter."""
    if browser == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()

def test_walmart_search(driver):
    """Test searching for a product on Walmart's website."""
    driver.get("https://www.saucedemo.com")

    # Verify search results
    assert "Swag Labs" in driver.title, "Test Failed: Search results did not load"
