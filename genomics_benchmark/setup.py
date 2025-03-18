from setuptools import setup, find_packages

setup(
    name="genomics_benchmark",
    version="0.1.0",
    description="A benchmark package for evaluating DNA sequence-based models",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "numpy",  # 基础科学计算
        "pandas",  # 数据处理
        "torch",  # 深度学习框架
        "tqdm",  # 进度条
        "requests",  # HTTP请求
        "scikit-learn",  # 机器学习工具
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
) 