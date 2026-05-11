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
    # Improved regex for parsing sections - more flexible headers
    summary_match = re.search(r"(?:\*\*|\#\#|\d+\.)\s*(?:1\)?|Summary):?\**\s*(.+?)(?=\n(?:\*\*|\#\#|\d+\.)\s*(?:2\)?|Root [Cc]ause)|$)", summary_text, re.DOTALL | re.IGNORECASE)
    if not summary_match:
        summary_match = re.search(r"Summary:\s*(.+?)(?=\nRoot|$)", summary_text, re.DOTALL | re.IGNORECASE)
        
    root_cause_match = re.search(r"(?:\*\*|\#\#|\d+\.)\s*(?:2\)?|Root [Cc]ause):?\**\s*(.+?)(?=\n(?:\*\*|\#\#|\d+\.)\s*(?:3\)?|Suggested [Ff]ixes)|$)", summary_text, re.DOTALL | re.IGNORECASE)
    if not root_cause_match:
        root_cause_match = re.search(r"Root [Cc]ause.*?:?\s*(.+?)(?=\nSuggested [Ff]ixes|\n3\)?|$)", summary_text, re.DOTALL | re.IGNORECASE)
    
    summary = summary_match.group(1).strip() if summary_match else "See report for details."
    root_cause = root_cause_match.group(1).strip() if root_cause_match else "See full report in summary.md"

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
            try:
                client = genai.Client(api_key=google_key)
                # Try 2.0 Flash first
                try:
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt
                    )
                    summary = response.text
                except Exception as e:
                    if "429" in str(e):
                        print("Gemini 2.0 Flash rate limited. Trying Gemini 1.5 Flash...")
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=prompt
                        )
                        summary = response.text
                    else:
                        raise e
            except Exception as e:
                if "429" in str(e):
                    print("All Gemini models rate limited. Falling back to Mock analysis.")
                    summary = generate_mock_summary(log_content)
                else:
                    raise e
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
            summary = generate_mock_summary(log_content)

        # Ensure summary is not empty
        if not summary:
            summary = generate_mock_summary(log_content)

        # Write to summary.md for the workflow to read
        with open("summary.md", "w", encoding='utf-8') as f:
            f.write(summary)
            
        print("Analysis complete. Summary saved to summary.md")
        
        # Update dashboard database
        append_to_db(summary)
        print("Dashboard database (db.json) updated.")
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        # Final fallback to avoid workflow failure
        fallback_summary = generate_mock_summary(log_content)
        with open("summary.md", "w", encoding='utf-8') as f:
            f.write(fallback_summary)
        append_to_db(fallback_summary)
        print("Fell back to Mock analysis due to critical error.")

def generate_mock_summary(log_content):
    """Generates a structured mock summary based on the log content."""
    summary_text = "### 🤖 AI Analysis (Fallback/Mock)\n\n"
    summary_text += "**1) Summary:**\nThe test suite executed multiple tests. "
    
    if "FAILED" in log_content or "ERROR" in log_content:
        summary_text += "Several failures were detected across different modules.\n"
        
        # Simple rule-based extraction for the mock
        causes = []
        if "ZeroDivisionError" in log_content: causes.append("Division by zero")
        if "KeyError" in log_content: causes.append("Missing dictionary key")
        if "TypeError" in log_content: causes.append("Type mismatch (String + Int)")
        if "AssertionError" in log_content: causes.append("Failed assertions")
        
        summary_text += "\n**2) Root cause:**\n"
        if causes:
            summary_text += "Detected errors: " + ", ".join(causes) + ".\n"
        else:
            summary_text += "Generic application failure or environment issue.\n"
            
        summary_text += "\n**3) Suggested fixes:**\n"
        summary_text += "- Review the specific lines in the log for precise error locations.\n"
        summary_text += "- Ensure data types are consistent and dictionary keys exist before access.\n"
    else:
        summary_text += "All tests passed successfully.\n\n**2) Root cause:**\nN/A\n\n**3) Suggested fixes:**\nNone needed."
        
    return summary_text

if __name__ == "__main__":
    main()
