import os
import base64
import sys

def publish_summary():
    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_file:
        print("GITHUB_STEP_SUMMARY not set, skipping summary generation.")
        return

    summary_content = "# 🧪 Test Execution Report\n\n"

    # 1. Add Logs
    log_file = "logs/test.log"
    if os.path.exists(log_file):
        summary_content += "## 📜 Test Logs\n"
        summary_content += "<details>\n<summary>Click to expand logs</summary>\n\n"
        summary_content += "```text\n"
        try:
            with open(log_file, "r") as f:
                # Take last 100 lines to avoid size limits if log is huge
                lines = f.readlines()
                summary_content += "".join(lines[-100:])
        except Exception as e:
            summary_content += f"Error reading log file: {str(e)}\n"
        summary_content += "```\n"
        summary_content += "</details>\n\n"

    # 2. Add Screenshots
    screenshot_dir = "screenshots"
    if os.path.exists(screenshot_dir):
        try:
            screenshots = [f for f in os.listdir(screenshot_dir) if f.endswith('.png')]
            if screenshots:
                summary_content += "## 📸 Visual Evidence\n"
                for screenshot in screenshots:
                    filepath = os.path.join(screenshot_dir, screenshot)
                    with open(filepath, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    
                    summary_content += f"### {screenshot}\n"
                    # Check if the encoded string is too large (GH Summary limit is 1024KB total)
                    if len(encoded_string) < 800000: # ~800KB buffer
                        summary_content += f"![{screenshot}](data:image/png;base64,{encoded_string})\n\n"
                    else:
                        summary_content += f"⚠️ Screenshot {screenshot} is too large to display inline.\n\n"
        except Exception as e:
            summary_content += f"Error processing screenshots: {str(e)}\n"

    with open(summary_file, "a", encoding="utf-8") as f:
        f.write(summary_content)

if __name__ == "__main__":
    publish_summary()
