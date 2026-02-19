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
        print(f"\nDEBUG: pytest_runtest_makereport called for {item.name}")
        
        # 1. Attach Screenshots
        screenshot_dir = "screenshots"
        if os.path.exists(screenshot_dir):
            for file in os.listdir(screenshot_dir):
                if file.endswith(".png"):
                    filepath = os.path.join(screenshot_dir, file)
                    try:
                        with open(filepath, "rb") as f:
                            encoded = base64.b64encode(f.read()).decode("utf-8")
                            from pytest_html import extras
                            # Add image as HTML to force it into the self-contained report
                            html_content = f'<div><p><b>{file}</b></p><img src="data:image/png;base64,{encoded}" style="width:600px; border: 2px solid #ddd;"></div>'
                            extra.append(extras.html(html_content))
                            print(f"DEBUG: Attached screenshot {file}")
                    except Exception as e:
                        print(f"DEBUG: Error attaching screenshot: {e}")

        # Add a clear text marker to prove extras are working
        from pytest_html import extras
        extra.append(extras.text("=== VISUAL EVIDENCE ATTACHED ==="))
        
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
