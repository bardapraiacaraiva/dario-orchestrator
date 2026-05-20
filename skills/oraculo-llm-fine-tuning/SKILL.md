---
name: oraculo-llm-fine-tuning
description: LLM fine-tuning — LoRA, QLoRA, full fine-tune, PEFT, DPO, ORPO. Triggers em "fine-tuning", "LoRA", "QLoRA", "PEFT", "DPO", "ORPO", "instruction tuning", "domain adaptation".
license: MIT
parent_agent: oraculo-director
---

# ORACULO-LLM-FINE-TUNING

## Methods
- **Full fine-tune:** all parameters trained ($$$, full GPU)
- **LoRA (Low-Rank Adaptation):** decompose weight updates (95% savings)
- **QLoRA:** quantized LoRA (4-bit) for consumer GPUs
- **PEFT (Parameter-Efficient Fine-Tuning):** family of methods
- **DPO (Direct Preference Optimization):** alternative to RLHF
- **ORPO:** preference learning + SFT combined
- **Instruction tuning:** SFT on prompt-response pairs
- **Domain adaptation:** continued pretraining on domain corpus

## Stack
- **Hugging Face transformers + PEFT**
- **TRL (Transformer Reinforcement Learning)** — RLHF library
- **axolotl** — config-driven fine-tuning
- **LLaMA-Factory** — training UI
- **Unsloth** — 2x speed fine-tuning
- **Together.AI / Replicate** — managed fine-tuning
- **OpenAI fine-tuning** — managed (GPT-4o-mini, GPT-3.5)

## Hardware
- **Consumer:** RTX 4090 (24GB) — QLoRA 7-13B
- **Prosumer:** RTX 6000 Ada (48GB) — QLoRA 70B
- **Workstation:** 4x A100 (320GB) — full 70B
- **Server:** 8x H100 (640GB) — large training
- **Cloud:** RunPod, Vast.ai, Lambda Labs (hourly)

## Data requirements
- **Instruction tuning:** 1K-10K examples
- **Style transfer:** 100-1K examples
- **Domain adaptation:** 100M+ tokens
- **Preference learning:** 5K-50K paired examples

## Templates
1. Fine-tuning project setup
2. Dataset curation + cleaning
3. Hyperparameter search
4. Eval before deploy
5. Deployment (vLLM, TGI, Ollama)
6. Cost calculator (hours × GPU rate)

## Cross-references
- [[demeter-ml-pipelines]] · [[oraculo-evaluation-frameworks]] · [[oraculo-multimodal-research]]
