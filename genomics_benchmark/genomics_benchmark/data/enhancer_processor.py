"""
Enhancer data processing module
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Union, Optional, Tuple
from sklearn.metrics import roc_auc_score, average_precision_score
from .base_dataset import BaseDataset
from .reference_genome import get_dataset_config

class EnhancerProcessor(BaseDataset):
    """Enhancer data processing class"""
    
    def __init__(self, dataset_name: str, cache_root: Optional[Union[str, Path]] = None):
        """
        Initialize enhancer data processor
        
        Args:
            dataset_name: Dataset name, e.g., 'fulco'
            cache_root: Cache root directory, defaults to .cache/genomics_benchmark in user's home directory
        """
        super().__init__("enhancer", dataset_name, cache_root)
        
    def load(self, distance_threshold: Optional[int] = None) -> pd.DataFrame:
        """
        Load and preprocess data
        
        Args:
            distance_threshold: Optional distance threshold, no filtering if not specified
            
        Returns:
            Processed DataFrame
        """
        if self.data_path is None:
            self.download()
        
        # Load data based on file format
        raw_data = self._load_file(self.data_path)
        
        # Standardize column names
        processed_data = self._standardize_columns(raw_data)
        
        # Calculate distances and labels
        processed_data = self._process_data(processed_data)
        
        # Filter data
        processed_data = self._filter_data(processed_data, distance_threshold)
        
        return processed_data
    
    def _load_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data based on file format
        
        Args:
            file_path: Path to the file
            
        Returns:
            Loaded DataFrame
        """
        file_path = Path(file_path)
        if file_path.suffix == '.xlsx':
            return pd.read_excel(file_path)
        elif file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix == '.tsv':
            return pd.read_csv(file_path, sep='\t')
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names
        
        Args:
            df: Original DataFrame
            
        Returns:
            DataFrame with standardized column names
        """
        # Get column mapping
        column_mapping = self.config["column_mapping"]
        
        # Check if required columns exist
        required_columns = []
        for cols in self.config["required_columns"].values():
            if isinstance(cols, list):
                required_columns.extend(cols)
            else:
                required_columns.append(cols)
        
        missing_columns = []
        for col in required_columns:
            if col not in column_mapping or column_mapping[col] not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Rename columns
        reverse_mapping = {v: k for k, v in column_mapping.items()}
        return df.rename(columns=reverse_mapping)
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process data: calculate distances and labels
        
        Args:
            df: DataFrame with standardized column names
            
        Returns:
            Processed DataFrame
        """
        # Calculate enhancer center point
        df['enhancer_center'] = (df['start'] + df['end']) // 2
        
        # Calculate distance to TSS
        df['distance'] = abs(df['enhancer_center'] - df['gene_tss'])
        
        # 从数据集配置中获取标签列名
        label_column = self.config["label_column"]
        
        # Determine regulatory labels based on effect size
        df['labels'] = df[label_column].apply(lambda x: 1 if x == 1 else 0)
        
        return df
    
    def _filter_data(self, df: pd.DataFrame, distance_threshold: Optional[int] = None) -> pd.DataFrame:
        """
        Filter data based on distance threshold
        
        Args:
            df: Processed DataFrame
            distance_threshold: Optional distance threshold, uses config threshold if not specified,
                             no filtering if set to None
            
        Returns:
            Filtered DataFrame
        """
        if distance_threshold is not None:
            df = df[df['distance'] <= distance_threshold]
        elif 'distance_threshold' in self.config:
            df = df[df['distance'] <= self.config['distance_threshold']]
            
        # Get all columns to keep
        columns_to_keep = self.config["output_columns"].copy()
        if "additional_columns" in self.config:
            columns_to_keep.extend(self.config["additional_columns"])
            
        return df[columns_to_keep]
    
    def save_processed_data(self, output_path: Union[str, Path]) -> None:
        """
        Save processed data to file
        
        Args:
            output_path: Path to save the processed data
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get output columns from config
        output_columns = self.config["task_config"]["output_columns"].copy()
        
        # Add additional columns if specified
        if "additional_columns" in self.config:
            output_columns.extend(self.config["additional_columns"])
        
        # Ensure all required columns exist
        missing_columns = [col for col in output_columns if col not in self.processed_data.columns]
        if missing_columns:
            print(f"Warning: Missing columns in processed data: {missing_columns}")
            # Remove missing columns from output_columns
            output_columns = [col for col in output_columns if col in self.processed_data.columns]
        
        # Save data
        self.processed_data[output_columns].to_csv(output_path, sep='\t', index=False)
        print(f"Processed data saved to: {output_path}")
        print(f"Columns saved: {output_columns}")
    
    def calculate_metrics(self, df: pd.DataFrame, score_column: str = 'ABC Score') -> Dict[str, float]:
        """
        Calculate AUROC and AUPRC between specified column and labels
        
        Args:
            df: DataFrame
            score_column: Score column name for metric calculation, defaults to 'ABC Score'
            
        Returns:
            Dictionary containing AUROC and AUPRC
        """
        if score_column not in df.columns:
            raise ValueError(f"Column not found in data: {score_column}")
        
        if 'labels' not in df.columns:
            raise ValueError("Labels column not found in data")
            
        # Ensure no missing values
        valid_mask = ~(df[score_column].isna() | df['labels'].isna())
        scores = df.loc[valid_mask, score_column]
        labels = df.loc[valid_mask, 'labels']
        
        # Calculate AUROC and AUPRC
        auroc = roc_auc_score(labels, scores)
        auprc = average_precision_score(labels, scores)
        
        return {
            'AUROC': auroc,
            'AUPRC': auprc
        }
    
    def analyze_label_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze label distribution
        
        Args:
            df: DataFrame
            
        Returns:
            Dictionary containing label distribution information
        """
        if 'labels' not in df.columns:
            raise ValueError("Labels column not found in data")
        
        # Calculate label distribution
        label_counts = df['labels'].value_counts()
        label_percentages = df['labels'].value_counts(normalize=True) * 100
        
        # Calculate total samples and positive-negative ratio
        total_samples = len(df)
        pos_neg_ratio = label_counts[1] / label_counts[0] if 0 in label_counts and 1 in label_counts else 0
        
        return {
            'total_samples': total_samples,
            'label_counts': label_counts.to_dict(),
            'label_percentages': label_percentages.to_dict(),
            'positive_negative_ratio': pos_neg_ratio
        }
    
    def _add_strand_info(self, df: pd.DataFrame, gtf_file: Union[str, Path]) -> pd.DataFrame:
        """
        Add gene strand information from GTF file
        
        Args:
            df: DataFrame
            gtf_file: Path to GTF file
            
        Returns:
            DataFrame with added strand information
        """
        print("Reading gene annotation from GTF file...")
        # Read GTF file
        gene_annotation = pd.read_csv(
            gtf_file, sep='\t', comment='#', header=None,
            names=['chr', 'source', 'type', 'start', 'end', 'score', 'strand', 'frame', 'attribute']
        )
        
        # Extract gene information
        gene_annotation = gene_annotation[gene_annotation['type'] == 'gene']
        gene_annotation['gene_name'] = gene_annotation['attribute'].str.extract(r'gene_name "(.*?)";')
        gene_annotation['gene_name'] = gene_annotation['gene_name'].str.replace('"', '')
        
        # 如果存在重复的gene_name，保留第一个出现的strand信息
        gene_annotation = gene_annotation.drop_duplicates(subset=['gene_name'], keep='first')
        gene_annotation = gene_annotation[['gene_name', 'strand']]
        
        # Merge strand information
        print("Adding strand information...")
        df = df.merge(
            gene_annotation[['gene_name', 'strand']],
            on='gene_name',
            how='left'
        )
        
        # Check for missing strand information
        missing_strand = df['strand'].isna().sum()
        if missing_strand > 0:
            print(f"Warning: {missing_strand} genes have missing strand information")
            
        return df

    def initialize_pipeline(
        self,
        output_path: Optional[Union[str, Path]] = None,
        distance_threshold: Optional[int] = None,
        clear_cache: bool = True,
        do_statistics: bool = True,
        download_genome: bool = False,
        genome_file_type: str = "both",
        add_strand: bool = False
    ) -> Dict[str, Any]:
        """
        Initialize and run data processing pipeline
        
        Args:
            output_path: Path to save processed data
            distance_threshold: Optional distance threshold
            clear_cache: Whether to clear cache
            do_statistics: Whether to perform statistical analysis
            download_genome: Whether to download reference genome files
            genome_file_type: Type of genome files to download, options: 'fasta', 'gtf', 'both'
            add_strand: Whether to add gene strand information
            
        Returns:
            Dictionary containing processing results
        """
        results = {}
        
        try:
            # Output dataset basic information
            print(f"Dataset name: {self.config['name']}")
            print(f"Description: {self.config['description']}")
            genome_version = self.config.get('genome_version')
            print(f"Reference genome version: {genome_version if genome_version else 'Not specified'}")
            print()
            
            # 0. Download reference genome (if needed)
            if download_genome or add_strand:
                if not genome_version:
                    print("Warning: Dataset has no specified genome version, skipping genome download")
                else:
                    print("0. Downloading reference genome files...")
                    try:
                        from .reference_genome import download_reference_genome
                        genome_files = download_reference_genome(
                            genome_version=genome_version,
                            cache_root=self.cache_root,
                            file_type="both" if download_genome else "gtf"
                        )
                        print("Reference genome files downloaded successfully:")
                        for file_type, file_path in genome_files.items():
                            print(f"{file_type.upper()} file: {file_path}")
                        results['genome_files'] = genome_files
                        print()
                    except Exception as e:
                        print(f"Failed to download reference genome: {str(e)}\n")
                        results['genome_download_error'] = str(e)
                        if add_strand:
                            raise ValueError("Cannot add strand information: Reference genome download failed")
            
            # 1. Download data
            print("1. Starting data download...")
            data_path = self.download()
            print(f"Data downloaded to: {data_path}")
            results['download_path'] = str(data_path)
            
            # 2. Process data
            print("\n2. Processing data...")
            processed_data = self.load(distance_threshold=distance_threshold)
            
            # 2.1 Add strand information (if needed)
            if add_strand:
                if 'genome_files' not in results or 'gtf' not in results['genome_files']:
                    raise ValueError("Cannot add strand information: GTF file not available")
                processed_data = self._add_strand_info(processed_data, results['genome_files']['gtf'])
            
            print(f"Data shape: {processed_data.shape}")
            print(f"Columns: {processed_data.columns.tolist()}")
            results['data_shape'] = processed_data.shape
            results['columns'] = processed_data.columns.tolist()
            
            # 3. Save processed data
            if output_path:
                print("\n3. Saving processed data...")
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                processed_data.to_csv(output_path, sep='\t', index=False)
                print(f"Data saved to: {output_path}")
                results['output_path'] = str(output_path)
            
            # 4. Clear cache
            if clear_cache:
                print("\n4. Clearing cache...")
                self.clear_cache(clear_all=True)
                results['cache_cleared'] = True
            
            # 5. Statistical analysis
            if do_statistics:
                print("\n5. Performing statistical analysis...")
                # Calculate performance metrics
                metrics = self.calculate_metrics(processed_data, score_column='ABC Score')
                print("\nPerformance metrics:")
                
                if metrics['AUROC'] is not None and metrics['AUPRC'] is not None:
                    print(f"AUROC: {metrics['AUROC']:.3f}")
                    print(f"AUPRC: {metrics['AUPRC']:.3f}")
                
                results['metrics'] = metrics
                
                # Analyze label distribution
                distribution = self.analyze_label_distribution(processed_data)
                print("\nLabel distribution:")
                print(f"Total samples: {distribution['total_samples']:,}")
                print("\nLabel counts:")
                for label, count in distribution['label_counts'].items():
                    print(f"Label {label}: {count:,}")
                print("\nLabel percentages:")
                for label, percentage in distribution['label_percentages'].items():
                    print(f"Label {label}: {percentage:.2f}%")
                print(f"\nPositive-negative ratio: {distribution['positive_negative_ratio']:.3f}")
                results['distribution'] = distribution
            
            print("\nInitialization complete!")
            results['status'] = 'success'
            
        except Exception as e:
            print(f"Error: {str(e)}")
            results['status'] = 'error'
            results['error_message'] = str(e)
            raise
        
        return results 