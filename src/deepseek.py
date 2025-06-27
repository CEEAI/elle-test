import concurrent.futures
import copy
import json
import logging
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

load_dotenv()

openai_api_key = os.getenv("DEEPSEEK_API_KEY")
model_names = ["deepseek-reasoner"]


def test_model(model_name, data):
    try:
        data_copy = copy.deepcopy(data)
        llm_chat = ChatOpenAI(
            api_key=openai_api_key,
            model_name=model_name,
            streaming=False,
            verbose=False,
            base_url="https://api.deepseek.com/v1",
        )
        responses = []
        for item in data_copy:
            try:
                response = llm_chat.invoke(item["question"])
                item["model"] = model_name
                item["response"] = response.content
                responses.append(item)
            except Exception as e:
                logging.error(
                    f"Error processing question '{item['question']}' with model '{model_name}': {e}"
                )
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"{model_name}_response.json")
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(responses, f, ensure_ascii=False, indent=4)
        logging.info(
            f"Model '{model_name}' processed successfully. Output saved to '{output_filename}'."
        )
    except Exception as e:
        logging.error(f"Error testing model '{model_name}': {e}")


def main():
    try:
        with open("data/question.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(test_model, model_name, data)
                for model_name in model_names
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Thread raised an exception: {e}")
    except Exception as e:
        logging.error(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
