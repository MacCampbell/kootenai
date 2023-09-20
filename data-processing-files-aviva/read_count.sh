#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name="read_count"
#SBATCH --nodes=1  
#SBATCH --ntasks=1
#SBATCH --mem=12G 
#SBATCH --time=14-1:00:00 
#SBATCH --output=read_count.out # File to which STDOUT will be written
#SBATCH --error=read_count.err # File to which STDERR will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=afiske@ucdavis.edu

echo "Starting Job: "
date

wc -l *fastq


echo "Ending Job: "
date
