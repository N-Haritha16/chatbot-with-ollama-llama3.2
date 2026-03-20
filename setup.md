1. Fix setup.md formatting
Make sure setup.md looks like this (proper markdown fences and headings):

# Setup Instructions

## 1. Requirements

- Windows with Python 3.8+
- Ollama installed and working
- Internet (one time) to download `llama3.2:3b`

## 2. Install and check Ollama

```bash
ollama --version
ollama pull llama3.2:3b
You should see the version and the model download successfully. 

3. Go to the project folder
bash
cd "C:\Users\HARITHA\Desktop\patnr tasks\chatbot-with-ollama-llama3.2"

4. Create and activate virtual environment
bash
python -m venv venv
venv\Scripts\activate

5. Install dependencies
bash
pip install -r requirements.txt

6. Run the chatbot evaluation
Make sure Ollama is running, then:

bash
python chatbot.py
This will create and fill eval\results.md with all 20 queries and both prompting methods. 

7. Score and write report
Open eval\results.md and fill Relevance, Coherence, Helpfulness (1–5) for each response. Use these scores to compute averages and write your analysis in report.md.

Save this as `setup.md` (only setup content in this file).

***

## 2. Put the report content into `report.md`

Everything from:

```markdown
# Zero-Shot vs One-Shot Prompting with Llama 3.2 (3B)
...
belongs in report.md, not in setup.md.
​

Open report.md.

Paste your Introduction, Methodology, Results & Analysis, and Conclusion & Limitations there.

Replace the example averages with your real averages if you compute them.
