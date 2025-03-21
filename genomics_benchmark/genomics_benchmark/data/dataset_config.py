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
                "enhancer_loc": ["chr", "start", "end"],  # Basic enhancer location
                "gene_info": ["gene_name", "gene_tss"],  # Basic gene information
                "label": "Significant"  # Binary label for positive/negative pairs
            },
            "distance_threshold": 100000000,  # Enhancer-gene distance threshold in bp
            "output_columns": [
                "chr", "start", "end",  # Enhancer location
                "gene_name", "gene_tss",  # Gene information
                "distance",  # Calculated distance
                "ABC Score",  # Effect size (if available)
                "labels"  # Calculated label
            ]
        },
        # Dataset-specific configuration
        "ABC_fulco": {
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
            },
            "additional_columns": []  # No additional columns needed
        },
        "Merged": {
            "name": "E2G Enhancer Dataset",
            "description": "E2G K562 enhancer dataset",
            "genome_version": "hg38",
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/enhancer/E2G/E2g.tsv",
            "file_format": "tsv",
            "column_mapping": {
                # Mapping from source column names to standard column names
                "chr": "chrom",
                "start": "chromStart",
                "end": "chromEnd",
                "gene_name": "measuredGeneSymbol",
                "gene_tss": "startTSS",
                "ABC Score": "ABCScoreDNaseOnlyAvgHicTrack2",
                "Significant": "Significant",
                "hic_contact": "3DContactAvgHicTrack2",
                "hic_contact_squared": "3DContactAvgHicTrack2_squared",
                "activity_enh": "activityEnhDNaseOnlyAvgHicTrack2_squared",
                "activity_prom": "activityPromDNaseOnlyAvgHicTrack2",
            },
            "additional_columns": [
                "EffectSize",  
            ]
        }
        # More datasets can be added...
    }
} 