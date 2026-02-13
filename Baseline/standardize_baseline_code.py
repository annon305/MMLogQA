#!/usr/bin/env python3
"""
Standardize all Baseline code notebooks:
1. Update dataset input paths to use standardized relative paths + pd.read_excel
2. Update OCR JSONL input paths (LLM_OCR only) to use standardized relative paths
3. Update response output paths to use standardized relative paths + to_excel
"""

import json
import os

BASE_DIR = "/Users/abrahamkaikobad/Desktop/MMLOGQA_CODEBASE/Baseline"

# ============================================================
# String replacements applied to ALL notebooks
# ============================================================

# Dataset Input Replacements (read_csv -> read_excel, old filenames -> new paths)
GLOBAL_REPLACEMENTS = {
    # ---- Dataset read paths ----
    # Various cloud test dataset references
    'pd.read_csv("reduce-test-cloud.csv")': 'pd.read_excel("../../Dataset/cloud/split_data/cloud_test.xlsx")',
    "pd.read_csv('reduce-test-cloud.csv')": "pd.read_excel('../../Dataset/cloud/split_data/cloud_test.xlsx')",
    'pd.read_csv("cloud_test.csv")': 'pd.read_excel("../../Dataset/cloud/split_data/cloud_test.xlsx")',
    "pd.read_csv('cloud_test.csv')": "pd.read_excel('../../Dataset/cloud/split_data/cloud_test.xlsx')",

    # Various device test dataset references
    'pd.read_csv("reduce-test-device.csv")': 'pd.read_excel("../../Dataset/device/split_data/device_test.xlsx")',
    "pd.read_csv('reduce-test-device.csv')": "pd.read_excel('../../Dataset/device/split_data/device_test.xlsx')",
    'pd.read_csv("device_test.csv")': 'pd.read_excel("../../Dataset/device/split_data/device_test.xlsx")',
    "pd.read_csv('device_test.csv')": "pd.read_excel('../../Dataset/device/split_data/device_test.xlsx')",

    # Absolute Google Drive path (deepseek device)
    'pd.read_csv("/content/drive/MyDrive/scrap/Device/QA/train_test_split/reduced_version/multimodal/reduce-test.csv")':
        'pd.read_excel("../../Dataset/device/split_data/device_test.xlsx")',

    # With spaces around = 
    'cloud = pd.read_csv("reduce-test-cloud.csv")': 'cloud = pd.read_excel("../../Dataset/cloud/split_data/cloud_test.xlsx")',
    'device = pd.read_csv("reduce-test-device.csv")': 'device = pd.read_excel("../../Dataset/device/split_data/device_test.xlsx")',
    'cloud=pd.read_csv("reduce-test-cloud.csv")': 'cloud=pd.read_excel("../../Dataset/cloud/split_data/cloud_test.xlsx")',
    'device=pd.read_csv("reduce-test-device.csv")': 'device=pd.read_excel("../../Dataset/device/split_data/device_test.xlsx")',
    'cloud=pd.read_csv("cloud_test.csv")': 'cloud=pd.read_excel("../../Dataset/cloud/split_data/cloud_test.xlsx")',
    'device=pd.read_csv("device_test.csv")': 'device=pd.read_excel("../../Dataset/device/split_data/device_test.xlsx")',

    # ---- OCR JSONL Paths (LLM_OCR) ----
    '"cloud-test-img-ocr-response.jsonl"': '"../../Ocr/extracted_data/cloud/ocr_extracted_cloud_test.jsonl"',
    '"device-test-img-ocr-response.jsonl"': '"../../Ocr/extracted_data/device/ocr_extracted_device_test.jsonl"',
}

# ============================================================
# Per-notebook output path replacements
# ============================================================

