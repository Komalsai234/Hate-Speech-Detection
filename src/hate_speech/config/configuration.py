from hate_speech.constants import *
from hate_speech.utils.common import read_yaml, create_directories
from hate_speech.entity.config_entity import (DataIngestionConfig,
                                                     DataValidationConfig,
                                                     DataTransformationConfig,
                                                     ModelTrainerConfig,ModelEvalutionConfig)



class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config
    

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_validation_config
    


    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            test_split=config.test_split,
            train_data_file=config.train_data_file,
            test_data_file=config.test_data_file
        )

        return data_transformation_config
    


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.TrainingArguments

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            max_words = params.max_words,
            max_len = params.max_len,
            batch_size = params.batch_size,
            epochs = params.epochs,
            validation_split = params.validation_split,
            saved_tokenizer_path=config.saved_tokenizer_path,
            saved_model_path=config.saved_model_path
            
        )

        return model_trainer_config
    

    def get_model_evalution_config(self) -> ModelEvalutionConfig:
        config = self.config.model_evalution

        create_directories([config.root_dir])

        model_trainer_config = ModelEvalutionConfig(
            root_dir=config.root_dir,
            metrics_file=config.metrics_file
        )

        return model_trainer_config