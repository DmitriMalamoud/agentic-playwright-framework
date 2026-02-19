import pytest
from pages.HomePage import HomePage
from utils.logger import logger

def test_demoblaze_categories(web_app):
    import os
    import shutil
    if os.path.exists("screenshots"):
        shutil.rmtree("screenshots")
    os.makedirs("screenshots")

    home_page = HomePage(web_app)
    
    # 1. Navigate to https://www.demoblaze.com/
    home_page.open()
    
    # 2. Verify that the panel "Categories" with options "Phones", "Laptops", "Monitors" is visible
    home_page.verify_categories_visible()
    
    # Capture state before clicking
    home_page.wait_for_products_to_load()
    initial_content = home_page.get_products_content()
    
    # Click on the "Monitors" button
    home_page.click_monitors()
    
    # Validation after "Monitors" is clicked, that the state of the page has changed
    # We wait for the content to be different from the initial state
    def content_changed():
        return home_page.get_products_content() != initial_content
    
    # Custom wait for state change
    try:
        web_app.wait_for_function("initial => document.querySelector('#tbodyid').innerHTML !== initial", 
                                 arg=initial_content, timeout=10000)
        logger.info("Verified: Page state (product list) has changed after clicking Monitors.")
    except Exception:
        assert False, "Page state did not change after clicking Monitors"
    
    # Reduce the wait from 20 to 5 seconds.
    home_page.wait(5000)

    # Add screenshot after the new elements are displayed, before the explicit 5 second wait starts
    home_page.take_screenshot("monitors_page.png")
