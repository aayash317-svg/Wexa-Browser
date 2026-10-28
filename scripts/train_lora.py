"""
Wexa Browser — Automated LoRA / QLoRA Fine-Tuning Pipeline
Trains our custom Wexa Coder model using collected user interactions and dataset files.
"""
import os
import argparse
from pathlib import Path

def train_wexa_lora(
    base_model_name: str = "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    dataset_path: str = "data/datasets/wexa_coder_finetune.jsonl",
    output_dir: str = "models/wexa_coder_lora_checkpoint",
    epochs: int = 3,
    batch_size: int = 1,
    learning_rate: float = 2e-4
):
    print(f"==================================================")
    print(f"        Wexa Coder LoRA Training Pipeline         ")
    print(f"==================================================")
    print(f"Base Model : {base_model_name}")
    print(f"Dataset    : {dataset_path}")
    print(f"Output Dir : {output_dir}")
    print(f"Epochs     : {epochs} | Batch Size: {batch_size}")
    print(f"==================================================")

    data_file = Path(dataset_path)
    if not data_file.exists():
        print(f"[Error] Dataset file not found: {data_file}")
        print("Tip: Run the browser and solve problems to automatically generate telemetry,")
        print("or run 'python scripts/dataset_downloader.py --create-starter'")
        return

    try:
        import torch
        from datasets import load_dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
        from peft import LoraConfig, get_peft_model, TaskType
        from trl import SFTTrainer

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Running on hardware device: {device}")

        # 1. Load Tokenizer & Model
        print("Loading tokenizer and base model...")
        tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            trust_remote_code=True
        )

        # 2. Configure LoRA
        lora_config = LoraConfig(
            r=8,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

        # 3. Load Dataset
        dataset = load_dataset("json", data_files=str(data_file), split="train")

        def formatting_prompts_func(example):
            return f"<|im_start|>user\n{example['instruction']}<|im_end|>\n<|im_start|>assistant\n{example['output']}<|im_end|>"

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=learning_rate,
            logging_steps=10,
            save_strategy="epoch",
            fp16=(device == "cuda"),
            report_to="none"
        )

        trainer = SFTTrainer(
            model=model,
            train_dataset=dataset,
            formatting_func=formatting_prompts_func,
            args=training_args
        )

        print("Starting training run...")
        trainer.train()
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        print(f"Training completed successfully! Saved to: {output_dir}")

    except ImportError as e:
        print(f"[Notice] Training dependencies not installed yet: {e}")
        print("To run local fine-tuning when ready, install:")
        print("pip install torch transformers peft trl datasets")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wexa LoRA Fine-Tuning Harness")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-Coder-1.5B-Instruct")
    parser.add_argument("--data", type=str, default="data/datasets/starter_coding_eval.jsonl")
    parser.add_argument("--output", type=str, default="models/wexa_coder_lora")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    train_wexa_lora(
        base_model_name=args.model,
        dataset_path=args.data,
        output_dir=args.output,
        epochs=args.epochs
    )
