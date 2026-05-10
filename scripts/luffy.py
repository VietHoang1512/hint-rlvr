import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
from datasets import Dataset, load_dataset
from tqdm.auto import tqdm
from collections import Counter
rows = []
parquet_path = Path()
for parquet_path in [
                    # "data/openr1.parquet", 
                    #  "data/valid.parquet", 
                    "data/valid.all.parquet",
                    # "data/valid.mmlu_pro.parquet",
                    # "data/valid.gpqa.parquet",
                    # "data/valid.arc_c.parquet",
                     ]:
    parquet_path = Path(parquet_path)
    # 1) Fast parquet metadata (no full load needed)
    pf = pq.ParquetFile(parquet_path)
    meta = pf.metadata
    # 2) Load with pandas for dtype + examples
    df = pd.read_parquet(parquet_path)
    print(f"Loaded {len(df)} rows from {parquet_path}")
    for idx, row in tqdm(df.iterrows()):
        # print(f"\nRow {idx}:")
        # for col in df.columns:
        #     print(f"  {col}: {row[col]}")
        # print(row)
        # print("prompt", row["prompt"])
        # print("target", row["target"])
        # print(row["data_source"])
        question = "\n".join([msg["content"] for msg in row["prompt"]])
        question = row["prompt"][-1]["content"] 
        datum = {
            "id": len(rows),
            "ground_truth": row["reward_model"]["ground_truth"],
            'data_source': row["data_source"],
            "question": (question + "Provide the correct option letter, e.g., A, B, C, D, E, as your final answer.") if row["data_source"] in ["mmlu_pro", "gpqa", "arc_c"] else question,
            "abstract_hint": "This is a place holder",
            "medium_hint": "This is a place holder",
            "direct_hint": "This is a place holder",
            "answer": row.get("target", "This is a place holder"),
            "system_prompt": row["prompt"][0]["content"] ,
        }
        rows.append(datum)
        # break
    print("_"*50)
    print("prompt", row["prompt"])
    print("target", row.get("target", "This is a place holder"))
    print(row["data_source"])    
    print(rows[-1])

print(Counter([row["data_source"] for row in rows]))
print(Counter([row["system_prompt"] for row in rows]))
# print(Counter([row["ground_truth"] for row in rows]))
# dataset = load_dataset("math-ai/minervamath", split="test")
# for idx, datum in tqdm(enumerate(dataset), total=len(dataset)):
#     question = datum["question"]
#     ground_truth = datum["answer"]

#     if not ground_truth:
#         continue

#     rows.append(
#         {
#             "id": len(rows),
#             "question": question,
#             "ground_truth": ground_truth,
#             "data_source": "minervamath",
#             "abstract_hint": "This is a place holder",
#             "medium_hint": "This is a place holder",
#             "direct_hint": "This is a place holder",
#         }
#     )    
ds = Dataset.from_list(rows)
ds.to_parquet("data/valid-math-luffy-processed.parquet")
ds.to_parquet("/scratch/mp5847/src/rgpo/data/valid-math-luffy-processed.parquet")

print(len(ds))

