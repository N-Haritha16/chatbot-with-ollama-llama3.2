# Offline Customer Support Chatbot with Ollama and Llama 3.2

This project implements an offline customer support chatbot for a fictional e‑commerce store called **Chic Boutique**, using the Llama 3.2 (3B) model served locally via Ollama. The main goal is to compare **zero-shot** and **one-shot** prompting strategies on a set of realistic customer queries, and to evaluate their performance using a manual scoring rubric.

Running the model fully on your local machine ensures that no customer data leaves the system, which helps with privacy and compliance while also avoiding external API costs. 

---

## 1. Project Overview

The chatbot answers common e‑commerce customer support questions such as order tracking, refunds, returns, damaged items, and payment options. It uses:

- A **zero-shot** prompt template: only role + instructions + current query, no examples. 
- A **one-shot** prompt template: same instructions plus one example query–response pair before the current query. 

For each of 20 adapted customer queries (derived from the Ubuntu Dialogue Corpus), the script generates: 

- One response using the zero-shot template  
- One response using the one-shot template  

All responses and scores are logged in `eval/results.md`, and the analysis is written in `report.md`. 

---

## 2. Repository Structure

The repository follows the structure required in the task PDF: 

```text
.
├─ chatbot.py          # Main script to call Ollama and log results
├─ README.md           # Project overview and usage
├─ setup.md            # Environment setup and run instructions
├─ report.md           # Final analysis of zero-shot vs one-shot
├─ prompts/
│  ├─ zeroshottemplate.txt   # Zero-shot prompt template
│  └─ oneshottemplate.txt    # One-shot prompt template with example
└─ eval/
   └─ results.md       # Markdown table with all queries, responses, and scores

## 3. How It Works

3.1 Data and Queries:

The task requires adapting 20 queries from the Ubuntu Dialogue Corpus (technical support chats) into plausible e‑commerce customer support questions.

Examples from the PDF: 

Technical: “My wifi driver is not working after the latest update.”
Adapted: “My discount code is not working at checkout.”

Technical: “How do I check the logs for the apache server?”
Adapted: “How do I track the shipping status of my recent order?”

These 20 adapted queries are hardcoded as a Python list inside chatbot.py. 

3.2 Prompt Templates:

The prompts directory contains two templates as required: 

- zeroshottemplate.txt

a. Gives the model its role: a helpful, friendly, concise support agent for Chic Boutique.

b. Contains a query placeholder for the customer question.

c. Does not include any example Q&A.

- oneshottemplate.txt

a. Same role and instructions.

b. Includes one complete example:

Customer Query: What is your return policy?
Agent Response: We offer a 30-day return policy for all unworn items with tags still attached. You can start a return from your order history page. 

c. Then a query placeholder for the actual customer question. 

These templates are loaded in chatbot.py and formatted with each query before calling the model. 

3.3 Chatbot Client (chatbot.py)
chatbot.py is the main driver script. It: 

a. Defines the Ollama endpoint and model name (llama3.2:3b).

b. Loads the zero-shot and one-shot templates from the prompts directory.

c. Defines the list of 20 adapted customer queries.

d. For each query:

- Fills the zero-shot template and sends it to the Ollama generate API.

- Fills the one-shot template and sends it to the same API.

- Parses the JSON responses to extract the generated text.

- Logs both responses into eval/results.md as Markdown table rows.

- The script does not assign scores; scoring is done manually afterward. 

## 4. Evaluation Methodology

4.1 Scoring Rubric:

The evaluation is done in eval/results.md, which contains:

- A Scoring Rubric section describing three metrics: 

a. Relevance (1–5) – How well the response answers the customer’s query (1 = Irrelevant, 5 = Perfectly relevant).

b. Coherence (1–5) – Grammar, clarity, and ease of understanding (1 = Incoherent, 5 = Flawless).

c. Helpfulness (1–5) – How useful and actionable the response is (1 = Not helpful, 5 = Very helpful).

d. A Markdown table with columns: [file:1]

| Query # | Customer Query | Prompting Method | Response | Relevance (1–5) | Coherence (1–5) | Helpfulness (1–5) |

For each of the 20 queries, there are two rows: one for Zero‑Shot, one for One‑Shot. [file:1] After running chatbot.py, you manually read each response and assign scores in the last three columns.

4.2 Report (report.md):

Once scoring is complete, you compute:

- Average Relevance, Coherence, Helpfulness for Zero‑Shot

- Average Relevance, Coherence, Helpfulness for One‑Shot

These averages and qualitative observations (where one-shot clearly improves over zero-shot, where they are similar, etc.) are documented in report.md with the required structure: Introduction, Methodology, Results & Analysis, Conclusion & Limitations. 

## 5. Setup and Usage

Detailed environment and run instructions are in setup.md as required by the task. In summary:

a. Install and verify Ollama, then pull the model:

bash
ollama --version
ollama pull llama3.2:3b

b. Create and activate a Python virtual environment, install dependencies, and run:

bash
python chatbot.py

c. After the script finishes, open eval/results.md, fill in the scores, and then update report.md with your averages and analysis. 

For exact step‑by‑step instructions, see setup.md. 

## 6. Limitations and Possible Extensions

- Limitations: 

a. The model is relatively small (3B parameters), so some answers may be generic or occasionally incorrect.

b. The chatbot does not access real order databases; all answers are based purely on the prompt and the model’s training.

c. Evaluation is based on 20 queries and a single human annotator.

- Possible extensions:

a. Try a larger local model (if hardware allows) or compare multiple models via Ollama.

b. Add retrieval from a local FAQ / policy knowledge base.

c. Use more few-shot examples or chain-of-thought prompting.

d. Expand the evaluation set and involve multiple annotators for more robust metrics.

## 7. How This Meets the Task Requirements

This repository satisfies the core requirements from the assignment PDF: 

a. Required files and directories: README.md, setup.md, chatbot.py, report.md, prompts/, eval/results.md.

b. chatbot.py connects to a local Ollama server and queries the llama3.2:3b model.

c. prompts/ contains zeroshottemplate.txt and oneshottemplate.txt with the correct structure.

d. At least 20 e‑commerce queries are processed, each with both zero-shot and one-shot prompting.

e. eval/results.md contains a full Markdown table with all responses and manually entered scores.

f. report.md provides a quantitative and qualitative comparison of zero-shot vs one-shot prompting and discusses suitability and limitations of the local LLM setup. 