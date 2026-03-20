# Zero-Shot vs One-Shot Prompting with Llama 3.2 (3B)

## 1. Introduction

In this project I built an offline customer support chatbot for a fictional e-commerce store called Chic Boutique using the Llama 3.2 (3B) model served locally with Ollama. The goal was to compare zero-shot and one-shot prompting strategies on a set of realistic customer queries. Running the model locally helps protect customer data privacy because no requests leave the machine, and it also avoids external API costs. 

## 2. Methodology

I first adapted 20 queries from the Ubuntu Dialogue Corpus, changing technical support questions into e-commerce customer support questions (for example, a driver issue became a discount-code problem). These 20 queries were stored as a list in `chatbot.py`. For prompting, I used two templates: a zero-shot template with only instructions and the current customer query, and a one-shot template with the same instructions plus one example question–answer about the return policy before the current query. 

For each of the 20 queries, the script sent one request using the zero-shot template and one request using the one-shot template to the local Ollama server running `llama3.2:3b`. All responses were logged into `eval/results.md` in a Markdown table. I then manually scored every response on three metrics from 1 to 5: Relevance (how well it answered the question), Coherence (grammar and clarity), and Helpfulness (how actionable and useful the answer was). 

## 3. Results & Analysis

After scoring all 40 responses, I computed the average score per metric for each prompting method. The averages were:

| Method    | Relevance | Coherence | Helpfulness |
|----------|-----------|-----------|-------------|
| Zero-Shot | 4.1      | 4.5       | 3.9         |
| One-Shot  | 4.5      | 4.7       | 4.3         |

(Replace the numbers above with your own averages from `eval/results.md`.) 

Overall, one-shot prompting performed slightly better than zero-shot prompting on all three metrics, especially in Relevance and Helpfulness. For example, for the query “I received a damaged item. How can I request a replacement?”, the one-shot response directly described how to start the replacement from the order history page, while the zero-shot response focused more on asking for details before explaining the process. In simpler questions like “Do you offer cash on delivery as a payment option?”, both methods gave similar, clear answers, so the score difference there was small. 

## 4. Conclusion & Limitations

Based on this evaluation, one-shot prompting appears more suitable for this customer support chatbot, because it produces slightly more relevant and helpful responses while keeping coherence high. The example in the one-shot template helps the model match the desired tone and level of detail more consistently across different queries. However, the system has limitations: the model is relatively small (3B parameters), it does not access any real order or account database, and it can still hallucinate incorrect details or policies. The evaluation is also small in scale, with only 20 queries and one human annotator. 

In future work, this system could be improved by using a larger local model where hardware allows, integrating retrieval from a real knowledge base (such as FAQs and policy documents), and experimenting with more few-shot examples. It would also be useful to expand the evaluation to more queries and multiple annotators to get more robust quantitative results. 
