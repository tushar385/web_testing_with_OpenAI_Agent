from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain.tools import tool
from config.tools.browser_control_methods import get_driver
from config.logs.logger import log_message
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException




@tool
def input_element(locator_type: str, locator_value: str, input_text: str, timeout: int = 10) -> str:
    """
    Finds an element on the web page and sends input text to it.

    Args:
    locator_type (str): The type of locator to use. Can be 'id', 'name', or 'xpath'.
    locator_value (str): The value of the locator.
    input_text (str): The text to input into the element.
    timeout (int): Maximum time to wait for the element to be present (default: 10 seconds).

    Returns:
    str: A message indicating whether the input was successful or not.
    """
    driver = get_driver()
    
    if driver is None:
        log_message("Error: Chrome WebDriver not started. Please start the driver first.")
        return "Error: Chrome WebDriver not started. Please start the driver first."

    try:
        if locator_type.lower() == 'id':
            locator = (By.ID, locator_value)
        elif locator_type.lower() == 'name':
            locator = (By.NAME, locator_value)
        elif locator_type.lower() == 'xpath':
            locator = (By.XPATH, locator_value)
        else:
            log_message(f"Invalid locator type: {locator_type}. Use 'id', 'name', or 'xpath'.")
            return f"Invalid locator type: {locator_type}. Use 'id', 'name', or 'xpath'."

        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

        element.send_keys(input_text)

        log_message(f"Input sent to element using {locator_type}: {locator_value}")
        return f"Input sent to element using {locator_type}: {locator_value}"
    except Exception as e:
        error_msg = f"Failed to input text to element using {locator_type}: {locator_value}. Error: {str(e)}"
        log_message(error_msg)
        return error_msg




@tool
def click_element(locator_type: str, locator_value: str, timeout: int = 10) -> str:
    """
    Finds an element on the web page and clicks it.

    Args:
    locator_type (str): The type of locator to use. Can be 'id', 'name', or 'xpath'.
    locator_value (str): The value of the locator.
    timeout (int): Maximum time to wait for the element to be clickable (default: 10 seconds).

    Returns:
    str: A message indicating whether the click was successful or not.
    """
    driver = get_driver()
    
    if driver is None:
        log_message("Error: Chrome WebDriver not started. Please start the driver first.")
        return "Error: Chrome WebDriver not started. Please start the driver first."

    try:
        if locator_type.lower() == 'id':
            locator = (By.ID, locator_value)
        elif locator_type.lower() == 'name':
            locator = (By.NAME, locator_value)
        elif locator_type.lower() == 'xpath':
            locator = (By.XPATH, locator_value)
        else:
            log_message(f"Invalid locator type: {locator_type}. Use 'id', 'name', or 'xpath'.")
            return f"Invalid locator type: {locator_type}. Use 'id', 'name', or 'xpath'."

        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        
        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)

        # Use JavaScript to click the element
        driver.execute_script("arguments[0].click();", element)

        log_message(f"Element clicked using {locator_type}: {locator_value}")
        return f"Element clicked using {locator_type}: {locator_value}"
    except Exception as e:
        error_msg = f"Failed to click element using {locator_type}: {locator_value}. Error: {str(e)}"
        log_message(error_msg)
        return error_msg
