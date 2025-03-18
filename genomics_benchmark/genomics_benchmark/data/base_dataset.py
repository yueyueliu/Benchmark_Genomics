"""
Base dataset class that integrates data download and preprocessing functionality
"""
import os
from pathlib import Path
from typing import Optional, Union, Dict, Any
from .download import DataDownloader
from .reference_genome import get_dataset_config

class BaseDataset:
    """Base dataset class"""
    
    def __init__(
        self,
        task_name: str,
        dataset_name: str,
        cache_root: Optional[Union[str, Path]] = None
    ):
        """
        Initialize dataset
        
        Args:
            task_name: Name of the task
            dataset_name: Name of the dataset
            cache_root: Cache root directory, defaults to .cache/genomics_benchmark in user's home directory
        """
        self.task_name = task_name
        self.dataset_name = dataset_name
        
        # Set cache root directory
        if cache_root is None:
            cache_root = os.path.expanduser("~/.cache/genomics_benchmark")
        self.cache_root = Path(cache_root)
        
        # Create task and dataset specific cache directories
        self.cache_dir = self.cache_root / task_name / dataset_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Get configuration
        self.config = get_dataset_config(task_name, dataset_name)
        
        # Initialize downloader and preprocessor
        self.downloader = DataDownloader(self.cache_dir)
        
        # Data file paths
        self.data_path = None
        self.processed_data = None
    
    def download(self, force: bool = False) -> Path:
        """
        Download dataset
        
        Args:
            force: Whether to force re-download
            
        Returns:
            Path to the downloaded file
        """
        self.data_path = self.downloader.download(
            self.config["data_url"],
            force=force
        )
        return self.data_path
    
    def clear_cache(self, clear_all: bool = False):
        """
        Clear cache
        
        Args:
            clear_all: Whether to clear cache for all tasks, defaults to clearing only current dataset cache
        """
        if clear_all:
            # Clear all cache
            if self.cache_root.exists():
                for path in self.cache_root.glob("**/*"):
                    if path.is_file():
                        path.unlink()
                for path in reversed(list(self.cache_root.glob("**/*"))):
                    if path.is_dir():
                        path.rmdir()
        else:
            # Clear only current dataset cache
            if self.cache_dir.exists():
                for file in self.cache_dir.glob("*"):
                    file.unlink()
                self.cache_dir.rmdir()
        
        self.data_path = None
        self.processed_data = None
    
    @property
    def cache_path(self) -> Path:
        """Get cache directory for current dataset"""
        return self.cache_dir 