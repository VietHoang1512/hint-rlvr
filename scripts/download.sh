module purge
module load anaconda3/2025.06
eval "$(conda shell.bash hook)"
cd /scratch/hvp2011/implement/rgpo/
conda activate /scratch/hvp2011/envs/rgpo/  
conda env list

mkdir -p data


# MATH-500
mkdir -p data/MATH-500
wget -O data/MATH-500/test.jsonl \
  https://huggingface.co/datasets/HuggingFaceH4/MATH-500/resolve/main/test.jsonl

# AIME 2024 / 2025, AMC, Minerva, OlympiadBench
python - <<'PY'
from datasets import load_dataset
import os, json

def save_jsonl(dataset_name, split, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ds = load_dataset(dataset_name, split=split)
    with open(out_path, "w", encoding="utf-8") as f:
        for x in ds:
            problem = x.get("problem") or x.get("question")
            answer = x.get("answer") or x.get("final_answer")
            if problem is None or answer is None:
                print("Error")
            f.write(json.dumps({"problem": problem, "answer": str(answer)}, ensure_ascii=False) + "\n")

save_jsonl("HuggingFaceH4/aime_2024", "train", "data/aime24/aime24.jsonl")
#save_jsonl("yentinglin/aime_2025", "train", "data/aime25/aime25.jsonl")
#save_jsonl("AI-MO/aimo-validation-amc", "train", "data/AMC/amc.jsonl")
save_jsonl("math-ai/minervamath", "test", "data/minerva/minerva.jsonl")
save_jsonl("Hothan/OlympiadBench", "train", "data/olympiad/olympiad.jsonl")
PY

PY