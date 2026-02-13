#!/usr/bin/env python3
"""
Second pass: Standardize intermediate JSONL output paths in VLM and LLM_OCR notebooks.
These are runtime inference artifacts (success/failed logs).
"""

import json
import os

BASE_DIR = "/Users/abrahamkaikobad/Desktop/MMLOGQA_CODEBASE/Baseline"

# VLM  intermediate JSONL outputs
VLM_JSONL_REPLACEMENTS = {
    "vlm_code_llama_3_2_vl_11b.ipynb": {
        '"cloud_logs_qa-vlm-zero-shot-generated-responses.jsonl"': '"vlm_cloud_llama_3_2_vl_11b_zero_shot_results.jsonl"',
        '"cloud_logs_qa-vlm-cot-generated-responses.jsonl"': '"vlm_cloud_llama_3_2_vl_11b_cot_results.jsonl"',
        '"device_logs_qa-vlm-zero-shot-generated-responses.jsonl"': '"vlm_device_llama_3_2_vl_11b_zero_shot_results.jsonl"',
        '"device_logs_qa-vlm-cot-generated-responses.jsonl"': '"vlm_device_llama_3_2_vl_11b_cot_results.jsonl"',
    },
    "vlm_code_llava1_5_vl_7b.ipynb": {
        '"cloud_logs_qa-vlm-zero-shot-generated-responses.jsonl"': '"vlm_cloud_llava1_5_vl_7b_zero_shot_results.jsonl"',
        '"cloud_logs_qa-vlm-cot-generated-responses.jsonl"': '"vlm_cloud_llava1_5_vl_7b_cot_results.jsonl"',
        '"device_logs_qa-vlm-zero-shot-generated-responses.jsonl"': '"vlm_device_llava1_5_vl_7b_zero_shot_results.jsonl"',
        '"device_logs_qa-vlm-cot-generated-responses.jsonl"': '"vlm_device_llava1_5_vl_7b_cot_results.jsonl"',
    },
    "vlm_code_qwen2_5_vl_7b.ipynb": {
        '"cloud_logs_qa-vlm-zero-shot-generated-responses.jsonl"': '"vlm_cloud_qwen2_5_vl_7b_zero_shot_results.jsonl"',
        '"cloud_logs_qa-vlm-cot-generated-responses.jsonl"': '"vlm_cloud_qwen2_5_vl_7b_cot_results.jsonl"',
        '"device_logs_qa-vlm-zero-shot-generated-responses.jsonl"': '"vlm_device_qwen2_5_vl_7b_zero_shot_results.jsonl"',
        '"device_logs_qa-vlm-cot-generated-responses.jsonl"': '"vlm_device_qwen2_5_vl_7b_cot_results.jsonl"',
    },
}

