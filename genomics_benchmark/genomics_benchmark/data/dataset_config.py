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
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/enhancer/ABC_Fulco.xlsx",
            "file_format": "xlsx",
            "label_column": "Significant",  # ABC_fulco数据集的标签列名
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
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/enhancer/Merged.tsv",
            "file_format": "tsv",
            "label_column": "Regulated",  # Merged数据集的标签列名
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
        },
        "Fulco": {
            "name": "Fulco K562 Enhancer Dataset",
            "description": "Fulco K562 enhancer dataset in TSV format",
            "genome_version": "hg38",
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/enhancer/Fulco.tsv",
            "file_format": "tsv",
            "label_column": "Regulated",
            "column_mapping": {
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
        },
        "Gasperini": {
            "name": "Gasperini K562 Enhancer Dataset",
            "description": "Gasperini K562 enhancer dataset",
            "genome_version": "hg38",
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/enhancer/Gasperini.tsv",
            "file_format": "tsv",
            "label_column": "Regulated",
            "column_mapping": {
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
        },
        "Schraivogel": {
            "name": "Schraivogel K562 Enhancer Dataset",
            "description": "Schraivogel K562 enhancer dataset",
            "genome_version": "hg38",
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/enhancer/Schraivogel.tsv",
            "file_format": "tsv",
            "label_column": "Regulated",
            "column_mapping": {
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
    },
    
    "eqtl": {
        # Task-level common configuration
        "task_config": {
            "required_columns": {
                "gene_info": ["phenotype_id", "gene_name", "biotype"],  # 基因信息
                "variant_info": ["variant_id", "pip", "af"],  # 变异信息
                "effect_info": ["afc", "afc_se"]  # 效应信息
            },
            "output_columns": [
                "phenotype_id", "gene_name", "biotype",  # 基因信息
                "variant_id", "pip", "af",  # 变异信息
                "afc", "afc_se",  # 效应信息
                "labels"  # 标签（如果启用）
            ]
        },
        # Dataset-specific configuration
        "Adipose_Subcutaneous": {
            "name": "Adipose Subcutaneous eQTL Dataset",
            "description": "eQTL data from GTEx v10 for Adipose Subcutaneous tissue",
            "genome_version": "hg38",
            "data_url": "https://raw.githubusercontent.com/yueyueliu/Benchmark_Genomics/main/data/demo_online/eqtl/Adipose_Subcutaneous.v10.eQTLs.SuSiE_summary.parquet",
            "file_format": "parquet",
            "column_mapping": {
                "phenotype_id": "phenotype_id",
                "gene_name": "gene_name",
                "biotype": "biotype",
                "variant_id": "variant_id",
                "pip": "pip",
                "af": "af",
                "cs_id": "cs_id",
                "cs_size": "cs_size",
                "afc": "afc",
                "afc_se": "afc_se"
            },
            "additional_columns": []
        }
    }
} 