# Agentic Playwright Framework

A basic example demonstrating **vibe coding** with AI agents (Gemini CLI) to build a robust UI automation infrastructure, test suite, and CI/CD pipeline from scratch.

## 🚀 Overview

This repository serves as a proof-of-concept for modern automation development where the boilerplate, infrastructure, and test logic are co-authored by an AI agent. The framework uses **Python**, **pytest**, and **Playwright**, structured with a Page Object Model (POM) and integrated with GitHub Actions.

### Key Features
- **Page Object Model (POM)**: Clean separation of UI selectors and test logic.
- **Self-Contained Reporting**: `pytest-html` reports with embedded screenshots and timestamped logs.
- **CI/CD Pipeline**: Automated testing via GitHub Actions with manual triggers (`workflow_dispatch`).
- **Integrated Logging**: Custom logger capturing test steps and system events.

## 🛠 Tech Stack
- **Language**: Python 3.13+
- **Task Runner**: [Poetry](https://python-poetry.org/)
- **Test Framework**: [pytest](https://docs.pytest.org/)
- **Browser Automation**: [Playwright](https://playwright.dev/python/)
- **Reporting**: [pytest-html](https://pytest-html.readthedocs.io/)
- **CI/CD**: GitHub Actions

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DmitriMalamoud/agentic-playwright-framework.git
   cd agentic-playwright-framework
   ```

2. **Install dependencies using Poetry**:
   ```bash
   poetry install
   ```

3. **Install Playwright browsers**:
   ```bash
   poetry run playwright install chromium
   ```

## 🏃 Running Tests Locally

Run the existing test suite:
```bash
poetry run pytest
```

To run in headed mode:
```bash
poetry run pytest --headless-mode false
```

## ☁️ CI/CD with GitHub Actions

The workflow is configured to be triggered manually to save on CI minutes:
1. Navigate to the **Actions** tab in the GitHub repository.
2. Select the **Playwright Tests** workflow.
3. Click **Run workflow**.

After completion, a single **`report.html`** artifact is published containing the full execution logs and visual evidence (screenshots).

## 🤖 Vibe Coding Note
This entire repository—including the framework architecture, logging utilities, screenshot handlers, and this README—was created through interactive collaboration with **Gemini CLI**. It demonstrates the shift from manual "boilerplate" writing to high-level intent-driven engineering.