# LLM_OCR intermediate JSONL outputs (model-specific names already somewhat okay, but let's standardize)
LLM_OCR_JSONL_REPLACEMENTS = {
    "llm_ocr_code_llama_3_1_8b_instruct.ipynb": {
        # Sample outputs
        '"sample_zero_shot_results.jsonl"': '"llm_ocr_sample_llama_3_1_8b_instruct_zero_shot_results.jsonl"',
        '"failed_sample_zero_shot-results.jsonl"': '"llm_ocr_sample_llama_3_1_8b_instruct_zero_shot_failed.jsonl"',
        '"sample_cot_results.jsonl"': '"llm_ocr_sample_llama_3_1_8b_instruct_cot_results.jsonl"',
        '"failed_sample_cot_results.jsonl"': '"llm_ocr_sample_llama_3_1_8b_instruct_cot_failed.jsonl"',
        # Cloud
        '"llama_cloud_zero_shot_results.jsonl"': '"llm_ocr_cloud_llama_3_1_8b_instruct_zero_shot_results.jsonl"',
        '"llama_cloud_failed_zero_shot_results.jsonl"': '"llm_ocr_cloud_llama_3_1_8b_instruct_zero_shot_failed.jsonl"',
        '"llama_cloud_cot_results.jsonl"': '"llm_ocr_cloud_llama_3_1_8b_instruct_cot_results.jsonl"',
        '"llama_cloud_failed_cot_results.jsonl"': '"llm_ocr_cloud_llama_3_1_8b_instruct_cot_failed.jsonl"',
        # Device
        '"llama_device_zero_shot_results.jsonl"': '"llm_ocr_device_llama_3_1_8b_instruct_zero_shot_results.jsonl"',
        '"llama_device_failed_zero_shot_results.jsonl"': '"llm_ocr_device_llama_3_1_8b_instruct_zero_shot_failed.jsonl"',
        '"llama_device_cot_results.jsonl"': '"llm_ocr_device_llama_3_1_8b_instruct_cot_results.jsonl"',
        '"llama_device_failed_cot_results.jsonl"': '"llm_ocr_device_llama_3_1_8b_instruct_cot_failed.jsonl"',
    },
    "llm_ocr_code_qwen_7b.ipynb": {
        '"sample_zero_shot_results.jsonl"': '"llm_ocr_sample_qwen_7b_zero_shot_results.jsonl"',
        '"failed_sample_zero_shot-results.jsonl"': '"llm_ocr_sample_qwen_7b_zero_shot_failed.jsonl"',
        '"sample_cot_results.jsonl"': '"llm_ocr_sample_qwen_7b_cot_results.jsonl"',
        '"failed_sample_cot_results.jsonl"': '"llm_ocr_sample_qwen_7b_cot_failed.jsonl"',
        '"qwen_cloud_zero_shot_results.jsonl"': '"llm_ocr_cloud_qwen_7b_zero_shot_results.jsonl"',
        '"qwen_cloud_failed_zero_shot_results.jsonl"': '"llm_ocr_cloud_qwen_7b_zero_shot_failed.jsonl"',
        '"qwen_cloud_cot_results.jsonl"': '"llm_ocr_cloud_qwen_7b_cot_results.jsonl"',
        '"qwen_cloud_failed_cot_results.jsonl"': '"llm_ocr_cloud_qwen_7b_cot_failed.jsonl"',
        '"qwen_device_zero_shot_results.jsonl"': '"llm_ocr_device_qwen_7b_zero_shot_results.jsonl"',
        '"qwen_device_failed_zero_shot_results.jsonl"': '"llm_ocr_device_qwen_7b_zero_shot_failed.jsonl"',
        '"qwen_device_cot_results.jsonl"': '"llm_ocr_device_qwen_7b_cot_results.jsonl"',
        '"qwen_device_failed_cot_results.jsonl"': '"llm_ocr_device_qwen_7b_cot_failed.jsonl"',
    },
    "llm_ocr_code_mistral_8b_instruct_2410.ipynb": {
        '"sample_zero_shot_results.jsonl"': '"llm_ocr_sample_mistral_8b_instruct_2410_zero_shot_results.jsonl"',
        '"failed_sample_zero_shot-results.jsonl"': '"llm_ocr_sample_mistral_8b_instruct_2410_zero_shot_failed.jsonl"',
        '"sample_cot_results.jsonl"': '"llm_ocr_sample_mistral_8b_instruct_2410_cot_results.jsonl"',
        '"failed_sample_cot_results.jsonl"': '"llm_ocr_sample_mistral_8b_instruct_2410_cot_failed.jsonl"',
        '"ministral_cloud_zero_shot_results.jsonl"': '"llm_ocr_cloud_mistral_8b_instruct_2410_zero_shot_results.jsonl"',
        '"ministral_cloud_failed_zero_shot_results.jsonl"': '"llm_ocr_cloud_mistral_8b_instruct_2410_zero_shot_failed.jsonl"',
        '"ministral_cloud_cot_results.jsonl"': '"llm_ocr_cloud_mistral_8b_instruct_2410_cot_results.jsonl"',
        '"ministral_cloud_failed_cot_results.jsonl"': '"llm_ocr_cloud_mistral_8b_instruct_2410_cot_failed.jsonl"',
        '"ministral_device_zero_shot_results.jsonl"': '"llm_ocr_device_mistral_8b_instruct_2410_zero_shot_results.jsonl"',
        '"ministral_device_failed_zero_shot_results.jsonl"': '"llm_ocr_device_mistral_8b_instruct_2410_zero_shot_failed.jsonl"',
        '"ministral_device_cot_results.jsonl"': '"llm_ocr_device_mistral_8b_instruct_2410_cot_results.jsonl"',
        '"ministral_device_failed_cot_results.jsonl"': '"llm_ocr_device_mistral_8b_instruct_2410_cot_failed.jsonl"',
    },
    "llm_ocr_code_deepseek_r1_distill_qwen_7b.ipynb": {
        '"sample_zero_shot_results.jsonl"': '"llm_ocr_sample_deepseek_r1_distill_qwen_7b_zero_shot_results.jsonl"',
        '"failed_sample_zero_shot-results.jsonl"': '"llm_ocr_sample_deepseek_r1_distill_qwen_7b_zero_shot_failed.jsonl"',
        '"sample_cot_results.jsonl"': '"llm_ocr_sample_deepseek_r1_distill_qwen_7b_cot_results.jsonl"',
        '"failed_sample_cot_results.jsonl"': '"llm_ocr_sample_deepseek_r1_distill_qwen_7b_cot_failed.jsonl"',
        '"deepseekr1_cloud_zero_shot_results.jsonl"': '"llm_ocr_cloud_deepseek_r1_distill_qwen_7b_zero_shot_results.jsonl"',
        '"deepseekr1_cloud_failed_zero_shot_results.jsonl"': '"llm_ocr_cloud_deepseek_r1_distill_qwen_7b_zero_shot_failed.jsonl"',
        '"deepseekr1_cloud_cot_results.jsonl"': '"llm_ocr_cloud_deepseek_r1_distill_qwen_7b_cot_results.jsonl"',
        '"deepseekr1_cloud_failed_cot_results.jsonl"': '"llm_ocr_cloud_deepseek_r1_distill_qwen_7b_cot_failed.jsonl"',
        '"deepseekr1_device_zero_shot_results.jsonl"': '"llm_ocr_device_deepseek_r1_distill_qwen_7b_zero_shot_results.jsonl"',
        '"deepseekr1_device_failed_zero_shot_results.jsonl"': '"llm_ocr_device_deepseek_r1_distill_qwen_7b_zero_shot_failed.jsonl"',
        '"deepseekr1_device_cot_results.jsonl"': '"llm_ocr_device_deepseek_r1_distill_qwen_7b_cot_results.jsonl"',
        '"deepseekr1_device_failed_cot_results.jsonl"': '"llm_ocr_device_deepseek_r1_distill_qwen_7b_cot_failed.jsonl"',
    },
}


