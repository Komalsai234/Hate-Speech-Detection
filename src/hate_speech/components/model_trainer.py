import pandas as pd
import pickle
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding, SpatialDropout1D
from keras.optimizers import RMSprop
from sklearn.model_selection import train_test_split
from hate_speech.logging import logger
import os
import json
from hate_speech.entity.config_entity import ModelTrainerConfig
from hate_speech.entity.config_entity import DataTransformationConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig, data_transformation_config:DataTransformationConfig):
        self.config = config
        self.data_transformation_config = data_transformation_config

    
    def train(self):

        x = pd.read_csv(self.data_transformation_config.train_data_file)
        x['tweet'] = x['tweet'].astype(str)
        
        x_train,y_train = x['tweet'],x['label']

        print(len(x_train),len(y_train))


        max_words = self.config.max_words
        max_len = self.config.max_len

        tokenizer = Tokenizer(num_words=max_words)
        tokenizer.fit_on_texts(x_train)


        sequences = tokenizer.texts_to_sequences(x_train)
        sequences_matrix = pad_sequences(sequences,maxlen=max_len)
        
        with open(self.config.saved_tokenizer_path, 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)


        model = Sequential()
        model.add(Embedding(self.config.max_words,100,input_length=self.config.max_len))
        model.add(SpatialDropout1D(0.2))
        model.add(LSTM(100,dropout=0.2,recurrent_dropout=0.2))
        model.add(Dense(1,activation='sigmoid'))
        model.summary()

        model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])

        model.fit(sequences_matrix,y_train,batch_size=self.config.batch_size,epochs = self.config.epochs,validation_split=self.config.validation_split)

        logger.info('Model training completed')

        model.save(self.config.saved_model_path)

        logger.info('Trained Model saved')

