"""
Data download module providing basic data download and caching functionality
"""
import os
import hashlib
import requests
from pathlib import Path
from tqdm import tqdm
from typing import Optional, Union

class DataDownloader:
    """Base data downloader class"""
    
    def __init__(self, cache_dir: Union[str, Path]):
        """
        Initialize data downloader
        
        Args:
            cache_dir: Data cache directory
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, url: str) -> Path:
        """
        Generate cache file path from URL
        
        Args:
            url: URL of the data file
            
        Returns:
            Cache file path
        """
        # Extract filename from URL
        filename = url.split('/')[-1]
        # If no filename in URL, use MD5 of URL as filename
        if not filename or '?' in filename:
            filename = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / filename
    
    def download(self, url: str, force: bool = False) -> Path:
        """
        Download data file
        
        Args:
            url: URL of the data file
            force: Whether to force re-download
            
        Returns:
            Path to the downloaded file
        """
        cache_path = self._get_cache_path(url)
        
        if not force and cache_path.exists():
            print(f"Using cached file: {cache_path}")
            return cache_path
        
        print(f"Downloading file: {url}")
        print(f"Saving to: {cache_path}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        
        with open(cache_path, 'wb') as f, tqdm(
            desc="Download progress",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(block_size):
                size = f.write(data)
                pbar.update(size)
        
        return cache_path
    
    def clear_cache(self):
        """Clear all cached files"""
        for file in self.cache_dir.glob("*"):
            file.unlink()
        print(f"Cache directory cleared: {self.cache_dir}")
