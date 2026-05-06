# AI-Powered Log Analysis POC

This repository contains a Proof of Concept (POC) for automatically analyzing CI/CD log failures using AI models (Gemini, Claude, or OpenAI).

## Features
- **Automatic Triggers**: Runs on every push or pull request.
- **AI Analysis**: Captures both **Build failures** (e.g., pip install errors) and **Test failures** (`pytest`).
- **Real-time Dashboard**: A premium local dashboard to track trends and analysis history.
- **Smart Reporting**: 
  - Posts a summary directly to PR comments.
  - Adds a detailed report to the GitHub Actions Job Summary.
  - Saves logs and summaries as workflow artifacts.
- **Multi-Model Support**: Works with `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, or `OPENAI_API_KEY`.

## Project Structure
- `.github/workflows/ai-log-analysis.yml`: The GitHub Actions workflow configuration.
- `scripts/analyze_log.py`: Python script that interfaces with AI APIs.
- `tests/test_demo.py`: Sample tests (including failures) to demonstrate the logic.
- `requirements.txt`: Python dependencies.

## Setup Instructions

1. **Add Secrets**:
   Go to your GitHub repository settings -> **Secrets and variables** -> **Actions** and add one (or more) of the following:
   - `GOOGLE_API_KEY` (Recommended)
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`

2. **Run the Dashboard Locally**:
   ```bash
   python run_dashboard.py
   ```
   Open [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/) to see your intelligence dashboard.

3. **Trigger the Workflow**:
   - Push a change to `main`.
   - Open a Pull Request.
   - Or manually trigger it from the **Actions** tab via `workflow_dispatch`.

4. **View Results**:
   - Check the **Job Summary** on the Actions run page.
   - Check your **Pull Request** for a comment from `github-actions[bot]`.
   - The dashboard will update automatically if you have it running!

## Demo
The `tests/test_demo.py` file is intentionally designed to fail. This ensures you can see the AI analysis in action immediately upon the first run!
