import pandas as pd
from datasets import Dataset
df = pd.read_parquet("data/mint_cot_r1_1024.parquet")


rows = []
for  (_, series_row) in df.iterrows():
    row = series_row.to_dict()
    row["problem"] = (
        row["problem"]
        + "\nThis is the (partial) solution without formatting, you can leverage it to check your answer:\n"
        + row["answer"]
    )
    rows.append(row)
print(row)
ds = Dataset.from_list(rows)
ds.to_parquet("data/mint_cot_r1_1024_full_hint.parquet")
print(len(rows))