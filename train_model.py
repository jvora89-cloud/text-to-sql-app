#!/usr/bin/env python3
"""
AI Model Fine-Tuning Pipeline for Text-to-SQL

This script fine-tunes language models using collected user data to improve
SQL generation accuracy. Uses PEFT/LoRA for efficient fine-tuning.

Usage:
    python train_model.py --model mistral --min-feedback 10 --output models/fine-tuned-v1
"""

import sqlite3
import json
import argparse
from datetime import datetime
from pathlib import Path

def export_training_data(min_positive_feedback=5, output_file="training_data.jsonl"):
    """
    Export high-quality training examples from database

    Args:
        min_positive_feedback: Minimum positive feedback count to include
        output_file: Output JSONL file path
    """
    conn = sqlite3.connect('training_data.db')
    cursor = conn.cursor()

    # Get queries with positive feedback or corrections
    query = '''
        SELECT DISTINCT
            ql.user_query,
            COALESCE(uf.corrected_sql, ql.generated_sql) as sql,
            ql.execution_success,
            COUNT(CASE WHEN uf.feedback_type = 'positive' THEN 1 END) as positive_count,
            COUNT(CASE WHEN uf.feedback_type = 'correction' THEN 1 END) as correction_count
        FROM query_logs ql
        LEFT JOIN user_feedback uf ON ql.id = uf.query_log_id
        WHERE ql.execution_success = 1
        GROUP BY ql.id
        HAVING positive_count >= ? OR correction_count > 0
        ORDER BY positive_count DESC, correction_count DESC
    '''

    cursor.execute(query, (min_positive_feedback,))
    results = cursor.fetchall()

    # Export to JSONL format for training
    training_examples = []
    with open(output_file, 'w') as f:
        for row in results:
            user_query, sql, success, pos_count, corr_count = row

            # Format as instruction-following example
            example = {
                "instruction": "Convert this natural language question to SQL.",
                "input": user_query,
                "output": sql,
                "metadata": {
                    "positive_feedback": pos_count,
                    "has_correction": corr_count > 0,
                    "execution_success": bool(success)
                }
            }

            f.write(json.dumps(example) + '\n')
            training_examples.append(example)

    conn.close()

    print(f"✅ Exported {len(training_examples)} training examples to {output_file}")
    return training_examples


