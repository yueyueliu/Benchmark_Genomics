"""
Reference genome processing module
"""
import os
import gzip
from pathlib import Path
from typing import Dict, Union
from .dataset_config import DATASET_CONFIG
from .download import DataDownloader

def get_dataset_config(task_name: str, dataset_name: str = None) -> dict:
    """
    Get configuration for specified task and dataset
    
    Args:
        task_name: Task name, e.g., 'enhancer'
        dataset_name: Dataset name, e.g., 'fulco', returns task-level config if None
    
    Returns:
        Dictionary containing configuration information
    """
    if task_name not in DATASET_CONFIG:
        raise ValueError(f"Unknown task name: {task_name}")
    
    if dataset_name is None:
        return DATASET_CONFIG[task_name]["task_config"]
        
    if dataset_name not in DATASET_CONFIG[task_name]:
        raise ValueError(f"Unknown dataset name: {dataset_name}")
    
    # Merge task-level config and dataset-specific config
    config = {
        **DATASET_CONFIG[task_name]["task_config"],
        **DATASET_CONFIG[task_name][dataset_name]
    }
    return config

def _decompress_gz(gz_path: Path) -> Path:
    """
    Decompress a .gz file
    
    Args:
        gz_path: Path to the .gz file
        
    Returns:
        Path to the decompressed file
    """
    output_path = gz_path.with_suffix('')  # Remove .gz extension
    
    if output_path.exists():
        print(f"Decompressed file already exists: {output_path}")
        return output_path
        
    print(f"Decompressing file: {gz_path}")
    with gzip.open(gz_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            f_out.write(f_in.read())
    print(f"Decompressed to: {output_path}")
    return output_path

def download_reference_genome(
    genome_version: str,
    cache_root: Union[str, Path],
    file_type: str = "both"
) -> Dict[str, Path]:
    """
    Download reference genome files for specified version
    
    Args:
        genome_version: Genome version, e.g., 'hg19', 'hg38', 'mm10'
        cache_root: Cache root directory
        file_type: Type of files to download, options: 'fasta', 'gtf', 'both'
        
    Returns:
        Dictionary containing paths to downloaded files
    """
    if genome_version not in DATASET_CONFIG["reference_genome"]:
        raise ValueError(f"Unsupported genome version: {genome_version}")
    
    if file_type not in ['fasta', 'gtf', 'both']:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Create download directory
    cache_dir = Path(cache_root) / "reference_genome" / genome_version
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Get download URLs
    genome_config = DATASET_CONFIG["reference_genome"][genome_version]
    downloader = DataDownloader(cache_dir=cache_dir)
    downloaded_files = {}
    
    try:
        if file_type in ['fasta', 'both']:
            # Check if decompressed file already exists
            fasta_path = cache_dir / genome_config['fasta_url'].split('/')[-1].replace('.gz', '')
            if not fasta_path.exists():
                # Download and decompress
                gz_path = downloader.download(
                    url=genome_config['fasta_url'],
                    force=False
                )
                fasta_path = _decompress_gz(gz_path)
            else:
                print(f"Using existing decompressed file: {fasta_path}")
            downloaded_files['fasta'] = fasta_path
            
        if file_type in ['gtf', 'both']:
            # Check if decompressed file already exists
            gtf_path = cache_dir / genome_config['gtf_url'].split('/')[-1].replace('.gz', '')
            if not gtf_path.exists():
                # Download and decompress
                gz_path = downloader.download(
                    url=genome_config['gtf_url'],
                    force=False
                )
                gtf_path = _decompress_gz(gz_path)
            else:
                print(f"Using existing decompressed file: {gtf_path}")
            downloaded_files['gtf'] = gtf_path
            
    except Exception as e:
        raise Exception(f"Failed to download reference genome files: {str(e)}")
    
    return downloaded_files 