import pytest
import os
import base64
from playwright.sync_api import sync_playwright
from utils.logger import logger

def pytest_addoption(parser):
    parser.addoption("--headless-mode", action="store", default="true", help="Run tests in headless mode (true/false)")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Ensure the 'extra' attribute exists
    extra = getattr(report, "extra", [])

    if report.when == "call":
        # 1. Prepare Screenshots (but don't append yet)
        screenshot_extras = []
        screenshot_dir = "screenshots"
        if os.path.exists(screenshot_dir):
            for file in os.listdir(screenshot_dir):
                if file.endswith(".png"):
                    filepath = os.path.join(screenshot_dir, file)
                    try:
                        with open(filepath, "rb") as f:
                            encoded = base64.b64encode(f.read()).decode("utf-8")
                            from pytest_html import extras
                            # Add image as HTML
                            html_content = f'<div style="margin-top: 20px;"><p><b>Screenshot: {file}</b></p><img src="data:image/png;base64,{encoded}" style="width:800px; border: 1px solid #ddd;"></div>'
                            screenshot_extras.append(extras.html(html_content))
                    except Exception as e:
                        logger.error(f"Error processing screenshot for report: {e}")

        # 2. Append everything else first (if any)
        # ...
        
        # 3. Append screenshots at the end of the extras list
        extra.extend(screenshot_extras)
        
        # Re-assign the extra list to the report
        report.extra = extra

@pytest.fixture(scope="function")
def web_app(request):
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    headless_opt = request.config.getoption("--headless-mode").lower() == "true"
    
    with sync_playwright() as p:
        logger.info(f"Launching browser (headless={headless_opt})")
        browser = p.chromium.launch(headless=headless_opt)
        context = browser.new_context()
        page = context.new_page()
        yield page
        logger.info(f"Cleaning up after test: {test_name}")
        page.close()
        context.close()
        browser.close()
        logger.info(f"Finished test: {test_name}")
