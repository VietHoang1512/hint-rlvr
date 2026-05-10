import re
from huggingface_hub import create_repo

from datasets import load_dataset, Dataset, DatasetDict
dataset = load_dataset("lmms-lab/multimodal-open-r1-8k-verified")["train"]

rows = []
for idx, datum in enumerate(dataset):
    print("_"*20)
    # print("datum", datum)
    answer = datum["original_answer"].strip()
    final_answers = re.findall(r'Answer:\s*([A-Z])', answer)
    print("answer", answer)
    print("final answer", final_answers)
    if len(final_answers)==0:
         
        final_answers = re.findall(r'The answer is\s*(.)+', answer)
        print("final answer", final_answers)
        if len(final_answers)==0:
            datum["image"].save(f"{idx}.png")
            print(idx, "solution", datum["solution"])
            continue
    ground_truth = final_answers[-1]
    rows.append({
        "id": idx,
        "images": [datum["image"]],  # PIL image or path
        "question" : "<image>" + datum["problem"],
        "ground_truth": ground_truth,
        "problem": "<image>" + datum["original_question"],
        "answer": "This is a dummy answer",
        "data_source": "multimodal-open-r1-8k-verified"
    })
    # print(rows[-1])

ds = Dataset.from_list(rows)
ds.to_parquet("data/multimodal-open-r1-8k-verified.parquet")