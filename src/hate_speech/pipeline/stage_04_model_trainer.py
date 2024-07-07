from hate_speech.config.configuration import ConfigurationManager
from hate_speech.components.model_trainer import ModelTrainer
from hate_speech.logging import logger


class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        data_transformation_config = config.get_data_transformation_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config,data_transformation_config=data_transformation_config)
        model_trainer_config.train()