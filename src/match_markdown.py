import json

def update_json_files():
    # Load the qa_with_index_markdown.json file
    with open("data/qa_with_index_markdown.json", "r", encoding="utf-8") as f:
        qa_data = json.load(f)
    
    # Load the all_accuracy_with_index.json file
    with open("data/accuracy_qwq_0404.json", "r", encoding="utf-8") as f:
        accuracy_data = json.load(f)
    
    # Create a dictionary from qa_data for efficient lookup by index
    qa_dict = {item["index"]: {"question": item["question"], "answer": item["answer"]} 
               for item in qa_data}
    
    # Replace matching items in accuracy_data
    replacements = 0
    for item in accuracy_data:
        if "index" in item and item["index"] in qa_dict:
            item["question"] = qa_dict[item["index"]]["question"]
            item["answer"] = qa_dict[item["index"]]["answer"]
            replacements += 1
    
    # Save the updated data to a new file
    output_path = "data/updated_accuracy_with_index_qwq.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(accuracy_data, f, ensure_ascii=False, indent=2)
    
    print(f"Process completed: {replacements} items replaced")
    print(f"Updated file saved to: {output_path}")

if __name__ == "__main__":
    update_json_files()