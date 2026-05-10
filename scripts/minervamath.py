import argparse
from datasets import Dataset, load_dataset
from tqdm.auto import tqdm


def last_boxed_only_string(text: str):
    idx = text.rfind("\\boxed")
    if "\\boxed " in text:
        return "\\boxed " + text.split("\\boxed ")[-1].split("$")[0]
    if idx < 0:
        idx = text.rfind("\\fbox")
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(text):
        if text[i] == "{":
            num_left_braces_open += 1
        if text[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    return None if right_brace_idx is None else text[idx : right_brace_idx + 1]


def extract_ground_truth(solution: str):
    boxed = last_boxed_only_string(solution)
    if boxed:
        return boxed

    if "####" in solution:
        return solution.split("####")[-1].strip()

    lines = [line.strip() for line in solution.strip().splitlines() if line.strip()]
    return lines[-1] if lines else None


def main():
    parser = argparse.ArgumentParser(description="Convert MinervaMath to parquet format used in this repo.")
    parser.add_argument("--split", type=str, default="test", help="HF split to load (default: test)")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output parquet path (default: data/minervamath_<split>.parquet)",
    )
    args = parser.parse_args()

    output_path = args.output or f"data/minervamath_{args.split}.parquet"

    dataset = load_dataset("math-ai/minervamath", split=args.split)
    print(f"Loaded split '{args.split}' with {len(dataset)} examples")

    rows = []
    for idx, datum in tqdm(enumerate(dataset), total=len(dataset)):
        problem = datum.get("problem", "")
        solution = datum.get("solution", "")
        ground_truth = extract_ground_truth(solution)

        if not ground_truth:
            continue

        rows.append(
            {
                "id": idx,
                "images": None,
                "question": problem,
                "ground_truth": ground_truth,
                "problem": problem,
                "answer": solution,
                "data_source": f"minervamath_{args.split}",
            }
        )

    ds = Dataset.from_list(rows)
    ds.to_parquet(output_path)
    print(f"Saved {len(ds)} rows to {output_path}")


if __name__ == "__main__":
    main()