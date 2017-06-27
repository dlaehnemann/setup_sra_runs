# Download and extract SRA data

Use the scripts `prefetch-sra.bash` and `fastq-dump-sra.bash` to download and extract data from the sequence read archive. They require a list of accession numbers for sequencing runs, usually in the form of an `SRR_Acc_List.txt`.

# Extract info on runs from `SraRunTable.txt`

Adapt and use the script `SraRunTable2config.py` to extract relevant info from a `SraRunTable.txt` and parse it into YAML format as a starting point for a Snakemake config.yaml.

# TODOs

* turn as much of this as possible into a Snakemake pipeline, to improve reproducibility, parallelisation and documentation 
