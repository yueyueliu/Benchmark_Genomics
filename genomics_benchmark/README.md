# Genomics Benchmark

这是一个用于评估DNA序列预训练模型性能的benchmark包。该包提供了多个下游分析任务，用于全面评估模型在不同生物信息学任务上的表现。

## 功能特点

- 支持多个下游分析任务
  - 基因表达预测
    - Kiver数据集
    - K562数据集
  - 其他任务（持续添加中）
- 自动数据下载和预处理
- 标准化的评估指标
- 易于使用的API

## 安装

```bash
# 从GitHub安装
pip install git+https://github.com/yourusername/genomics_benchmark.git

# 或者克隆仓库后本地安装
git clone https://github.com/yourusername/genomics_benchmark.git
cd genomics_benchmark
pip install -e .
```

## 快速开始

```python
from genomics_benchmark import tasks

# 加载Kiver基因表达数据集
kiver_dataset = tasks.gene_expression.kiver.load_dataset()

# 加载K562基因表达数据集
k562_dataset = tasks.gene_expression.k562.load_dataset()

# 获取预处理后的数据
processed_data = tasks.gene_expression.kiver.preprocess()
```

## 项目结构

```
genomics_benchmark/
├── genomics_benchmark/
│   ├── tasks/           # 不同的下游任务
│   ├── data/           # 数据处理相关代码
│   └── utils/          # 工具函数
├── tests/              # 测试代码
└── setup.py           # 包配置文件
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License 