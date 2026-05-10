#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:a100:1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=80GB
#SBATCH --job-name=eval
#SBATCH --output=logs/%j.out
#SBATCH --error=logs/%j.err
#SBATCH --account torch_pr_559_cds
module purge
module load anaconda3/2025.06
eval "$(conda shell.bash hook)"
conda activate /scratch/hvp2011/envs/rgpo/
cd /scratch/hvp2011/implement/rgpo/
conda env list


python scripts/test_qwen2vl_geoqa.py
# python scripts/helix_train.py