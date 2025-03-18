"""
Dataset configuration file containing metadata for each dataset
"""

DATASET_CONFIG = {
    # Reference genome configuration
    "reference_genome": {
        "hg19": {
            "fasta_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/GRCh37.p13.genome.fa.gz",
            "gtf_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz"
        },
        "hg38": {
            "fasta_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/GRCh38.p14.genome.fa.gz",
            "gtf_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/gencode.v47.annotation.gtf.gz"
        },
        "mm10": {
            "fasta_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M36/GRCm39.genome.fa.gz",
            "gtf_url": "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M36/gencode.vM36.annotation.gtf.gz"
        }
    },
    
    "enhancer": {
        # Task-level common configuration
        "task_config": {
            "required_columns": {
                "enhancer_loc": ["chr", "start", "end"],  # Enhancer location
                "gene_info": ["gene_name", "gene_tss"],  # Gene information
                "effect": ["Normalized HiC Contacts", "H3K27ac (RPM)", "Activity"],  # Effect size
                "ABC Score": ["ABC Score"],
                "label": "Significant"  # Calculated label
            },
            "distance_threshold": 1000000,  # Enhancer-gene distance threshold in bp
            "output_columns": [
                "chr", "start", "end",  # Enhancer location
                # "strand",
                "gene_name", "gene_tss",  # Gene information
                "distance",  # Calculated distance
                "ABC Score",  # Effect size
                "labels"  # Calculated label
            ]
        },
        # Dataset-specific configuration
        "fulco": {
            "name": "Fulco Enhancer Dataset",
            "description": "Fulco K562 enhancer dataset",
            "genome_version": "hg19",  # Add genome version information
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/enhancer/Fulco/41588_2019_538_MOESM3_ESM.xlsx",
            "file_format": "xlsx",
            "column_mapping": {
                # Mapping from source column names to standard column names
                "chr": "chr",
                "start": "start",
                "end": "end",
                "gene_name": "Gene",
                "gene_tss": "Gene TSS",
                "Normalized HiC Contacts": "Normalized HiC Contacts",
                "H3K27ac (RPM)": "H3K27ac (RPM)",
                "Activity": "Activity",
                "ABC Score": "ABC Score",
                "Significant": "Significant"
            }
        }
        # More datasets can be added...
    }
} 