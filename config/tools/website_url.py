from langchain.agents import tool
from config.tools.browser_control_methods import get_driver
from config.logs.logger import log_message

@tool
def redirect_to_website(url: str) -> str:
    """
    Redirects the Chrome WebDriver to the specified URL.

    Args:
    url (str): The URL or ip address to navigate to. 
    If user gives website name convert into url

    Returns:
    str: A message indicating the result of the redirection.
    """
    driver = get_driver()
    
    if driver is None:
        log_message("Error: Chrome WebDriver not started. Please start the driver first.")
        return "Error: Chrome WebDriver not started. Please start the driver first."

    try:
        driver.get(url)
        log_message(f"Successfully redirected to {url}")
        return f"Successfully redirected to {url}"
    except Exception as e:
        error_msg = f"Failed to redirect to {url}. Error: {str(e)}"
        log_message(error_msg)
        return error_msg