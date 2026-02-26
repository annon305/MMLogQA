# Multimodal Log-based Question Answering (MMLOGQA)

This repository contains the code and datasets for the paper: **"A Multimodal Log-based Question Answering"**.

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
├── data/                      # CTQA and DTQA datasets
│   ├── raw/                   # Raw logs and images
│   ├── processed/             # Refined data (e.g., OCR-extracted)
│   ├── splits/                # Training/test partitions (Cloud/Device)
│   └── eval/                  # Evaluation-ready sets
├── models/                    # Model weights and baseline configs
│   ├── baselines/             # OCR, Text, and VLM implementations
│   ├── sft/                   # Supervised fine-tuning artifacts
│   └── dpo/                   # EG-DPO alignment artifacts
├── training/                  # Fine-tuning pipelines
│   ├── sft/                   # Llama 3.1 SFT notebooks
│   └── dpo/                   # EG-DPO alignment notebooks
├── notebooks/                 # Key processing & analysis pipelines
│   ├── ocr_pipeline.ipynb     # Visual log text extraction
│   ├── dataset_pipeline.ipynb # End-to-end data processing
│   └── dataset_analysis.ipynb # Statistical dataset overview
├── evaluation/                # Benchmarking and Alignment
│   ├── automatic/             # BLEU, ROUGE, METEOR scoring
│   └── llm_judge/             # LLM-as-Judge & expert review modules
├── scraping/                  # Data collection workflows
│   ├── cloud/                 # Cloud-centric logs scraping
│   └── device/                # Device-centric logs scraping
└── outputs/                   # Model generation and evaluation results
```

## Getting Started

### Environment Setup

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Abrahamkaikobad/MMlogQA.git
cd MMlogQA
pip install -r requirements.txt
```
