cd /scratch/hvp2011/implement/rgpo/
for task in aime24 #math500  minerva olympiad gpqa_d arc_c mmlu_pro 
do
sbatch  /scratch/hvp2011/implement/rgpo/scripts/eval.sh $task
done