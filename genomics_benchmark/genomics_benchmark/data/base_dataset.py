"""
数据集基类，整合数据下载和预处理功能
"""
from pathlib import Path
from typing import Optional, Union, Dict, Any
from .download import DataDownloader
from .preprocessing import DataPreprocessor
from .dataset_config import get_dataset_config

class BaseDataset:
    """数据集基类"""
    
    def __init__(
        self,
        task_name: str,
        dataset_name: str,
        cache_dir: Optional[Union[str, Path]] = None
    ):
        """
        初始化数据集
        
        Args:
            task_name: 任务名称
            dataset_name: 数据集名称
            cache_dir: 缓存目录
        """
        self.task_name = task_name
        self.dataset_name = dataset_name
        self.config = get_dataset_config(task_name, dataset_name)
        self.downloader = DataDownloader(cache_dir)
        self.preprocessor = DataPreprocessor()
        
        # 数据文件路径
        self.data_path = None
        self.processed_data = None
    
    def download(self, force: bool = False) -> Path:
        """
        下载数据集
        
        Args:
            force: 是否强制重新下载
            
        Returns:
            下载文件的路径
        """
        self.data_path = self.downloader.download(
            self.config["data_url"],
            force=force
        )
        return self.data_path
    
    def load(self) -> Dict[str, Any]:
        """
        加载并预处理数据
        
        Returns:
            处理后的数据字典
        """
        if self.data_path is None:
            self.download()
        
        # 加载原始数据
        raw_data = self.preprocessor.load_data(self.data_path)
        
        # 数据清洗
        cleaned_data = self.preprocessor.clean_data(raw_data)
        
        # 数据标准化
        normalized_data = self.preprocessor.normalize_data(cleaned_data)
        
        # 划分数据集
        X_train, y_train, X_val, y_val, X_test, y_test = self.preprocessor.split_data(
            normalized_data,
            cleaned_data["target"].values  # 假设标签列名为"target"
        )
        
        self.processed_data = {
            "train": {"X": X_train, "y": y_train},
            "val": {"X": X_val, "y": y_val},
            "test": {"X": X_test, "y": y_test}
        }
        
        return self.processed_data
    
    def get_data(self, split: str = "train") -> Dict[str, Any]:
        """
        获取指定划分的数据
        
        Args:
            split: 数据集划分，可选 "train", "val", "test"
            
        Returns:
            指定划分的特征和标签
        """
        if self.processed_data is None:
            self.load()
        
        if split not in self.processed_data:
            raise ValueError(f"未知的数据集划分: {split}")
        
        return self.processed_data[split]
    
    def clear_cache(self):
        """清除缓存"""
        self.downloader.clear_cache()
        self.data_path = None
        self.processed_data = None 