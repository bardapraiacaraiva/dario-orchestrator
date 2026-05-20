---
name: oraculo-multimodal-research
description: Multimodal AI — VLMs, audio, video, embodied, omni-models. Triggers em "multimodal", "VLM", "vision language model", "GPT-4V", "Gemini multimodal", "CLIP", "Flamingo", "omni-model".
license: MIT
parent_agent: oraculo-director
---

# ORACULO-MULTIMODAL-RESEARCH

## Multimodal categories
- **Vision-Language (VLM):** GPT-4V, Gemini, Claude, LLaVA
- **Audio-Language:** Whisper, AudioPaLM, music gen (MusicGen)
- **Video:** Sora (OpenAI), Veo (Google), Movie Gen (Meta), Runway
- **3D:** point clouds, NeRF, Gaussian splatting
- **Embodied:** robotics + language (RT-2 Google)
- **Omni-models:** GPT-4o, Gemini 1.5/2, Claude 3.5+ — handle all natively

## Architecture patterns
- **Cross-attention:** image features → language model
- **Adapter modules:** lightweight modality bridges
- **Unified tokenization:** images → tokens (ViT patches)
- **Multimodal LLMs native:** trained on mixed data from start

## Eval benchmarks
- **MMMU:** Multi-discipline Multimodal Understanding
- **MMBench:** general visual reasoning
- **MathVista:** math + vision
- **POPE:** hallucination evaluation
- **AudioBench:** audio understanding
- **VideoMME:** video understanding

## Stack
- **HuggingFace Transformers + accelerate**
- **LangChain multimodal**
- **LlamaIndex multimodal**
- **Replicate** — hosted model APIs
- **Together.AI** — open model hosting

## Templates
1. Multimodal benchmark suite
2. VLM fine-tuning pipeline
3. Multimodal RAG architecture
4. Hallucination measurement
5. Cross-modal evaluation
6. Embodied agent simulation

## Cross-references
- [[oraculo-model-evaluation]] · [[oraculo-llm-fine-tuning]] · [[oraculo-rag-research]]
