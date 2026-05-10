import os, re
from datetime import datetime
from typing import Any, Dict, List

# Removed extract_boxed_content since we are now targeting <answer> tags
from mathruler.grader import grade_answer


def extract_answer_content(response: str) -> str:
    """Extracts the content enclosed in <answer> tags."""
    match = re.search(r"<answer>(.*?)</answer>", response, re.DOTALL)
    # Return the content if found, otherwise return an empty string
    return match.group(1).strip() if match else ""


def format_reward(response: str) -> float:
    """Checks if the response contains the <answer> tags."""
    # Matches any thinking trace followed by <answer>...</answer>
    pattern = re.compile(r".*<answer>.*</answer>\s*", re.DOTALL)
    format_match = re.fullmatch(pattern, response)
    return 1.0 if format_match else 0.0


def accuracy_reward(response: str, ground_truth: str) -> float:
    """Grades the extracted answer against the ground truth."""
    answer = extract_answer_content(response)
    return 1.0 if grade_answer(answer, ground_truth) else 0.0


def compute_score(solution_str: str, ground_truth: str, timeout_score: float = 0, prompt_str=None, data_source="unknown", format_weight: float = 0.1, **kwargs) -> Dict[str, Any]:
    # Clean up accidental spacing around tags
    response = re.sub(r"\s*(<|>|/)\s*", r"\1", solution_str)  
    
    format_score = format_reward(response)
    accuracy_score = accuracy_reward(response, ground_truth)
    score = (1 - format_weight) * accuracy_score + format_weight * format_score
    
    solution_extracted = extract_answer_content(response)
    
    if os.getenv("DEBUG_MODE") == "true":
        log_path = os.getenv("LOG_PATH")
        if log_path:
            current_time = datetime.now().strftime("%d-%H-%M-%S-%f")
            with open(log_path, "a", encoding='utf-8') as f:
                f.write(f"------------- {current_time} Accuracy reward: {score} -------------\n")
                f.write(f"Prompt: {prompt_str}\n")
                f.write(f"Response: {solution_str}\n")
                f.write(f"Solution: {solution_extracted}\n")
                f.write(f"Ground truth: {ground_truth}\n")
                f.write(f"Format score: {format_score}\n")
                f.write(f"Accuracy score: {accuracy_score}\n")
                f.write(f"Overall score: {score}\n")
            
    return {
        "score": score,
        "feedback": f"Format score: {format_score}/1.0\nAccuracy score: {accuracy_score}/1.0\nOverall score: {score}/1.0",
    }

if __name__ == "__main__":
    # Updated test cases to reflect the <answer> tag requirement
    print(compute_score("Thinking process here... <answer>D</answer>", "D"))
    print(compute_score("Let's calculate step by step... <answer>4 \pi</answer>", "$4 \pi$"))
    print(compute_score("Thinking process here... <answer>d</answer>", "D"))
    
    # These should yield lower scores due to missing/incorrect formats
    print(compute_score("4*\pi", "$4 \pi$")) 
    print(compute_score("<answer>4\pi", "$4 \pi$")) # Missing closing tag