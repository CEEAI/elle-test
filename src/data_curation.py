import json
import time

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import APIConnectionError

load_dotenv()

llm = init_chat_model("gpt-4o", model_provider="openai")

json_schema = {
    "title": "formatting_question",
    "description": "Formatting question",
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "description": "Formatted text",
        },
    },
    "required": ["text"],
}

prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "Your task is to convert all numerical values, units (e.g., °C, µg/m³, µm, g/cm³), formulas and chemical expressions into the specified Markdown notation, using the `$...$` format for inline expressions. Additionally, correct any potential spelling mistakes in English and any character errors or typos in Chinese while ensuring that the intended meaning remains unchanged.",
        ),
        ("user", "The original question: {text}"),
    ]
)

structured_llm = llm.with_structured_output(json_schema)

input_file = "data/qa_with_index.json"
output_file = "data/qa_with_index_markdown.json"

with open(input_file, "r", encoding="utf-8") as f:
    qa_items = json.load(f)

updated_qa_items = []
total_items = len(qa_items)

for i, qa_item in enumerate(qa_items):
    try:
        # process question
        question_prompt = prompt_template.invoke({"text": qa_item.get("question", "")})
        formatted_question = structured_llm.invoke(question_prompt).get("text")
        
        # process answer
        answer_prompt = prompt_template.invoke({"text": qa_item.get("answer", "")})
        formatted_answer = structured_llm.invoke(answer_prompt).get("text")
        
        # update item
        updated_item = qa_item.copy()
        updated_item["question"] = formatted_question
        updated_item["answer"] = formatted_answer
        updated_qa_items.append(updated_item)
        
        print(f"Processed item {i+1}/{total_items} (index: {qa_item.get('index', 'N/A')})")
        

        time.sleep(1)
    except APIConnectionError as e:
        print(f"Connection error occurred: {e}")
        print(f"Skipping item with index: {qa_item.get('index', 'N/A')}")
        
        updated_qa_items.append(qa_item)
        continue
    except Exception as e:
        print(f"Error processing item with index {qa_item.get('index', 'N/A')}: {e}")
        updated_qa_items.append(qa_item)
        continue


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(updated_qa_items, f, indent=2, ensure_ascii=False)

print(f"Processing complete. Updated {len(updated_qa_items)} items.")
print(f"Results saved to {output_file}")
