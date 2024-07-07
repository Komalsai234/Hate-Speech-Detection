from hate_speech.config.gcloud import GCloud
from hate_speech.entity.config_entity import ModelTrainerConfig
from hate_speech.constants import *
from hate_speech.logging import logger

class ModelPusher:
    def __init__(self,model_trainer_config:ModelTrainerConfig):
        self.gcloud = GCloud()
        self.model_trainer_config = model_trainer_config

    def sync_to_cloud(self)-> str:
        try: 
            self.gcloud.sync_model_and_tokenizer_to_gcloud(
                gcp_bucket_url=GCP_BUCKET_NAME,
                filepath=self.model_trainer_config.root_dir,
                model_name=MODEL_NAME,
                tokenizer_name=TOKENIZER_NAME)
            
            logger.info(f"Model and tokenizer are synced to GCloud Bucket")

        except Exception as e:
            raise e
