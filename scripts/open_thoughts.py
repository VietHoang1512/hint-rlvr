from tqdm.auto import tqdm
from datasets import load_dataset, Dataset

def last_boxed_only_string(string):
    idx = string.rfind("\\boxed")
    if "\\boxed " in string:
        return "\\boxed " + string.split("\\boxed ")[-1].split("$")[0]
    if idx < 0:
        idx = string.rfind("\\fbox")
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == "{":
            num_left_braces_open += 1
        if string[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    retval = None if right_brace_idx is None else string[idx : right_brace_idx + 1]

    return retval

dataset = load_dataset("bethgelab/CuratedThoughts", 'OpenThoughts-114k-math-default', split="train")
print(dataset)
rows = []
N_TOKENS=8192
for idx, datum in tqdm(enumerate(dataset),total=len(dataset)):
    # print(datum["correct"])
    
    # if datum["correct"]:
    if datum["generated_token_count"] <= N_TOKENS:



        # print("_"*20)
        # print("datum", datum)
        answer = datum["solution"]
        ground_truth = last_boxed_only_string(answer)
        # print(datum["conversations"][1])
        if ground_truth:
            rows.append({
                "id": idx,
                "images": None,  # PIL image or path
                "question" : datum["problem"],
                "source": datum["source"],
                "ground_truth": ground_truth,
                "problem": datum["problem"],
                "answer": answer,
                "generated_answer": datum["conversations"][1]['value'],
                "data_source": "open_thoughts_114k_math"
            })
            # print(rows[-1])
        else:
            print("ground_truth", ground_truth)

ds = Dataset.from_list(rows)
print("Total", len(ds))
ds.to_parquet(f"data/open_thoughts_114k_math_{N_TOKENS}.parquet")