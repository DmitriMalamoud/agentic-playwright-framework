import pytest
from playwright.sync_api import sync_playwright
from utils.logger import logger

def pytest_addoption(parser):
    parser.addoption("--headless-mode", action="store", default="true", help="Run tests in headless mode (true/false)")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    
    # We only look at the actual test call (not setup/teardown)
    if rep.when == "call":
        if rep.passed:
            logger.info(f"Test PASSED: {item.name}")
        elif rep.failed:
            logger.error(f"Test FAILED: {item.name}")
        elif rep.skipped:
            logger.info(f"Test SKIPPED: {item.name}")

        # Attach screenshots to the HTML report
        from pytest_html import extras
        import base64
        import os
        
        if not hasattr(rep, 'extra'):
            rep.extra = []

        # 1. Attach Screenshots
        screenshot_dir = "screenshots"
        if os.path.exists(screenshot_dir):
            for file in os.listdir(screenshot_dir):
                if file.endswith(".png"):
                    filepath = os.path.join(screenshot_dir, file)
                    try:
                        with open(filepath, "rb") as f:
                            encoded = base64.b64encode(f.read()).decode("utf-8")
                            rep.extra.append(extras.image(encoded, name=file))
                    except Exception as e:
                        logger.error(f"Failed to attach screenshot {file} to report: {e}")

        # 2. Attach Logs
        log_file = os.path.join("logs", "test.log")
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    log_content = f.read()
                    rep.extra.append(extras.text(log_content, name="Execution Logs"))
            except Exception as e:
                logger.error(f"Failed to attach logs to report: {e}")

@pytest.fixture(scope="function")
def web_app(request):
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    
    # Parse headless option
    headless_opt = request.config.getoption("--headless-mode").lower() == "true"
    
    with sync_playwright() as p:
        logger.info(f"Launching browser (headless={headless_opt})")
        # 1. Launch Browser
        browser = p.chromium.launch(headless=headless_opt)
        
        # 2. Provide fresh context and page
        context = browser.new_context()
        page = context.new_page()
        
        yield page
        
        # 3. Teardown
        logger.info(f"Cleaning up after test: {test_name}")
        page.close()
        context.close()
        browser.close()
        logger.info(f"Finished test: {test_name}")
