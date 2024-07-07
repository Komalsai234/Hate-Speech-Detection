import os
import json
import pickle
import pandas as pd
from hate_speech.logging import logger
from hate_speech.entity.config_entity import ModelEvalutionConfig, ModelTrainerConfig,DataTransformationConfig
from tensorflow.keras.models import load_model
from keras.utils import pad_sequences


class ModelEvalution:
    def __init__(self,  config:ModelEvalutionConfig,model_trainer_config:ModelTrainerConfig,data_transformation_config:DataTransformationConfig):
        self.model_evalution_config = config
        self.model_trainer_config = model_trainer_config
        self.data_transformation_config = data_transformation_config

    def evalute(self)-> str:
        try: 
            with open(self.model_trainer_config.saved_tokenizer_path, 'rb') as handle:
                tokenizer = pickle.load(handle)

            model = load_model(self.model_trainer_config.saved_model_path)

            y = pd.read_csv(self.data_transformation_config.test_data_file)
            y['tweet'] = y['tweet'].astype(str)

            x_test,y_test = y['tweet'],y['label']

            test_sequences = tokenizer.texts_to_sequences(x_test)
            test_sequences_matrix = pad_sequences(test_sequences,maxlen=self.model_trainer_config.max_len)

            accr = model.evaluate(test_sequences_matrix,y_test)

            metrics = {"eval": accr}

            with open(self.model_evalution_config.metrics_file, "w") as file:
                json.dump(metrics, file)

            logger.info(f"Model Evalution completed saving the metrics file at {self.model_evalution_config.metrics_file}")


        except Exception as e:
            raise e
