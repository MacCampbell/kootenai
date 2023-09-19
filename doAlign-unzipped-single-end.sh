#!/bin/bash -l

#Requires a tab delimited list of paired end files with desired name (list, $1)
#SRR1613242_1 SRR1613242

#Requires a path to indexed reference genome (ref, $2)

#bash ../../doAlign-unzipped-single-end.sh to-align.txt /home/maccamp/kootenai/data/new-ref/new-ref.fasta

list=$1
ref=$2

wc=$(wc -l ${list} | awk '{print $1}')

x=1
while [ $x -le $wc ] 
do
        string="sed -n ${x}p ${list}" 
        str=$($string)

        var=$(echo $str | awk -F"\t" '{print $1, $2}')   
        set -- $var
        c1=$1
        c2=$2
        

       echo "#!/bin/bash -l
       module load bwa/0.7.17
       bwa mem $ref ${c1}.fastq | samtools view -Sb | samtools sort - -o ${c2}.sort.bam
       samtools index ${c2}.sort.bam
       reads=\$(samtools view -c ${c2}.sort.bam)
       depth=\$(samtools depth -a ${c2}.sort.bam | awk '{sum+="\$3"} END {print sum/NR}' )
       echo \"${c2},\${reads},\${depth}\"  > ${c2}.stats" > ${c2}.sh
       sbatch -p med -t 1-10:00:00 --mem=8G ${c2}.sh

       x=$(( $x + 1 ))

done


