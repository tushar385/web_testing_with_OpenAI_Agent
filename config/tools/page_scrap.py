from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from langchain.tools import tool
from config.logs.logger import log_message
from config.tools.browser_control_methods import get_driver
from selenium.webdriver.support.ui import WebDriverWait
import time


@tool
def is_page_loaded(driver) -> bool:
    """
    Checks if the page is fully loaded by waiting for the document.readyState to be complete.

    Args:
    driver: The WebDriver instance.

    Returns:
    bool: True if the page is fully loaded, False otherwise.
    """
    try:
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        return True
    except Exception as e:
        log_message(f"Error while checking if page is loaded: {str(e)}")
        return False




@tool
def fetch_html(url: str = "") -> dict:
    """
    Fetches the HTML content of the specified page or the current page if no URL is provided.

    Args:
    url (str, optional): The URL of the page to fetch. If not provided, fetches the current page.

    Returns:
    dict: A dictionary containing the current URL and the full HTML source of the page.
    """
    driver = get_driver()

    if driver is None:
        log_message("Error: Chrome WebDriver not started. Please start the driver first.")
        return {"error": "Chrome WebDriver not started. Please start the driver first."}

    try:
        if url:
            # Navigate to the specified URL
            driver.get(url)
            # Check if the page is fully loaded
            if not is_page_loaded(driver):
                log_message("Error: Page did not load completely.")
                return {"error": "Page did not load completely."}

        # Extract the full HTML content of the page
        html_source = driver.page_source

        # Get the current URL (in case of redirects or if no URL was provided)
        current_url = driver.current_url

        log_message(f"Fetched HTML content for page: {current_url}")

        return {
            "url": current_url,
            "html_source": html_source
        }
    
    except Exception as e:
        error_msg = f"An error occurred while fetching HTML: {str(e)}"
        log_message(error_msg)
        return {"error": error_msg}

