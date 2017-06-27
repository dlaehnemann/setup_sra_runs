#!/usr/bin/env bash

## prefetch sequencing data for a full study from the sequence
## read archive (SRA) using the sra toolkit's `prefetch`
##
## as a default, all the *.sra files will go into:
## ~/ncbi/public/sra/
##
## this default can be changed using sra toolkit's `vdb-config`:
## https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=toolkit_doc&f=vdb-config
##
## TODO: Make this a Snakemake rule in an SRA Snakemake pipeline,
## in order to parallelize and improve reproducability.


## ensure the cluster job inherits the environment it is submitted from
#$ -V

## set cluster job to run in the directory it is submitted from
#$ -cwd

## base name for the cluster job
#$ -N prefetch_SRA_files

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
    prefetch --max-size 150G $a
done
