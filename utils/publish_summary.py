import os
import sys

def publish_summary():
    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_file:
        print("GITHUB_STEP_SUMMARY not set, skipping summary generation.")
        return

    summary_content = "# 🧪 Test Execution Report\n\n"
    
    summary_content += "### 📊 Visual Report Available\n"
    summary_content += "A detailed HTML report with integrated screenshots is available in the **Artifacts** section of this run (see `playwright-html-report`).\n\n"

    # 1. Add Logs
    log_file = "logs/test.log"
    if os.path.exists(log_file):
        summary_content += "## 📜 Test Logs\n"
        summary_content += "<details>\n<summary>Click to expand logs</summary>\n\n"
        summary_content += "```text\n"
        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                summary_content += "".join(lines[-100:])
        except Exception as e:
            summary_content += f"Error reading log file: {str(e)}\n"
        summary_content += "```\n"
        summary_content += "</details>\n\n"

    with open(summary_file, "a", encoding="utf-8") as f:
        f.write(summary_content)

if __name__ == "__main__":
    publish_summary()
