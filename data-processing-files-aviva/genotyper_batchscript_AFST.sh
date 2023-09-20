#!/bin/bash
#SBATCH --partition=production
#SBATCH --job-name=genotyping
#SBATCH --nodes=1  
#SBATCH --ntasks=1
#SBATCH --mem=15G 
#SBATCH --time=12:00:00 
#SBATCH --output=genotyping.out # File to which STDOUT will be written
#SBATCH --error=genotyping.err # File to which STDERR will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=afiske@ucdavis.edu

echo "Starting Job: "
date

module load perl-libs

../../scripts/genotyper_AFST.sh

echo "Ending Job: "
date

