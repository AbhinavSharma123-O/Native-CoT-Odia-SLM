import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# Groq uses the OpenAI python library, we just point it to Groq's servers!
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API Key not found! Please check your .env file.")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# Llama 3.3 70B is free, fast, and excellent at mathematical reasoning
MODEL_ID = "llama-3.3-70b-versatile"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "raw_english")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_reasoning_problem(index, max_retries=3):
    file_path = os.path.join(OUTPUT_DIR, f"problem_{index}.json")
    
    if os.path.exists(file_path):
        print(f"⏭️ Skipping {index}: Already exists.")
        return

    prompt = """
    Generate a highly complex, multi-step math or logic word problem.
    The problem MUST require at least 4-5 distinct steps of reasoning to solve.
    
    You must output ONLY valid JSON using this exact format:
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
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are an expert logic puzzle designer. You output strict JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            raw_text = response.choices[0].message.content
            data = json.loads(raw_text)
            data["id"] = str(index)
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            print(f"✅ [Success] Generated problem {index}")
            return 
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ [Attempt {attempt + 1}/{max_retries}] Error on problem {index}: {error_msg}")
            
            if attempt < max_retries - 1:
                print("⏳ Waiting 15 seconds before retrying...")
                time.sleep(15)
            else:
                print(f"❌ [Failed] Could not generate problem {index}.")

if __name__ == "__main__":
    print("🚀 Starting Groq Mass Generation Pipeline...")
    for i in range(490, 500):
        generate_reasoning_problem(i)
        # 5 seconds delay keeps us well within Groq's generous free tier
        time.sleep(5) 
    print("🎉 Generation Complete!")