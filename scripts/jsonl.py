import pandas as pd
import json
data = pd.read_parquet("data/valid.all.parquet")
for index, row in data.iterrows():
    # problem = row["prompt"][-1]["content"].replace("Answer the following multiple choice question. The last line of your response should be of the following format: 'ANSWER: $LETTER' (without quotes) where LETTER is one of ABCD. Think step by step before answering.\n\n", "")
    # problem = row["prompt"][-1]["content"].replace("The following are multiple choice questions (with answers) about {$}. Think step by step and then finish your answer with \"\\boxed{X}\" where X is the correct letter choice.Question:\n", "")
    problem = row["prompt"][-1]["content"]
    answer = row['reward_model']['ground_truth']
    data_source = row['data_source']
    with open(f"data/{data_source}.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"problem": problem, "answer": str(answer)}, ensure_ascii=False) + "\n")