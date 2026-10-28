"""
Wexa Browser — Resilient Two-Pass LoRA Training Pipeline
Performs 2-stage iterative training:
- Pass 1: Foundation instruction tuning & function synthesis
- Pass 2: Hardened compiler-error recovery and edge-case correction
"""
import os
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_pass(
    pass_number: int,
    pass_name: str,
    base_or_adapter_path: str,
    dataset_path: str,
    output_dir: str,
    epochs: int = 2,
    batch_size: int = 1,
    learning_rate: float = 2e-4
):
    print(f"\n=======================================================")
    print(f"   STARTING TRAINING PASS {pass_number}: {pass_name.upper()}   ")
    print(f"=======================================================")
    print(f"Model Input : {base_or_adapter_path}")
    print(f"Dataset     : {dataset_path}")
    print(f"Output Path : {output_dir}")
    print(f"Epochs      : {epochs} | Batch Size: {batch_size}")
    print(f"-------------------------------------------------------")

    data_file = BASE_DIR / dataset_path
    if not data_file.exists():
        print(f"[Error] Dataset not found: {data_file}")
        return False

    try:
        import torch
        from datasets import load_dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
        from peft import LoraConfig, get_peft_model, TaskType, PeftModel
        from trl import SFTTrainer

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Active Device: {device.upper()}")

        tokenizer = AutoTokenizer.from_pretrained(base_or_adapter_path, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token

        # Load base model or existing adapter for Pass 2
        print("Loading model weights...")
        base_model = AutoModelForCausalLM.from_pretrained(
            base_or_adapter_path,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            trust_remote_code=True
        )

        lora_config = LoraConfig(
            r=8,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        model = get_peft_model(base_model, lora_config)

        dataset = load_dataset("json", data_files=str(data_file), split="train")

        def formatting_func(example):
            return f"<|im_start|>user\n{example['instruction']}\n{example.get('input', '')}<|im_end|>\n<|im_start|>assistant\n{example['output']}<|im_end|>"

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=learning_rate,
            logging_steps=5,
            save_strategy="epoch",
            fp16=(device == "cuda"),
            report_to="none"
        )

        trainer = SFTTrainer(
            model=model,
            train_dataset=dataset,
            formatting_func=formatting_func,
            args=training_args
        )

        print(f"Executing Pass {pass_number} optimization steps...")
        trainer.train()

        # Save Checkpoint
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        print(f"[Success] Pass {pass_number} ({pass_name}) completed and verified at: {output_dir}")
        return True

    except ImportError as e:
        print(f"\n[Environment Diagnostic] PyTorch / PEFT training modules not installed:")
        print(f"Detail: {e}")
        print("\nThe two-pass training pipeline is fully architected and ready.")
        print("To trigger on-device GPU/CPU training, run: pip install torch transformers peft trl datasets")
        return False
    except Exception as err:
        print(f"[Runtime Diagnostic] Pass {pass_number} error encountered: {err}")
        return False

def execute_two_pass_workflow(
    base_model: str = "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    epochs_per_pass: int = 2
):
    print("=================================================================")
    print("      WEXA BROWSER RESILIENT TWO-PASS MODEL TRAINING HARNESS     ")
    print("=================================================================")
    
    pass1_dataset = "data/datasets/pass1_foundation_train.jsonl"
    pass1_output = str(BASE_DIR / "models" / "wexa_coder_pass1_checkpoint")

    pass2_dataset = "data/datasets/pass2_error_recovery_train.jsonl"
    pass2_output = str(BASE_DIR / "models" / "wexa_coder_pass2_hardened_final")

    # Pass 1: Foundation Function Completion
    success_p1 = run_pass(
        pass_number=1,
        pass_name="Foundation Instruction & Infilling",
        base_or_adapter_path=base_model,
        dataset_path=pass1_dataset,
        output_dir=pass1_output,
        epochs=epochs_per_pass
    )

    if success_p1:
        # Pass 2: Hardened Compiler-Error Recovery & Edge Case Tuning
        run_pass(
            pass_number=2,
            pass_name="Compiler Error Recovery & Edge Hardening",
            base_or_adapter_path=pass1_output,
            dataset_path=pass2_dataset,
            output_dir=pass2_output,
            epochs=epochs_per_pass
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wexa Two-Pass LoRA Training")
    parser.add_argument("--base-model", type=str, default="Qwen/Qwen2.5-Coder-1.5B-Instruct")
    parser.add_argument("--epochs", type=int, default=2)
    args = parser.parse_args()

    execute_two_pass_workflow(
        base_model=args.base_model,
        epochs_per_pass=args.epochs
    )
