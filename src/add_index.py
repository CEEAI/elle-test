import pandas as pd
import json
import os

def add_index_to_json():
    
    csv_path = 'data/add_index.csv' #csv file with question and index
    json_path = 'data/new.json' #json file with questions, answers, responses, and scores to be indexed
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return
    
    # 读取CSV文件，获取question和index的映射
    try:
        df = pd.read_csv(csv_path)
        # 创建一个字典，key是question，value是index
        question_to_index = dict(zip(df['question'], df['index']))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # 读取JSON文件
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return
    
    # 为JSON中的每个question添加index字段
    questions_not_found = []
    for item in json_data:
        question = item.get('question')
        if question in question_to_index:
            item['index'] = question_to_index[question]
        else:
            questions_not_found.append(question)
    
    # 输出未找到对应index的question
    if questions_not_found:
        print(f"Warning: {len(questions_not_found)} questions in JSON not found in CSV.")
        print("First few missing questions:")
        for q in questions_not_found[:5]:
            print(f"  - {q}")
    
    # 保存更新后的JSON
    output_path = 'data/qa_with_index.json' #output file with index added
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully added indices to JSON. Output saved to {output_path}")
    except Exception as e:
        print(f"Error writing updated JSON file: {e}")
        return

if __name__ == "__main__":
    add_index_to_json()