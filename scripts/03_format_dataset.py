import os
import json

# BULLETPROOF PATHING
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_DIR = os.path.join(ROOT_DIR, "data", "final_odia_gold")
OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "odia_reasoning_train.jsonl")

def format_dataset():
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return

    # Find all the gold translated files
    gold_files = sorted([f for f in os.listdir(INPUT_DIR) if f.startswith("gold_") and f.endswith(".json")])
    
    if not gold_files:
        print("No translated gold files found! Complete the UI translation first.")
        return

    print(f"Found {len(gold_files)} translated files. Consolidating into .jsonl format...")

    # Write them line-by-line into the .jsonl file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for filename in gold_files:
            filepath = os.path.join(INPUT_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as infile:
                data = json.load(infile)
                
                # In .jsonl, each line is a valid JSON object
                json_line = json.dumps(data, ensure_ascii=False)
                outfile.write(json_line + "\n")

    print(f"✅ Success! Your training dataset is ready at: {OUTPUT_FILE}")

if __name__ == "__main__":
    format_dataset()
