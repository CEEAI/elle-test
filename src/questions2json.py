#Convert questions and answers of the lvgou model in csv format to json format for scoring
import pandas as pd
import json
import os

def convert_csv_to_json(csv_path, json_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Create list to store questions
    questions = []
    
    # Process each row, excluding the first column (序号)
    for _, row in df.iterrows():
        # Skip empty rows
        if pd.isna(row['question']):
            continue
            
        # Create dictionary excluding the 序号 column
        question_dict = {
            'question': row['question'],
            'answer': row['answer'],
            'difficulty': row['difficulty'],
            'type': row['type'],
            'field': row['field'],
            'model': row['model'],
            'response': row['response']
        }
        questions.append(question_dict)
    
    # Write to JSON file with proper formatting
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(questions, json_file, ensure_ascii=False, indent=2)
    
    print(f"Successfully converted {csv_path} to {json_path}")
    print(f"Total questions: {len(questions)}")

if __name__ == "__main__":
    csv_path = "data/lvgou1.csv"
    json_path = "data/lvgou_response.json"
    convert_csv_to_json(csv_path, json_path)