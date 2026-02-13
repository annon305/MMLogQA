# Multimodal Log-based Question Answering (MMLOGQA)

This repository contains the code and datasets for the paper: **"A Multimodal Log-based Question Answering Framework for Technical Support"**.

## Abstract

This study presents a multimodal log-based question answering (QA) framework that addresses user queries by jointly reasoning over device-centric and cloud-centric multimodal logs. To support this task, we construct two specialized datasets: (1) a Cloud-centric Technical Question Answering dataset (**CTQA**) and (2) a Device-centric Technical Question Answering dataset (**DTQA**). Both datasets are collected from open technical forums and validated under domain expert supervision to ensure technical correctness and quality. 

We establish comprehensive baselines using four large language models (LLMs), three vision-language models (VLMs), and OCR-augmented pipelines across three inference paradigms: Zero-Shot, Chain-of-Thought (CoT), and Supervised Fine-Tuning (SFT). To further enhance reliability and alignment, we introduce **Explanation-Guided Direct Preference Optimization (EG-DPO)**, which leverages rationales for both correct and incorrect answers and explicitly trains models to abstain on unanswerable queries. 

We evaluate both datasets using automatic metrics, including BLEU, ROUGE-L, ROUGE-Lsum, METEOR, and BERT-F1. Recognizing the limitations of lexical-overlap metrics, we additionally conduct LLM-as-Judge and human expert evaluations for more reliable assessment. This research is motivated by the evolving needs of the software industry and individual developers, aiming to provide robust benchmark resources for future research in multimodal reasoning and log-based QA systems.

## Key Features

- **Datasets**: Specialized CTQA and DTQA datasets collected from technical forums.
- **Inference Paradigms**: Benchmarks for Zero-Shot, CoT, and SFT.
- **EG-DPO**: A novel Direct Preference Optimization approach using explanation-guided rationales.
- **Expert Evaluation**: Integrated framework for LLM-as-Judge and expert human review alignment.

## Repository Structure

```text
.
├── Dataset/                   # Core CTQA and DTQA data
│   ├── testset/               # Standardized test sets (Cloud/Device)
│   └── raw_data/              # Raw multimodal data (images, logs)
├── Baseline/                  # Baseline model implementations
├── Training/                  # Training scripts for SFT and EG-DPO
├── Ocr/                       # OCR-augmented pipeline scripts
└── Evaluation_Judgement/      # LLM-as-Judge and Human Expert Evaluation
    ├── LLM_Judge/             # LLM Judge scoring modules
    └── Human_Judge/           # Expert human review modules
```

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd MMLOGQA_CODEBASE
   ```
2. **Usage**: Jupyter notebooks for LLM-as-Judge scoring are located in `Evaluation_Judgement/LLM_Judge/Code/`.
