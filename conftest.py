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
        import os
        import base64
        
        # Get the pytest-html plugin
        pytest_html = item.config.pluginmanager.getplugin("html")
        
        if not hasattr(rep, 'extra'):
            rep.extra = []

        # Diagnostic text
        if pytest_html:
            rep.extra.append(pytest_html.extras.text("Visual Evidence Processing..."))

        # 1. Attach Screenshots
        screenshot_dir = "screenshots"
        if os.path.exists(screenshot_dir):
            for file in os.listdir(screenshot_dir):
                if file.endswith(".png"):
                    filepath = os.path.join(screenshot_dir, file)
                    try:
                        with open(filepath, "rb") as f:
                            encoded = base64.b64encode(f.read()).decode("utf-8")
                            # Using html extra to force rendering
                            html = f'<div><p>{file}</p><img src="data:image/png;base64,{encoded}" style="width:600px;"></div>'
                            if pytest_html:
                                rep.extra.append(pytest_html.extras.html(html))
                    except Exception as e:
                        logger.error(f"Failed to attach screenshot {file} to report: {e}")

        # Removed manual log attachment as it causes duplication with pytest's own capture

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
