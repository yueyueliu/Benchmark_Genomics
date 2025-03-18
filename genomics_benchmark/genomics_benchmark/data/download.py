"""
数据下载模块，提供基础的数据下载和缓存功能
"""
import os
import hashlib
import requests
from pathlib import Path
from tqdm import tqdm
from typing import Optional, Union
from genomics_benchmark.data.base_dataset import BaseDataset

class DataDownloader:
    """数据下载器基类"""
    
    def __init__(self, cache_dir: Optional[Union[str, Path]] = None):
        """
        初始化数据下载器
        
        Args:
            cache_dir: 数据缓存目录，默认为用户主目录下的.cache/genomics_benchmark
        """
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/genomics_benchmark")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, url: str) -> Path:
        """
        根据URL生成缓存文件路径
        
        Args:
            url: 数据文件的URL
            
        Returns:
            缓存文件路径
        """
        # 使用URL的MD5作为文件名
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / url_hash
    
    def download(self, url: str, force: bool = False) -> Path:
        """
        下载数据文件
        
        Args:
            url: 数据文件的URL
            force: 是否强制重新下载
            
        Returns:
            下载文件的路径
        """
        cache_path = self._get_cache_path(url)
        
        if not force and cache_path.exists():
            print(f"使用缓存文件: {cache_path}")
            return cache_path
        
        print(f"下载文件: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        
        with open(cache_path, 'wb') as f, tqdm(
            desc="下载进度",
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
        """清除所有缓存文件"""
        for file in self.cache_dir.glob("*"):
            file.unlink()
        print(f"已清除缓存目录: {self.cache_dir}")

# 创建数据集实例
dataset = BaseDataset(
    task_name="gene_expression",
    dataset_name="kiver"
)

# 下载数据
dataset.download()

# 加载并预处理数据
processed_data = dataset.load()

# 获取训练集数据
train_data = dataset.get_data(split="train") 