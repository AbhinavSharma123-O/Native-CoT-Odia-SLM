import streamlit as st
import os
import json

# BULLETPROOF PATHING
UI_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UI_DIR)
INPUT_DIR = os.path.join(ROOT_DIR, "data", "stripped_skeletons")
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "final_odia_gold")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up the webpage layout
st.set_page_config(layout="wide", page_title="Odia Native-CoT Translator")

def get_pending_files():
    if not os.path.exists(INPUT_DIR):
        return []
    # Get all skeleton files
    all_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.json')])
    pending = []
    # Check which ones haven't been translated yet
    for f in all_files:
        out_name = f.replace("skeleton_", "gold_")
        if not os.path.exists(os.path.join(OUTPUT_DIR, out_name)):
            pending.append(f)
    return pending

pending_files = get_pending_files()

if not pending_files:
    st.success("🎉 All files translated! You are done with this batch.")
    st.stop()

# Load the first pending file
current_file = pending_files[0]
input_path = os.path.join(INPUT_DIR, current_file)

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

st.title(f"🛠️ Translation Workbench - {current_file}")
st.write(f"Remaining in this batch: {len(pending_files)}")

# Create a two-column layout
col1, col2 = st.columns(2)

# LEFT COLUMN: The English/Skeleton Context
with col1:
    st.header("Context (English & Skeleton)")
    
    st.subheader("Original English Problem")
    st.info(data.get("original_problem", ""))
    
    st.subheader("Odia Anchored Problem (Helper)")
    st.warning(data.get("deconstructed_problem", ""))
    
    st.subheader("Reasoning Steps (Skeletons)")
    for i, step in enumerate(data.get("skeleton_steps", [])):
        st.markdown(f"**Step {i+1}:** {step}")
        
    st.subheader("Final Answer")
    st.success(data.get("final_answer", ""))

# RIGHT COLUMN: Your Translation Input
with col2:
    st.header("📝 Native Odia Translation")
    
    with st.form(key="translation_form"):
        translated_problem = st.text_area("1. Translated Problem (Instruction):", height=100)
        
        st.markdown("### 2. Reasoning Trace")
        st.caption("Write the full reasoning flow here. Do NOT type the `<think>` tags; the app will add them automatically when you save.")
        translated_reasoning = st.text_area("Native Odia Reasoning:", height=250)
        
        translated_answer = st.text_input("3. Translated Final Answer:")
        
        submit_button = st.form_submit_button(label="💾 Save & Load Next")
        
        if submit_button:
            if not translated_problem or not translated_reasoning or not translated_answer:
                st.error("Please fill out all 3 fields before saving!")
            else:
                output_filename = current_file.replace("skeleton_", "gold_")
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                
                # Format exactly as specified in the Kakugo pipeline for your SLM
                final_data = {
                    "id": data.get("id", current_file),
                    "instruction": translated_problem,
                    "response": f"<think>\n{translated_reasoning}\n</think>\n{translated_answer}"
                }
                
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(final_data, f, indent=4, ensure_ascii=False)
                    
                st.rerun()
