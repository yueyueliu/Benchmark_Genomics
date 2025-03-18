"""
数据集配置文件，包含各个数据集的元数据信息
"""

DATASET_CONFIG = {
    "gene_expression": {
        "kiver": {
            "name": "Kiver Gene Expression",
            "description": "Kiver细胞系的基因表达数据",
            "data_url": "https://example.com/kiver_data",  # 需要替换为实际的数据URL
            "file_format": "csv",
            "preprocessing_steps": [
                "数据清洗",
                "标准化",
                "特征选择"
            ],
            "evaluation_metrics": [
                "MSE",
                "R2",
                "Pearson相关系数"
            ]
        },
        "k562": {
            "name": "K562 Gene Expression",
            "description": "K562细胞系的基因表达数据",
            "data_url": "https://example.com/k562_data",  # 需要替换为实际的数据URL
            "file_format": "csv",
            "preprocessing_steps": [
                "数据清洗",
                "标准化",
                "特征选择"
            ],
            "evaluation_metrics": [
                "MSE",
                "R2",
                "Pearson相关系数"
            ]
        }
    }
}

def get_dataset_config(task_name: str, dataset_name: str) -> dict:
    """
    获取指定任务和数据集的配置信息
    
    Args:
        task_name: 任务名称，如 'gene_expression'
        dataset_name: 数据集名称，如 'kiver'
    
    Returns:
        包含数据集配置信息的字典
    """
    if task_name not in DATASET_CONFIG:
        raise ValueError(f"未知的任务名称: {task_name}")
    if dataset_name not in DATASET_CONFIG[task_name]:
        raise ValueError(f"未知的数据集名称: {dataset_name}")
    return DATASET_CONFIG[task_name][dataset_name] 