#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --constraint="a100|h200"
#SBATCH --time=24:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=100GB
#SBATCH --job-name=eval
#SBATCH --output=logs/%j.out
#SBATCH --error=logs/%j.err
##SBATCH --account=torch_pr_40_tandon_advanced
#SBATCH --account=torch_pr_559_cds
set -e
module purge
module load anaconda3/2025.06
eval "$(conda shell.bash hook)"
cd /scratch/hvp2011/implement/rgpo/
conda activate /scratch/hvp2011/envs/rgpo/  
conda env list
# python scripts/dp_infer.py --model_path /scratch/hvp2011/implement/rgpo/checkpoints/rgpo-hint-3/hint-Qwen2.5-3B-prompt--adv_estimator-grpo-refine_coef-1.-refine-False-hint-False/global_step_321/actor/huggingface --tasks math500 aime24 aime25 amc minerva olympiad gpqa_d arc_c mmlu_pro --output result-0.jsonl
task=${1:-aime24}
set -x
  # --val_top_k -1 \
  # --val_top_p 1.0 \
  # --val_n 1 \
python scripts/dp_infer.py \
  --model_path /scratch/hvp2011/implement/rgpo/checkpoints/rgpo-hint-3/hint-Qwen2.5-3B-prompt--adv_estimator-grpo-refine_coef-1.-refine-False-hint-False/global_step_321/actor/huggingface \
  --tasks $task \
  --val_temperature 0.6 \
  --val_do_sample \
  --use_chat_template \
  --output result-verl-$task.jsonl
done