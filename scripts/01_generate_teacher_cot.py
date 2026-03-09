import os
import json
import time
from google import genai
from google.genai import types

# --- CONFIGURATION ---
API_KEY = "AIzaSyDFny7EAIUyXoSEH0OEsqw7gBPoSbhYt88" # <-- Paste your Gemini key here

# Initialize the NEW official client
client = genai.Client(api_key=API_KEY)

# Using 2.5-flash: It is fast, free-tier friendly, and great at logic
MODEL_ID = 'gemini-2.5-flash'

# BULLETPROOF PATHING
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "raw_english")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_reasoning_problem(index):
    prompt = """
    Generate a complex multi-step math or logic word problem.
    The problem must require at least 4-5 steps of reasoning.
    
    Use this exact JSON format:
    {
        "id": "index_number",
        "problem": "The text of the problem",
        "reasoning_steps": [
            "Step 1: ...",
            "Step 2: ...",
            "Step 3: ..."
        ],
        "final_answer": "The final numeric or logical answer"
    }
    """
    
    try:
        # The new v2 SDK syntax for generating content
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", # Forces strict JSON output
            )
        )
        
        raw_text = response.text
        # Safety cleanup just in case
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw_text)
        
        file_path = os.path.join(OUTPUT_DIR, f"problem_{index}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully generated problem {index}")
        
    except Exception as e:
        print(f"Error on problem {index}: {e}")

if __name__ == "__main__":
    for i in range(1, 6):
        generate_reasoning_problem(i)
        time.sleep(3)
