import os
import urllib.request as request
import zipfile
import gdown
from hate_speech.logging import logger
from hate_speech.utils.common import get_size
from hate_speech.entity.config_entity import DataIngestionConfig
from hate_speech.config.gcloud import GCloud
from hate_speech.constants import *

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.gcp_bucket = GCloud()


    def download_file(self)-> str:
        try: 
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")


            self.gcp_bucket.sync_folder_from_gcloud(
                gcp_bucket_url=GCP_BUCKET_NAME,
                filename=GCP_DATA_FILE_NAME,
                destination=self.config.local_data_file,
            )

            logger.info(f"Downloaded data from Google Cloud Bucket into file {zip_download_dir}")

        except Exception as e:
            raise e


        
    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)