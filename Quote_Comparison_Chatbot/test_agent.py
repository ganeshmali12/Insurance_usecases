import json
from quote_comparison_agent import compare_quotes

with open("sample_quotes.json") as f:
    quotes = json.load(f)

question = "Which insurance quote is best for a family of 4?"

response = compare_quotes(quotes, question)

print("\n🤖 Chatbot Response:\n")
print(response)