def update_notebook(filepath, replacements):
    filename = os.path.basename(filepath)
    print(f"\nProcessing: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    total_changes = 0
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        source_text = ''.join(cell.get('source', []))
        new_source = source_text
        for old, new in replacements.items():
            if old in new_source:
                count = new_source.count(old)
                new_source = new_source.replace(old, new)
                total_changes += count
        if new_source != source_text:
            cell['source'] = new_source.splitlines(keepends=True)
    
    if total_changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"  ✅ {total_changes} replacements applied")
    else:
        print(f"  ⚠️  No changes made")
    return total_changes


def main():
    total = 0
    
    print("VLM JSONL Outputs:")
    for nb_name, reps in VLM_JSONL_REPLACEMENTS.items():
        path = os.path.join(BASE_DIR, "VLM", "code", nb_name)
        if os.path.exists(path):
            total += update_notebook(path, reps)

    print("\nLLM_OCR JSONL Outputs:")
    for nb_name, reps in LLM_OCR_JSONL_REPLACEMENTS.items():
        path = os.path.join(BASE_DIR, "LLM_OCR", "code", nb_name)
        if os.path.exists(path):
            total += update_notebook(path, reps)

    print(f"\nTOTAL: {total} replacements applied")


if __name__ == "__main__":
    main()
