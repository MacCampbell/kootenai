#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name=genotyping
#SBATCH --nodes=1  
#SBATCH --ntasks=1
#SBATCH --mem=15G 
#SBATCH --time=15:00:00 
#SBATCH --output=geno_compile.out # File to which STDOUT will be written
#SBATCH --error=geno_compile.err # File to which STDERR will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=afiske@ucdavis.edu

echo "Starting Job: "
date

../../scripts/GTseq_GenoCompile_v3_Tetra.py

echo "Ending Job: "
date

