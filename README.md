# kootenai
GTSeq analyses of Kootenai sturgeon


## Goals

_1_ Interrogate data for new SNPs    
_2_ Adjust GTSeq analysis to genotype new SNPs    

## File Descriptions

Aviva made a really helpful walkthrough document for the GTseq pipeline (GTseqPipeline.Rmd), going from demultiplexed fastqs to final genotypes. I'm attaching that here, as well as a plethora of supporting files. This includes all the scripts with functions described in the walkthrough (the .py and most of the .pl files). I've also included excel files with the i5 and i7 6bp sequences, as well as small perl scripts for converting those sequences to their reverse complements, which is necessary for the demultiplexing csv file. Make sure the csv has unix line endings before using these scripts on it! Speaking of the demultiplexing csv file, I can make one with my plates in this library and send it your way, and you can combine it with a csv covering your plates. A couple more tips for the process, gunziping the R1 fastq takes a long time, so I just sbatch it with a few hours allocated it instead of using srun, and the BarcodeSplit (demultiplexing) similarly takes a long time, so I'd allocate at least 2 hours on srun for this moderately sized library. Let me know once the raw fastqs are ready and I'll get you that demultiplexing csv.      

## Steps    

_1_ Interrogate data for new SNPs     
The current analysis looks for existing SNPs by using a perl regex to match known alleles. Looks to be biallelic. 
`Atr_10304-61,G,A,TGGCTTGGCAGTGG,TGGCTTGACAGTGG,GCCTTTGTTCTCCAGCTTGC,0,0`
`Locus Name,Allele1,Allele2,ProbeSeq1,ProbeSeq2,FWD_Primer,A1_correction,A2_correction`
TGGCTTGGCAGTGG      
TGGCTTGACAGTGG      
`Atr_78173-42,T,C,GGCATTGGAAC[CG]GTC,GGCATCGGAAC[CG]GTC,CTCAGGTCACCCAGCAGAG,0.3,0`    

What is A1_correction/A2_correction? 

Can create a reference then align data and see what variants there are in the data. What was the original reference?   
Can check which loci are invariant, and then look specifically at those to make new variants specific for thse fish.
