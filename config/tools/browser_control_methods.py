import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from langchain.tools import tool
from config.logs.logger import log_message


driver = None

@tool
def start_chrome_driver(_: str = "") -> str:
    """
    Starts the Chrome WebDriver instance.

    Returns:
    str: A message indicating the result of starting the driver.
    """
    global driver
    try:
        if not driver:
            driver = webdriver.Chrome()
            log_message("Chrome WebDriver started successfully")
            return "Successfully started Chrome WebDriver"
        else:
            log_message("Chrome WebDriver is already running")
            return "Chrome WebDriver is already running"
    except Exception as e:
        log_message(f"Failed to start Chrome WebDriver. Error: {str(e)}")
        return f"Failed to start Chrome WebDriver. Error: {str(e)}"


def get_driver():
    global driver
    return driver



@tool
def stop_chrome_driver(_: str = "") -> str:
    """
    Stops the Chrome WebDriver instance.

    Returns:
    str: A message indicating the result of stopping the driver.
    """
    global driver
    try:
        if driver:
            driver.quit()
            driver = None
            log_message("Chrome WebDriver stopped successfully")
            return "Successfully stopped Chrome WebDriver"
        else:
            log_message("No active Chrome WebDriver instance to stop")
            return "No active Chrome WebDriver instance to stop"
    except Exception as e:
        log_message(f"Failed to stop Chrome WebDriver. Error: {str(e)}")
        return f"Failed to stop Chrome WebDriver. Error: {str(e)}"



@tool
def sleep_driver(seconds: str) -> str:
    """
    Pauses the execution of the WebDriver for a specified number of seconds.

    Args:
    seconds (str): The number of seconds to sleep.

    Returns:
    str: A message indicating the result of the sleep operation.
    """
    global driver
    try:
        seconds = float(seconds)
        if driver:
            time.sleep(seconds)
            log_message(f"Successfully paused Chrome WebDriver for {seconds} seconds")
            return f"Successfully paused Chrome WebDriver for {seconds} seconds"
        else:
            log_message("No active Chrome WebDriver instance to pause")
            return "No active Chrome WebDriver instance to pause"
    except ValueError:
        error_msg = f"Invalid input for seconds: {seconds}. Please provide a valid integer."
        log_message(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Failed to pause Chrome WebDriver. Error: {str(e)}"
        log_message(error_msg)
        return error_msg



