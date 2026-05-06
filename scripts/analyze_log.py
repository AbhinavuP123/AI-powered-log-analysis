import os
import sys
import json
import datetime
import re
from openai import OpenAI
import anthropic
from google import genai
from dotenv import load_dotenv

# Load environment variables (for local testing)
load_dotenv()

def append_to_db(summary_text):
    db_path = "db.json"
    data = []
    if os.path.exists(db_path):
        try:
            with open(db_path, "r") as f:
                data = json.load(f)
        except:
            pass
            
    # Try to extract details from the markdown
    status = "failed"
    if "passed" in summary_text.lower() and "failed" not in summary_text.lower():
        status = "passed"
        
    # Improved regex for parsing sections
    summary_match = re.search(r"\*\*1\) Summary:\*\*\s*(.+?)(?=\n\*\*2\)|\n$|$)", summary_text, re.DOTALL | re.IGNORECASE)
    if not summary_match:
        summary_match = re.search(r"Summary:\s*(.+?)(?=\nRoot|\n$|$)", summary_text, re.DOTALL | re.IGNORECASE)
        
    root_cause_match = re.search(r"\*\*2\) Root cause of failures:\*\*\s*(.+?)(?=\n\*\*3\)|\n$|$)", summary_text, re.DOTALL | re.IGNORECASE)
    if not root_cause_match:
        root_cause_match = re.search(r"Root cause:\s*(.+?)(?=\nFixes|\n$|$)", summary_text, re.DOTALL | re.IGNORECASE)
    
    summary = summary_match.group(1).strip() if summary_match else "See report for details."
    root_cause = root_cause_match.group(1).strip() if root_cause_match else "Analysis in progress."

    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "status": status,
        "summary": summary.replace("\n", " ")[:200] + ("..." if len(summary) > 200 else ""),
        "root_cause": root_cause.replace("\n", " ")[:200] + ("..." if len(root_cause) > 200 else ""),
    }
    
    data.append(entry)
    with open(db_path, "w") as f:
        json.dump(data, f, indent=4)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_log.py <path_to_log_file>")
        sys.exit(1)
        
    log_path = sys.argv[1]
    
    if not os.path.exists(log_path):
        print(f"Error: Log file not found at {log_path}")
        sys.exit(1)
        
    with open(log_path, 'r', encoding='utf-8') as f:
        log_content = f.read()

    # Truncate log if it's too long
    max_chars = 10000
    if len(log_content) > max_chars:
        log_content = "...[Truncated]...\n" + log_content[-max_chars:]
        
    prompt = f"""You are a CI/CD assistant. Analyze the following build/test log 
and provide: 
1) A 3-line summary
2) Root cause of failures
3) Suggested fixes

Log Output:
```
{log_content}
```
"""

    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    google_key = os.environ.get("GOOGLE_API_KEY")

    summary = ""

    try:
        if google_key:
            print("Using Google Gemini for analysis...")
            client = genai.Client(api_key=google_key)
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            summary = response.text
        elif anthropic_key:
            print("Using Anthropic Claude for analysis...")
            client = anthropic.Anthropic(api_key=anthropic_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=1000,
                temperature=0.2,
                system="You are a helpful CI/CD assistant. Format your response in markdown.",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.content[0].text
        elif openai_key:
            print("Using OpenAI GPT for analysis...")
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful CI/CD assistant. Format your response in markdown."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            summary = response.choices[0].message.content
        else:
            print("No API key provided. Generating mock analysis.")
            summary = "### 🤖 Mock AI Analysis\n\n**1) Summary:**\nTests failed due to an intentional assertion error.\nThe workflow is working correctly but the code is broken.\nFix the failing test to see this pass.\n\n**2) Root cause:**\n`AssertionError: 1 == 2` in `tests/test_demo.py`.\n\n**3) Suggested fixes:**\nCorrect the assertion in the test file."

        # Write to summary.md for the workflow to read
        with open("summary.md", "w", encoding='utf-8') as f:
            f.write(summary)
            
        print("Analysis complete. Summary saved to summary.md")
        
        # Update dashboard database
        append_to_db(summary)
        print("Dashboard database (db.json) updated.")
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        with open("summary.md", "w", encoding='utf-8') as f:
            f.write(f"### ❌ AI Analysis Failed\n\nAn error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
