# Genomics Benchmark

一个用于基因组学任务基准测试的Python工具包。

## 功能特点

- 基因表达预测基准测试
- 增强子-启动子相互作用预测基准测试
- 标准化的评估指标
- 常用模型实现
- 数据预处理工具

## 安装

```bash
pip install genomics-benchmark
```

## 快速开始

```python
from genomics_benchmark.tasks import GeneExpressionPrediction
from genomics_benchmark.models import BaselineModel

# 初始化任务
task = GeneExpressionPrediction()

# 加载数据
train_data, test_data = task.load_data()

# 训练模型
model = BaselineModel()
model.train(train_data)

# 评估模型
metrics = task.evaluate(model, test_data)
print(metrics)
```

## 项目结构

```
genomics_benchmark/
├── tasks/           # 基准测试任务
├── data/            # 数据加载和处理
├── utils/           # 通用工具函数
├── models/          # 模型实现
├── metrics/         # 评估指标
└── config/          # 配置文件
```

## 支持的任务

1. 基因表达预测
   - 输入：DNA序列、表观遗传学特征
   - 输出：基因表达水平预测

2. 增强子-启动子相互作用预测
   - 输入：DNA序列对、染色质可及性数据
   - 输出：相互作用概率

## 贡献指南

欢迎提交问题和拉取请求。对于重大更改，请先开issue讨论您想要更改的内容。

## 许可证

[MIT](https://choosealicense.com/licenses/mit/)
