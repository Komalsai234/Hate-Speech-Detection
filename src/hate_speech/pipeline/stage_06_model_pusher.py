from hate_speech.config.configuration import ConfigurationManager
from hate_speech.logging import logger
from hate_speech.components.model_pusher import ModelPusher


class ModelPusherTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_pusher = ModelPusher(model_trainer_config=model_trainer_config)
        model_pusher.sync_to_cloud()