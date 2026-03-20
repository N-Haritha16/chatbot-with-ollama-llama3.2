import json
import os
from pathlib import Path

import requests

# Constants
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"
EVAL_DIR = BASE_DIR / "eval"
RESULTS_FILE = EVAL_DIR / "results.md"

ZERO_SHOT_TEMPLATE_PATH = PROMPTS_DIR / "zero_shot_template.txt"
ONE_SHOT_TEMPLATE_PATH = PROMPTS_DIR / "one_shot_template.txt"


def query_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload)
        response.raise_for_status()
        data = json.loads(response.text)
        return data.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        return "Error: Could not get a response from the model."


def load_template(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ensure_directories():
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(EVAL_DIR, exist_ok=True)


def get_queries():
    # 20 adapted e‑commerce queries (you can tweak wordings if you like)
    return [
        "My discount code is not working at checkout.",
        "How do I track the shipping status of my recent order?",
        "Can I change the delivery address after placing an order?",
        "I received a damaged item. How can I request a replacement?",
        "When will my refund be credited to my account?",
        "Do you offer cash on delivery as a payment option?",
        "How can I cancel an order that has not shipped yet?",
        "The size I ordered does not fit. What is the exchange process?",
        "How do I apply multiple discount codes on a single order?",
        "Is there a shipping charge for orders above a certain amount?",
        "My order shows delivered, but I have not received it. What should I do?",
        "How can I update my phone number in my account?",
        "Do you ship internationally and what are the charges?",
        "How do I know if a product is in stock before ordering?",
        "Can I schedule delivery for a specific date and time?",
        "I was charged twice for the same order. How do I fix this?",
        "How do I download the invoice for my order?",
        "What is your policy for returning sale or discounted items?",
        "I am not receiving order confirmation emails. How can I fix this?",
        "Can I combine items from multiple orders into a single shipment?"
    ]


def init_results_file():
    # Write header, rubric, and table header
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write("# Evaluation Results\n\n")
        f.write("Scoring Rubric:\n")
        f.write("- Relevance (1–5): How well does the response address the customer's query? "
                "(1 = Irrelevant, 5 = Perfectly relevant)\n")
        f.write("- Coherence (1–5): Is the response grammatically correct and easy to understand? "
                "(1 = Incoherent, 5 = Flawless)\n")
        f.write("- Helpfulness (1–5): Does the response provide a useful, actionable answer? "
                "(1 = Not helpful, 5 = Very helpful)\n\n")

        f.write("| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |\n")
        f.write("|---------|----------------|------------------|----------|-----------------|-----------------|-------------------|\n")


def append_result_row(f, query_index: int, customer_query: str, method: str, response_text: str):
    # Escape pipe characters in text so markdown table does not break
    safe_query = customer_query.replace("|", "\\|")
    safe_response = response_text.replace("|", "\\|").replace("\n", " ")

    f.write(
        f'| {query_index} | "{safe_query}" | {method} | {safe_response} |   |   |   |\n'
    )


def run_evaluation():
    ensure_directories()

    if not ZERO_SHOT_TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Missing template: {ZERO_SHOT_TEMPLATE_PATH}")
    if not ONE_SHOT_TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Missing template: {ONE_SHOT_TEMPLATE_PATH}")

    zero_shot_template = load_template(ZERO_SHOT_TEMPLATE_PATH)
    one_shot_template = load_template(ONE_SHOT_TEMPLATE_PATH)

    queries = get_queries()
    init_results_file()

    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        for i, q in enumerate(queries, start=1):
            # Zero-shot
            zero_prompt = zero_shot_template.format(query=q)
            zero_response = query_ollama(zero_prompt)
            append_result_row(f, i, q, "Zero-Shot", zero_response)

            # One-shot
            one_prompt = one_shot_template.format(query=q)
            one_response = query_ollama(one_prompt)
            append_result_row(f, i, q, "One-Shot", one_response)

    print(f"Evaluation completed. Results written to {RESULTS_FILE}")


if __name__ == "__main__":
    run_evaluation()
