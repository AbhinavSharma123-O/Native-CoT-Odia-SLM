import os
import json
import re

# BULLETPROOF PATHING
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_DIR = os.path.join(ROOT_DIR, "data", "raw_english")
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "stripped_skeletons")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Core Math & Logic Dictionary (English to Odia) ---
# We inject both the Odia word and the English word in brackets to give you context during translation.
# You can easily add more words to this list as you expand your dataset!
ODIA_DICT = {
    r"\badd\b": "ଯୋଗ (add)",
    r"\baddition\b": "ଯୋଗ (addition)",
    r"\bsubtract\b": "ବିୟୋଗ (subtract)",
    r"\bmultiply\b": "ଗୁଣନ (multiply)",
    r"\bdivide\b": "ହରଣ (divide)",
    r"\bequal\b": "ସମାନ (equal)",
    r"\bequals\b": "ସମାନ (equals)",
    r"\bif\b": "ଯଦି (if)",
    r"\bthen\b": "ତାହେଲେ (then)",
    r"\btherefore\b": "ତେଣୁ (therefore)",
    r"\bbecause\b": "କାରଣ (because)",
    r"\bsum\b": "ସମଷ୍ଟି (sum)",
    r"\btotal\b": "ମୋଟ (total)",
    r"\bdifference\b": "ପାର୍ଥକ୍ୟ (difference)",
    r"\bstep\b": "ପଦକ୍ଷେପ (step)",
    r"\bvariable\b": "ଚଳ (variable)",
    r"\bequation\b": "ସମୀକରଣ (equation)"
}

def deconstruct_text(text):
    """Scans text and replaces English logic words with Odia anchors."""
    processed_text = str(text)
    for eng_pattern, odia_replacement in ODIA_DICT.items():
        # re.IGNORECASE makes sure it catches "If", "IF", and "if"
        processed_text = re.sub(eng_pattern, odia_replacement, processed_text, flags=re.IGNORECASE)
    return processed_text

def process_files():
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return

    files_processed = 0
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".json"):
            input_path = os.path.join(INPUT_DIR, filename)
            # Change the filename from problem_1.json to skeleton_1.json
            output_path = os.path.join(OUTPUT_DIR, filename.replace("problem_", "skeleton_"))
            
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Deconstruct the reasoning steps
            skeleton_steps = [deconstruct_text(step) for step in data.get("reasoning_steps", [])]
            
            # Build the new hybrid JSON object
            skeleton_data = {
                "id": data.get("id", filename),
                "original_problem": data.get("problem", ""),
                "deconstructed_problem": deconstruct_text(data.get("problem", "")),
                "original_steps": data.get("reasoning_steps", []),
                "skeleton_steps": skeleton_steps,
                "final_answer": data.get("final_answer", "")
            }
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(skeleton_data, f, indent=4, ensure_ascii=False)
                
            print(f"Processed and skeletonized: {filename}")
            files_processed += 1
            
    if files_processed == 0:
        print("No JSON files found in the raw_english directory. Run Script 01 first.")

if __name__ == "__main__":
    print("Starting Deconstruction Protocol...")
    process_files()
    print("Done! Skeletons are ready in data/stripped_skeletons/")
