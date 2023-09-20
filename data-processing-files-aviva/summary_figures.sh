#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name="summary_figures"
#SBATCH --nodes=1  
#SBATCH --ntasks=1
#SBATCH --mem=10G 
#SBATCH --time=00:30:00 
#SBATCH --output=AFST01_figures.out # File to which STDOUT will be written
#SBATCH --error=AFST01_figures.err # File to which STDERR will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=afiske@ucdavis.edu

echo "Starting Job: "
date

module load anaconda3
python3
import matplotlib ../../scripts/GTseq_SummaryFigures_v3_Tetra.py 'compiled_genos_AFST01.csv'


echo "Ending Job: "
date


