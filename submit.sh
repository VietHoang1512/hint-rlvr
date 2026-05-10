#!/bin/bash
set -euo pipefail
run_script="run.sh"
engine="vllm"
# cd ~
# sbatch "$run_script"
for full_hint in False  #False 
do
	for use_refine in True
	do
		for refine_coef in  .001  .0001  # .00001 0.1  # 0.01    #   1.0 
		do	
			for use_sft in False 
			do
				echo "Submitting: refine_coef=${refine_coef}, use_refine=${use_refine}, full_hint=${full_hint}, sft=${use_sft}"
				#bash "$run_script" "$engine" "$refine_coef" "$use_refine" "$full_hint"
				sbatch "$run_script" "$engine" "$refine_coef" "$use_refine" "$full_hint" "$use_sft"
			done
		done
	done
done
