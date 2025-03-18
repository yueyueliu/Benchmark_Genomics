"""
Reference genome processing module
"""
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
            fasta_path = downloader.download(
                url=genome_config['fasta_url'],
                force=False
            )
            downloaded_files['fasta'] = fasta_path
            
        if file_type in ['gtf', 'both']:
            gtf_path = downloader.download(
                url=genome_config['gtf_url'],
                force=False
            )
            downloaded_files['gtf'] = gtf_path
            
    except Exception as e:
        raise Exception(f"Failed to download reference genome files: {str(e)}")
    
    return downloaded_files 