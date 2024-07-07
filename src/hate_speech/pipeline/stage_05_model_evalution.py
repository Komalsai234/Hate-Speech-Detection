from hate_speech.config.configuration import ConfigurationManager
from hate_speech.components.model_evalution import ModelEvalution
from hate_speech.logging import logger


class ModelEvalutionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_evalution_config = config.get_model_evalution_config()
        model_trainer_config = config.get_model_trainer_config()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation =ModelEvalution(config=model_evalution_config,model_trainer_config=model_trainer_config,
                                            data_transformation_config=data_transformation_config)
        data_transformation.evalute()