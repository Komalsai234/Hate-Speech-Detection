from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path



@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    ALL_REQUIRED_FILES: list



@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    test_split: float
    train_data_file: Path
    test_data_file: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    max_words: int
    max_len: int
    batch_size: int
    epochs: int
    validation_split: float
    saved_tokenizer_path:Path
    saved_model_path:Path

@dataclass(frozen=True)
class ModelEvalutionConfig:
    root_dir: Path
    metrics_file:Path