# LLM_Text notebooks
LLM_TEXT_OUTPUT_REPLACEMENTS = {
    "llm_text_code_llama_3_1_8b_instruct.ipynb": {
        # Sample debug output - keep local but standardize name
        '"sample-llama-instruct-1-response.csv"': '"sample_llm_text_llama_3_1_8b_instruct.csv"',
        '.to_csv("sample_llm_text_llama_3_1_8b_instruct.csv")': '.to_csv("sample_llm_text_llama_3_1_8b_instruct.csv")',
        # Cloud outputs
        '.to_csv("llama-cloud-testset-baseline-zero-shot.csv")': '.to_excel("../responses/cloud/llm_text_response_cloud_llama_3_1_8b_instruct_zero_shot.xlsx", index=False)',
        '.to_csv("llama-cloud-testset-baseline.csv")': '.to_excel("../responses/cloud/llm_text_response_cloud_llama_3_1_8b_instruct_cot.xlsx", index=False)',
        # Device outputs
        '.to_csv("llama-device-testset-baseline-zero-shot.csv")': '.to_excel("../responses/device/llm_text_response_device_llama_3_1_8b_instruct_zero_shot.xlsx", index=False)',
        '.to_csv("llama-device-testset-baseline.csv")': '.to_excel("../responses/device/llm_text_response_device_llama_3_1_8b_instruct_cot.xlsx", index=False)',
    },
    "llm_text_code_qwen_7b.ipynb": {
        '"sample-qwen-response-cloud.csv"': '"sample_llm_text_qwen_7b.csv"',
        '.to_csv("qwen-cloud-testset-baseline.csv")': '.to_excel("../responses/cloud/llm_text_response_cloud_qwen_7b.xlsx", index=False)',
        '.to_csv("qwen-device-testset-baseline.csv")': '.to_excel("../responses/device/llm_text_response_device_qwen_7b.xlsx", index=False)',
    },
    "llm_text_code_mistral_8b_instruct_2410.ipynb": {
        '"sample-ministral-response-cloud.csv"': '"sample_llm_text_mistral_8b_instruct_2410.csv"',
        '.to_csv("ministral-cloud-testset-baseline.csv")': '.to_excel("../responses/cloud/llm_text_response_cloud_mistral_8b_instruct_2410.xlsx", index=False)',
        '.to_csv("ministral-device-testset-baseline.csv")': '.to_excel("../responses/device/llm_text_response_device_mistral_8b_instruct_2410.xlsx", index=False)',
    },
    "llm_text_code_deepseek_r1_distill_qwen_7b.ipynb": {
        '"sample-deepseek-response-cloudx.csv"': '"sample_llm_text_deepseek_r1_distill_qwen_7b.csv"',
        '.to_csv("deepseek-cloud-testset-baseline.csv")': '.to_excel("../responses/cloud/llm_text_response_cloud_deepseek_r1_distill_qwen_7b.xlsx", index=False)',
        '.to_csv("deepseek-device-testset-baseline.csv")': '.to_excel("../responses/device/llm_text_response_device_deepseek_r1_distill_qwen_7b.xlsx", index=False)',
    },
}

# LLM_OCR notebooks
LLM_OCR_OUTPUT_REPLACEMENTS = {
    "llm_ocr_code_llama_3_1_8b_instruct.ipynb": {
        '"sample-llama-instruct-1-response.csv"': '"sample_llm_ocr_llama_3_1_8b_instruct.csv"',
        '.to_csv("llama-cloud-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_llama_3_1_8b_instruct_zero_shot.xlsx", index=False)',
        '.to_csv("llama-cloud-logs-qa-cot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_llama_3_1_8b_instruct.xlsx", index=False)',
        '.to_csv("llama-device-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_llama_3_1_8b_instruct.xlsx", index=False)',
        '.to_csv("llama-device-logs-qa-cot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_llama_3_1_8b_instruct_cot.xlsx", index=False)',
    },
    "llm_ocr_code_qwen_7b.ipynb": {
        '"sample-llama-instruct-1-response.csv"': '"sample_llm_ocr_qwen_7b.csv"',
        '.to_csv("qwen-cloud-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_qwen_7b.xlsx", index=False)',
        '.to_csv("qwen-cloud-logs-qa-cot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_qwen_7b_cot.xlsx", index=False)',
        '.to_csv("qwen-device-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_qwen_7b.xlsx", index=False)',
        '.to_csv("qwen-device-logs-qa-cot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_qwen_7b_cot.xlsx", index=False)',
    },
    "llm_ocr_code_mistral_8b_instruct_2410.ipynb": {
        '"sample-llama-instruct-1-response.csv"': '"sample_llm_ocr_mistral_8b_instruct_2410.csv"',
        '.to_csv("ministral-cloud-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_mistral_8b_instruct_2410.xlsx", index=False)',
        '.to_csv("ministral-cloud-logs-qa-cot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_mistral_8b_instruct_2410_cot.xlsx", index=False)',
        '.to_csv("ministral-device-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_mistral_8b_instruct_2410.xlsx", index=False)',
        '.to_csv("ministral-device-logs-qa-cot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_mistral_8b_instruct_2410_cot.xlsx", index=False)',
    },
    "llm_ocr_code_deepseek_r1_distill_qwen_7b.ipynb": {
        '"sample-deepseekr1-response.csv"': '"sample_llm_ocr_deepseek_r1_distill_qwen_7b.csv"',
        '.to_csv("deepseekr1-cloud-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_deepseek_r1_distill_qwen_7b_zero_shot.xlsx", index=False)',
        '.to_csv("deepseekr1-cloud-logs-qa-cot-generated-responses.csv")': '.to_excel("../responses/cloud/llm_ocr_response_cloud_deepseek_r1_distill_qwen_7b.xlsx", index=False)',
        '.to_csv("deepseekr1-device-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_deepseek_r1_distill_qwen_7b_zero_shot.xlsx", index=False)',
        # This one appears to be duplicated in the notebook (same filename for both zero-shot and cot device)
        '.to_csv("deepseekr1-device-logs-qa-zero-shot-generated-responses.csv")': '.to_excel("../responses/device/llm_ocr_response_device_deepseek_r1_distill_qwen_7b_zero_shot.xlsx", index=False)',
    },
}

