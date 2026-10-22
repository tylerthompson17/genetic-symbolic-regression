#!/bin/bash
#SBATCH --job-name=gp
#SBATCH --partition=batch-cpu
#SBATCH --qos=project-cpu
#SBATCH --account=projects
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=02:00:00
#SBATCH --array=1-200
#SBATCH --output=logs/gp-%A_%a.out
export OMP_NUM_THREADS=1
FILE=${1:-run_dataset3.py}
python3 - <<PYEOF
import random
random.seed($SLURM_ARRAY_TASK_ID)
print("file $FILE, seed $SLURM_ARRAY_TASK_ID")
exec(open("$FILE").read().replace("range(10)", "range(1)"))  # one run instead of the file's 10
PYEOF
