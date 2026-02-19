import os
import base64
import sys

def publish_summary():
    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_file:
        print("GITHUB_STEP_SUMMARY not set, skipping summary generation.")
        return

    summary_content = "# 🧪 Test Execution Report

"

    # 1. Add Logs
    log_file = "logs/test.log"
    if os.path.exists(log_file):
        summary_content += "## 📜 Test Logs
"
        summary_content += "<details>
<summary>Click to expand logs</summary>

"
        summary_content += "```text
"
        with open(log_file, "r") as f:
            # Take last 100 lines to avoid size limits if log is huge
            lines = f.readlines()
            summary_content += "".join(lines[-100:])
        summary_content += "```
"
        summary_content += "</details>

"

    # 2. Add Screenshots
    screenshot_dir = "screenshots"
    if os.path.exists(screenshot_dir):
        screenshots = [f for f in os.listdir(screenshot_dir) if f.endswith('.png')]
        if screenshots:
            summary_content += "## 📸 Visual Evidence
"
            for screenshot in screenshots:
                filepath = os.path.join(screenshot_dir, screenshot)
                with open(filepath, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                
                summary_content += f"### {screenshot}
"
                # Check if the encoded string is too large (GH Summary limit is 1024KB total)
                if len(encoded_string) < 800000: # ~800KB buffer
                    summary_content += f"![{screenshot}](data:image/png;base64,{encoded_string})

"
                else:
                    summary_content += f"⚠️ Screenshot {screenshot} is too large to display inline.

"

    with open(summary_file, "a") as f:
        f.write(summary_content)

if __name__ == "__main__":
    publish_summary()
