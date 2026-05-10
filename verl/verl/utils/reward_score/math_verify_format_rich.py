# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, re
from datetime import datetime

from math_verify import parse, verify

def format_reward(response: str) -> float:
    pattern = re.compile(r"<think>.*</think>.*\\boxed\{.*\}.*", re.DOTALL)
    format_match = re.fullmatch(pattern, response)
    return 1.0 if format_match else 0.0


def accuracy_reward(response: str, ground_truth: str) -> float:
    pattern = r'\\boxed{([^{}]*(?:\{[^{}]*\}[^{}]*)*)}'
    boxed_content_ans = re.findall(pattern, response)

    if not boxed_content_ans:
        return None, 0
    final_ans_expr = "\\boxed{" + boxed_content_ans[-1] + "}"
    final_gt_expr = "\\boxed{" + ground_truth + "}"

    if final_ans_expr == final_gt_expr:
        return boxed_content_ans[-1], 1.0
    try:
        parsed_ans = parse(final_ans_expr)
        parsed_gt = parse(final_gt_expr)
        is_correct = verify(parsed_ans, parsed_gt)
        return parsed_ans, 1.0 if is_correct else 0
    except Exception as e:
        return None, 0



def compute_score(solution_str: str, ground_truth: str, timeout_score: float = 0, prompt_str=None, data_source="unknown", format_weight: float = 0.1, **kwargs) -> bool:

    # response = re.sub(r"\s*(<|>|/)\s*", r"\1", solution_str)  # handle qwen2.5vl-32b format
    response = solution_str
    solution_extracted, accuracy_score = accuracy_reward(response, ground_truth)
    format_score = format_reward(response)
    score = (1 - format_weight) * accuracy_score + format_weight * format_score
    if os.getenv("DEBUG_MODE") == "true":
        log_path = os.getenv("LOG_PATH")
        current_time = datetime.now().strftime("%d-%H-%M-%S-%f")
        with open(log_path, "a", encoding='utf-8') as f:
            f.write(f"------------- {current_time} -------------\n")
            f.write(f"Prompt: {prompt_str}\n")
            f.write(f"Response: {solution_str}\n")
            f.write(f"Solution: {solution_extracted}\n")
            f.write(f"Ground truth: {ground_truth}\n")
            f.write(f"Format score: {format_score}\n")
            f.write(f"Accuracy score: {accuracy_score}\n")
            f.write(f"Overall score: {score}\n")

    return {
        "score": score,
        "overall_score": score,
        "format_score": format_score,
        "accuracy_score": accuracy_score,
        "feedback": f"Format score: {format_score:.1f}/1.0\nAccuracy score: {accuracy_score:.1f}/1.0\nOverall score: {score}/1.0\nYou should maximize the overall score by improving both the format and accuracy of your answer.",
    }
if __name__ == "__main__":
    print(compute_score("D", "D"))
    
    print(compute_score("4 \pi", "$4 \pi$"))
    print(compute_score("4*\pi", "$4 \pi$"))
    print(compute_score("4\pi", "$4 \pi$"))