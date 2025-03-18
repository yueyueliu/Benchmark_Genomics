"""
数据预处理模块，提供基础的数据预处理功能
"""
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union, Tuple, Optional
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    """数据预处理器基类"""
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def load_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        加载数据文件
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            加载的数据框
        """
        file_path = Path(file_path)
        if file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix == '.tsv':
            return pd.read_csv(file_path, sep='\t')
        else:
            raise ValueError(f"不支持的文件格式: {file_path.suffix}")
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        数据清洗
        
        Args:
            df: 输入数据框
            
        Returns:
            清洗后的数据框
        """
        # 删除重复行
        df = df.drop_duplicates()
        
        # 删除全为空的行
        df = df.dropna(how='all')
        
        # 删除全为空的列
        df = df.dropna(axis=1, how='all')
        
        return df
    
    def normalize_data(self, data: np.ndarray, fit: bool = True) -> np.ndarray:
        """
        数据标准化
        
        Args:
            data: 输入数据
            fit: 是否拟合新的标准化器
            
        Returns:
            标准化后的数据
        """
        if fit:
            return self.scaler.fit_transform(data)
        return self.scaler.transform(data)
    
    def split_data(
        self,
        data: np.ndarray,
        labels: np.ndarray,
        train_ratio: float = 0.8,
        val_ratio: float = 0.1,
        random_state: Optional[int] = None
    ) -> Tuple[np.ndarray, ...]:
        """
        划分训练集、验证集和测试集
        
        Args:
            data: 特征数据
            labels: 标签数据
            train_ratio: 训练集比例
            val_ratio: 验证集比例
            random_state: 随机种子
            
        Returns:
            训练集、验证集和测试集的特征和标签
        """
        np.random.seed(random_state)
        n_samples = len(data)
        
        # 计算每个集合的大小
        n_train = int(n_samples * train_ratio)
        n_val = int(n_samples * val_ratio)
        
        # 随机打乱索引
        indices = np.random.permutation(n_samples)
        
        # 划分索引
        train_indices = indices[:n_train]
        val_indices = indices[n_train:n_train + n_val]
        test_indices = indices[n_train + n_val:]
        
        # 划分数据
        X_train = data[train_indices]
        y_train = labels[train_indices]
        X_val = data[val_indices]
        y_val = labels[val_indices]
        X_test = data[test_indices]
        y_test = labels[test_indices]
        
        return X_train, y_train, X_val, y_val, X_test, y_test 