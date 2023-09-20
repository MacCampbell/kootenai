#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name="Add_index"
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

../../scripts/add_indexSeqs.pl AFST01_S42_L002_R1_001.fastq AFST01_S42_L002_R2_001.fastq AFST01_S42_L002_R3_001.fastq 


echo "Ending Job: "
date
