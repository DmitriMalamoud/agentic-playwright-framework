from playwright.sync_api import Page, Response
from utils.logger import logger
from utils.screenshot_utils import take_screenshot

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str) -> Response | None:
        """Navigates to a URL and waits for the load state."""
        logger.info(f"Navigating to URL: {url}")
        try:
            response = self.page.goto(url, wait_until="load")
            logger.info(f"Successfully navigated to: {url}")
            return response
        except Exception as e:
            logger.error(f"Failed to navigate to {url}. Error: {str(e)}")
            raise

    def click_element(self, selector: str, timeout: float = 10000):
        """Waits for an element to be visible and clicks it."""
        logger.info(f"Clicking element with selector: {selector}")
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            logger.info(f"Successfully clicked element: {selector}")
        except Exception as e:
            logger.error(f"Failed to click element: {selector}. Error: {str(e)}")
            raise

    def get_text(self, selector: str, timeout: float = 10000) -> str:
        """Waits for an element to be visible and returns its inner text."""
        logger.info(f"Getting text from element: {selector}")
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            text = locator.inner_text()
            logger.info(f"Retrieved text: '{text}' from element: {selector}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element: {selector}. Error: {str(e)}")
            raise

    def is_visible(self, selector: str, timeout: float = 5000) -> bool:
        """Checks if an element is visible within the timeout."""
        logger.info(f"Checking visibility of element: {selector}")
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            logger.info(f"Element {selector} is visible.")
            return True
        except Exception:
            logger.info(f"Element {selector} is NOT visible.")
            return False

    def wait(self, milliseconds: float):
        """Explicitly waits for the specified amount of time."""
        logger.info(f"Waiting for {milliseconds}ms...")
        self.page.wait_for_timeout(milliseconds)

    def take_screenshot(self, name: str = "latest_action.png"):
        """Takes a screenshot of the current page."""
        return take_screenshot(self.page, name)

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: float = 10000):
        """Waits for a selector to reach a certain state."""
        logger.info(f"Waiting for selector: {selector} to be {state}")
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
