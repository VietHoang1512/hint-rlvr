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

dataset = []
for subset in ['algebra', 'counting_and_probability', 'geometry', 'intermediate_algebra', 'number_theory', 'prealgebra', 'precalculus']:
    dataset += list(load_dataset("EleutherAI/hendrycks_math", subset, split="test"))
rows = []

for idx, datum in tqdm(enumerate(dataset),total=len(dataset)):
    # print(datum["correct"])
    
    # print("_"*20)
    # print("datum", datum)
    # if datum["correct"]:
    
    answer = datum["solution"]
    ground_truth = last_boxed_only_string(answer)
    # print(datum["conversations"][1])
    if ground_truth:
        rows.append({
            "id": idx,
            "images": None,  # PIL image or path
            "question" : datum["problem"],
            "ground_truth": ground_truth,
            "problem": datum["problem"],
            "answer": answer,
            "data_source": "hendrycks_math_test"
        })
        print(rows[-1])
    else:
        print("ground_truth", ground_truth)

ds = Dataset.from_list(rows)
ds.to_parquet("data/hendrycks_math_test.parquet")