# VLM notebooks
VLM_OUTPUT_REPLACEMENTS = {
    "vlm_code_llama_3_2_vl_11b.ipynb": {
        '"sample_logs_qa-vlm-zero-shot-generated-responses.csv"': '"sample_vlm_llama_3_2_vl_11b.csv"',
        '.to_csv("cloud_logs_qa-vlm-zero-shot-generated-responses.csv", index=False)': '.to_excel("../responses/cloud/vlm_response_cloud_llama_3_1_8b_instruct.xlsx", index=False)',
        '.to_csv("cloud_logs_qa-vlm-cot-generated-responses.csv", index=False)': '.to_excel("../responses/cloud/vlm_response_cloud_llama_3_1_8b_instruct_cot.xlsx", index=False)',
        '.to_csv("device_logs_qa-vlm-zero-shot-generated-responses.csv", index=False)': '.to_excel("../responses/device/vlm_response_device_llama_3_1_8b_instruct.xlsx", index=False)',
        '.to_csv("device_logs_qa-vlm-cot-generated-responses.csv", index=False)': '.to_excel("../responses/device/vlm_response_device_llama_3_1_8b_instruct_cot.xlsx", index=False)',
    },
    "vlm_code_llava1_5_vl_7b.ipynb": {
        '.to_csv("cloud_logs_qa-vlm-zero-shot-generated-responses.csv", index=False)': '.to_excel("../responses/cloud/vlm_response_cloud_llava1_5_vl_7b_zero_shot.xlsx", index=False)',
        '.to_csv("cloud_logs_qa-vlm-cot-generated-responses.csv", index=False)': '.to_excel("../responses/cloud/vlm_response_cloud_llava1_5_vl_7b_cot.xlsx", index=False)',
        '.to_csv("device_logs_qa-vlm-zero-shot-generated-responses.csv", index=False)': '.to_excel("../responses/device/vlm_response_device_llava1_5_vl_7b_zero_shot.xlsx", index=False)',
        '.to_csv("device_logs_qa-vlm-cot-generated-responses.csv", index=False)': '.to_excel("../responses/device/vlm_response_device_llava1_5_vl_7b_cot.xlsx", index=False)',
    },
    "vlm_code_qwen2_5_vl_7b.ipynb": {
        '.to_csv("cloud_logs_qa-vlm-zero-shot-generated-responses.csv", index=False)': '.to_excel("../responses/cloud/vlm_response_cloud_qwen_7b_zero_shot.xlsx", index=False)',
        '.to_csv("cloud_logs_qa-vlm-cot-generated-responses.csv", index=False)': '.to_excel("../responses/cloud/vlm_response_cloud_qwen_7b.xlsx", index=False)',
        '.to_csv("device_logs_qa-vlm-zero-shot-generated-responses.csv", index=False)': '.to_excel("../responses/device/vlm_response_device_qwen_7b_zero_shot.xlsx", index=False)',
        '.to_csv("device_logs_qa-vlm-cot-generated-responses.csv", index=False)': '.to_excel("../responses/device/vlm_response_device_qwen_7b.xlsx", index=False)',
    },
}


def update_notebook(filepath, specific_replacements):
    """Update a single notebook with global + specific replacements."""
    filename = os.path.basename(filepath)
    print(f"\nProcessing: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Build combined replacements
    all_replacements = dict(GLOBAL_REPLACEMENTS)
    all_replacements.update(specific_replacements)
    
    total_changes = 0
    
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        
        source_text = ''.join(cell.get('source', []))
        new_source = source_text
        
        for old, new in all_replacements.items():
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
    
    # LLM_Text
    print("=" * 60)
    print("LLM_Text Notebooks")
    print("=" * 60)
    for nb_name, replacements in LLM_TEXT_OUTPUT_REPLACEMENTS.items():
        path = os.path.join(BASE_DIR, "LLM_Text", "code", nb_name)
        if os.path.exists(path):
            total += update_notebook(path, replacements)
        else:
            print(f"  ❌ Not found: {nb_name}")
    
    # LLM_OCR
    print("\n" + "=" * 60)
    print("LLM_OCR Notebooks")
    print("=" * 60)
    for nb_name, replacements in LLM_OCR_OUTPUT_REPLACEMENTS.items():
        path = os.path.join(BASE_DIR, "LLM_OCR", "code", nb_name)
        if os.path.exists(path):
            total += update_notebook(path, replacements)
        else:
            print(f"  ❌ Not found: {nb_name}")
    
    # VLM
    print("\n" + "=" * 60)
    print("VLM Notebooks")
    print("=" * 60)
    for nb_name, replacements in VLM_OUTPUT_REPLACEMENTS.items():
        path = os.path.join(BASE_DIR, "VLM", "code", nb_name)
        if os.path.exists(path):
            total += update_notebook(path, replacements)
        else:
            print(f"  ❌ Not found: {nb_name}")
    
    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total} replacements across all notebooks")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
