#!/usr/bin/env bash

## extract already prefetched sequencing data for a full study
## from the sequence read archive (SRA) using the sra toolkit's
## `fastq-dump`
##
## TODO: Make this a Snakemake rule in an SRA Snakemake pipeline,
## in order to parallelize and improve reproducability.


## ensure the cluster job inherits the environment it is submitted from
#$ -V

## set cluster job to run in the directory it is submitted from
#$ -cwd

## request multiple cores for the cluster job 
#$ -pe multislot 20

## base name for the cluster job
#$ -N fastq_dump_SRA_files

## set directory for stderr and stdout of cluster job
#$ -o ./
#$ -e ./

## submit the job to a specific queue
#$ -q all.q

# the file SRR_Acc_List.txt can be obtained for at the sequence
# read archive by entering a study number (e.g. SRP044380) at:
# https://www.ncbi.nlm.nih.gov/Traces/study/
# And then clicking on "Accesion List" in the "Download" field
# of the study.
ACCS=( `cat SRR_Acc_List.txt` )

for a in ${ACCS[@]}
do
    fastq-dump --origfmt --gzip -split-3 $a
    mkdir $a
    mv ${a}_1.fastq.gz ${a}/${a}.1.fastq.gz
    mv ${a}_2.fastq.gz ${a}/${a}.2.fastq.gz
done