def get_verified_examples(output_file="verified_examples.jsonl"):
    """Export manually verified examples"""
    conn = sqlite3.connect('training_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT natural_language, correct_sql, difficulty_level
        FROM verified_examples
        WHERE used_in_training = 0
        ORDER BY difficulty_level, verified_date DESC
    ''')

    results = cursor.fetchall()
    verified_count = 0

    with open(output_file, 'w') as f:
        for nl, sql, difficulty in results:
            example = {
                "instruction": "Convert this natural language question to SQL.",
                "input": nl,
                "output": sql,
                "metadata": {
                    "verified": True,
                    "difficulty": difficulty
                }
            }
            f.write(json.dumps(example) + '\n')
            verified_count += 1

    # Mark as used in training
    cursor.execute('UPDATE verified_examples SET used_in_training = 1')
    conn.commit()
    conn.close()

    print(f"✅ Exported {verified_count} verified examples to {output_file}")
    return verified_count


def create_training_script(model_type="mistral", output_dir="models/fine-tuned"):
    """
    Create a training script for fine-tuning with PEFT/LoRA

    This generates a Python script that can be run separately with GPU resources
    """

    training_script = f'''#!/usr/bin/env python3
"""
Generated Fine-Tuning Script
Model: {model_type}
Generated: {datetime.now().isoformat()}

Prerequisites:
    pip install transformers peft accelerate bitsandbytes datasets torch

Run with:
    python fine_tune_{model_type}.py
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import json

# Model configuration
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
OUTPUT_DIR = "{output_dir}"
TRAINING_DATA = "training_data.jsonl"

# LoRA configuration for efficient fine-tuning
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    load_best_model_at_end=True,
    report_to="none"
)

def load_training_data():
    """Load and preprocess training data"""
    dataset = load_dataset('json', data_files=TRAINING_DATA, split='train')

    def format_instruction(example):
        prompt = f"""{{instruction}}

Input: {{input}}

Output:"""

        text = prompt.format(
            instruction=example['instruction'],
            input=example['input']
        ) + f" {{example['output']}}"

        return {{"text": text}}

    return dataset.map(format_instruction)

def main():
    print("🚀 Starting model fine-tuning...")
    print(f"📊 Model: {{MODEL_NAME}}")
    print(f"💾 Output: {{OUTPUT_DIR}}")

    # Load model and tokenizer
    print("\\n📥 Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        load_in_8bit=True,  # Use 8-bit for memory efficiency
        device_map="auto",
        torch_dtype=torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    # Prepare model for training
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, lora_config)

    print("\\n📊 Trainable parameters:")
    model.print_trainable_parameters()

    # Load training data
    print("\\n📁 Loading training data...")
    train_dataset = load_training_data()
    print(f"✅ Loaded {{len(train_dataset)}} examples")

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer
    )

    # Train
    print("\\n🎓 Starting training...")
    trainer.train()

    # Save
    print(f"\\n💾 Saving model to {{OUTPUT_DIR}}...")
    trainer.save_model()
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("\\n✅ Training complete!")
    print(f"📁 Model saved to: {{OUTPUT_DIR}}")
    print("\\n🚀 To use this model, update app.py to load from this directory")

if __name__ == "__main__":
    main()
'''

    script_path = f"fine_tune_{model_type}.py"
    with open(script_path, 'w') as f:
        f.write(training_script)

    Path(script_path).chmod(0o755)  # Make executable

    print(f"✅ Created training script: {script_path}")
    print(f"📝 Review and run: python {script_path}")

    return script_path


def create_requirements():
    """Create requirements file for training"""
    requirements = """# AI Training Requirements
transformers>=4.35.0
peft>=0.7.0
accelerate>=0.24.0
bitsandbytes>=0.41.0
datasets>=2.15.0
torch>=2.1.0
sentencepiece>=0.1.99
protobuf>=3.20.0
"""

    with open("requirements_training.txt", 'w') as f:
        f.write(requirements)

    print("✅ Created requirements_training.txt")


def main():
    parser = argparse.ArgumentParser(description="AI Model Fine-Tuning Pipeline")
    parser.add_argument('--model', default='mistral', choices=['mistral', 'flan-t5'],
                      help='Model to fine-tune')
    parser.add_argument('--min-feedback', type=int, default=5,
                      help='Minimum positive feedback count')
    parser.add_argument('--output', default='models/fine-tuned-v1',
                      help='Output directory for fine-tuned model')
    parser.add_argument('--export-only', action='store_true',
                      help='Only export data, don\'t create training script')

    args = parser.parse_args()

    print("=" * 60)
    print("🤖 AI Model Fine-Tuning Pipeline")
    print("=" * 60)

    # Step 1: Export training data
    print("\\n📊 Step 1: Exporting training data from database...")
    training_examples = export_training_data(args.min_feedback)

    # Step 2: Export verified examples
    print("\\n✅ Step 2: Exporting verified examples...")
    verified_count = get_verified_examples()

    total_examples = len(training_examples) + verified_count
    print(f"\\n📈 Total training examples: {total_examples}")

    if total_examples < 10:
        print("\\n⚠️  WARNING: Less than 10 training examples!")
        print("   Collect more user feedback before training to avoid overfitting.")
        return

    if not args.export_only:
        # Step 3: Create training script
        print("\\n🔧 Step 3: Creating fine-tuning script...")
        script_path = create_training_script(args.model, args.output)

        # Step 4: Create requirements
        print("\\n📦 Step 4: Creating requirements file...")
        create_requirements()

        print("\\n" + "=" * 60)
        print("✅ TRAINING PIPELINE READY")
        print("=" * 60)
        print(f"\\n📁 Training data: training_data.jsonl ({len(training_examples)} examples)")
        print(f"📁 Verified data: verified_examples.jsonl ({verified_count} examples)")
        print(f"🔧 Training script: {script_path}")
        print(f"📦 Requirements: requirements_training.txt")
        print(f"\\n🚀 Next steps:")
        print(f"   1. Install training requirements: pip install -r requirements_training.txt")
        print(f"   2. Run training script: python {script_path}")
        print(f"   3. Wait for training to complete (may take hours on GPU)")
        print(f"   4. Update app.py to use fine-tuned model from: {args.output}")
        print("\\n💡 Tip: Run training on a machine with GPU for faster results")

if __name__ == "__main__":
    main()
