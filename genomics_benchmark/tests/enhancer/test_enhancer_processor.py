"""
Test enhancer data processing functionality
"""
import sys
import os
from pathlib import Path
import pandas as pd

# Add project root directory to Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from genomics_benchmark.data.enhancer_processor import EnhancerProcessor
from genomics_benchmark.data.reference_genome import download_reference_genome

if __name__ == "__main__":
    # Set paths
    cache_root = Path("/storage/zhangkaiLab/liuyue87/Projects/Benchmark_Genomics/data/cache")
    output_path = Path("/storage/zhangkaiLab/liuyue87/Projects/Benchmark_Genomics/data/demo_data/enhancer/Fulco/197k_data.tsv")
    
    # Create processor instance
    processor = EnhancerProcessor(
        dataset_name="fulco",
        cache_root=cache_root
    )
    
    # Download data and reference genome files
    results = processor.initialize_pipeline(
        output_path=output_path,
        distance_threshold=2000000,  # Optional distance threshold
        clear_cache=False,  # Clear cache after processing
        do_statistics=True,  # Perform statistical analysis

        download_genome=True,  # Download reference genome
        genome_file_type="both",  # Download both FASTA and GTF files

        # download_genome=False,
        add_strand=True,  # Add strand information
        )
    
    # Print test status
    if results['status'] == 'success':
        print("\nInitialization complete!")