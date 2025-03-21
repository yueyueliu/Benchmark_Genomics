"""
Test script for EnhancerProcessor
"""
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from genomics_benchmark.data import EnhancerProcessor

def main():
    # Set cache root and output path
    dataset_name = "Gasperini" # "Fulco" # "Schraivogel" #"ABC_fulco" # "Merged"
    cache_root = "/storage/zhangkaiLab/liuyue87/Projects/Benchmark_Genomics/data/cache"
    output_path = "/storage/zhangkaiLab/liuyue87/Projects/Benchmark_Genomics/data/demo_data/enhancer/" + dataset_name + "/processed_data.tsv"
    
    # Create processor instance
    processor = EnhancerProcessor(
        dataset_name=dataset_name,
        cache_root=cache_root
    )
    
    # Run pipeline
    results = processor.initialize_pipeline(
        output_path=output_path,
        distance_threshold=None,
        clear_cache=False,
        do_statistics=True,
        download_genome=True,
        genome_file_type="both",
        add_strand=True
    )
    
    print("Test completed successfully!")

if __name__ == "__main__":
    main()