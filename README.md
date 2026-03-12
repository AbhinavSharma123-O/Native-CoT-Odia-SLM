# Native-CoT Odia SLM Dataset Pipeline

## Overview
This repository contains a complete data engineering pipeline designed to generate a high-quality, Native Chain-of-Thought (CoT) reasoning dataset in Odia. The final dataset is built specifically for fine-tuning Small Language Models (like Gemma-2-2B) to perform complex mathematical and logical reasoning natively in a low-resource language.

## The Problem
Odia lacks robust, mathematically accurate training data for AI. Fully automated translation of English mathematical logic into Odia often results in broken algebra, hallucinated numbers, and unnatural phrasing. This makes standard translation APIs insufficient for creating reasoning datasets.

## The Solution: A Hybrid "Cyborg" Pipeline
To ensure maximum data quality for model fine-tuning, this project utilizes a 4-step human-in-the-loop architecture:

### 1. Data Generation (`01_generate_teacher_cot.py`)
Uses the Groq API (Llama-3.3-70B) to generate 1,000 highly complex, multi-step math and logic word problems. The output is strictly formatted JSON containing the problem, reasoning steps, and the final answer.

### 2. Syntax Anchoring (`02_deconstruct_syntax.py`)
A custom Python engine that scans the raw English traces and automatically injects native Odia mathematical terminology (e.g., replacing "sum" with "ସମଷ୍ଟି (sum)"). This creates a hybrid English-Odia skeleton that standardizes the vocabulary for the translation phase.

### 3. Translation Workbench (`ui/translator_app.py`)
A local Streamlit web application providing a split-screen interface. It allows human translators to read the anchored skeletons and manually craft grammatically perfect, mathematically sound Odia translations. The app automatically formats the output with the necessary `<think>` tags required for reasoning models.

### 4. Dataset Compiler (`03_format_dataset.py`)
Consolidates the validated, human-reviewed JSON files into a final `.jsonl` format, ready for distribution on Hugging Face and immediate SLM fine-tuning.

## How to Contribute
If you are a native Odia speaker and want to help build foundational open-source AI resources for the language, your contributions are highly welcome.

1. Clone this repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Launch the translation workbench: `streamlit run ui/translator_app.py`
4. Translate the raw problems into Odia using the provided Streamlit UI.
5. Submit a pull request with your newly generated JSON files located in the `data/final_odia_gold/` folder.