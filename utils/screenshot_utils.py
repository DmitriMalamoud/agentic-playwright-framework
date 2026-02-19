import os
from playwright.sync_api import Page
from utils.logger import logger

def take_screenshot(page: Page, filename: str = "latest_action.png"):
    """
    Takes a screenshot and saves it to the 'screenshots' directory.
    Overwrites the previous screenshot with the same name.
    """
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    filepath = os.path.join(screenshot_dir, filename)
    
    try:
        # Use jpeg format with compression for smaller size if needed, 
        # but for now sticking to png with a smaller viewport or quality if supported
        page.screenshot(path=filepath, type="png")
        logger.info(f"Screenshot saved to: {filepath}")
    except Exception as e:
        logger.error(f"Failed to take screenshot. Error: {str(e)}")

    return filepath
