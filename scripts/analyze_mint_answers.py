import json
import statistics
from collections import defaultdict
from tqdm.auto import tqdm

# Load dataset
with open("./data/MINT-CoT_interleave_sft_54k.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} samples")

# Check what keys are available in the first sample
if data:
    print(f"Available keys: {data[0].keys()}")

# Compute answer statistics
def compute_lengths(text):
    text = text.strip()
    return {
        "word_length": len(text.split()),
        "char_length": len(text)
    }

word_lengths = []
char_lengths = []

for datum in tqdm(data, desc="Computing answer lengths"):
    answer = datum['messages'][1]['content']
    lengths = compute_lengths(answer)
    word_lengths.append(lengths['word_length'])
    char_lengths.append(lengths['char_length'])

# Compute statistics
stats = {
    "mean_words": statistics.mean(word_lengths),
    "median_words": statistics.median(word_lengths),
    "max_words": max(word_lengths),
    "min_words": min(word_lengths),
    "stdev_words": statistics.stdev(word_lengths) if len(word_lengths) > 1 else 0,
    "mean_chars": statistics.mean(char_lengths),
    "median_chars": statistics.median(char_lengths),
    "max_chars": max(char_lengths),
    "min_chars": min(char_lengths),
    "stdev_chars": statistics.stdev(char_lengths) if len(char_lengths) > 1 else 0,
    "total_samples": len(word_lengths)
}

print("\n" + "=" * 80)
print("MINT-CoT Answer Statistics")
print("=" * 80)
print(f"Total Samples: {stats['total_samples']}")
print(f"\nWord Count:")
print(f"  Mean:   {stats['mean_words']:.2f}")
print(f"  Median: {stats['median_words']}")
print(f"  Min:    {stats['min_words']}")
print(f"  Max:    {stats['max_words']}")
print(f"  Stdev:  {stats['stdev_words']:.2f}")
print(f"\nCharacter Count:")
print(f"  Mean:   {stats['mean_chars']:.2f}")
print(f"  Median: {stats['median_chars']}")
print(f"  Min:    {stats['min_chars']}")
print(f"  Max:    {stats['max_chars']}")
print(f"  Stdev:  {stats['stdev_chars']:.2f}")
print("=" * 80)
