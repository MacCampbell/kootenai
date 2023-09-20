#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name=“Add_index” 
#SBATCH --nodes=1  
#SBATCH --ntasks=1
#SBATCH --mem=12G 
#SBATCH --time=14-1:00:00 
#SBATCH --output=Add_index.out # File to which STDOUT will be written
#SBATCH --error=Add_index.err # File to which STDERR will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=afiske@ucdavis.edu

echo "Starting Job: "
date

../Data/AFST01/AFST01_S42_L002_R1_001.fastq.gz gunzip 

echo "Ending Job: "
date
