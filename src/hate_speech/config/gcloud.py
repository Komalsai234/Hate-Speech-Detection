import os
from zipfile import Path
import time
from datetime import datetime
import subprocess


class GCloud:
    def sync_folder_to_gcloud(self, gcp_bucket_url, filepath, filename):

        command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        
        os.system(command)




    def sync_folder_from_gcloud(
        self, gcp_bucket_url: str, filename: str, destination: Path
    ):

        command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}"
        os.system(command)



    def sync_model_and_tokenizer_to_gcloud(self, gcp_bucket_url, filepath, model_name, tokenizer_name):

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        model_command = f"gsutil cp {filepath}/{model_name} gs://{gcp_bucket_url}/Model/{timestamp}/{model_name}"
        tokenizer_command = f"gsutil cp {filepath}/{tokenizer_name} gs://{gcp_bucket_url}/Model/{timestamp}/{tokenizer_name}"

        os.system(model_command)
        os.system(tokenizer_command)



    def sync_model_and_tokenizer_from_gcloud(self, gcp_bucket_url, model_name, tokenizer_name, destination, timestamp= None):
        if not timestamp:
            command = f"gsutil ls gs://{gcp_bucket_url}/Model/"
            result = subprocess.check_output(command, shell=True).decode("utf-8")
            folders = result.strip().split("\n")
            timestamps = [folder.split("/")[-2] for folder in folders if folder.split("/")[-2] != 'Model']

            if not timestamps:
                raise ValueError("No timestamped folders found in the Model directory.")
            
            latest_timestamp = max(timestamps)
            model_remote_path = f"gs://{gcp_bucket_url}/Model/{latest_timestamp}/{model_name}"
            toeknizer_remote_path = f"gs://{gcp_bucket_url}/Model/{latest_timestamp}/{tokenizer_name}"

        else:
            model_remote_path = f"gs://{gcp_bucket_url}/Model/{latest_timestamp}/{model_name}"
            toeknizer_remote_path = f"gs://{gcp_bucket_url}/Model/{latest_timestamp}/{tokenizer_name}"

        model_destination_path = os.path.join(destination, model_name)
        tokenizer_destination_path = os.path.join(destination, tokenizer_name)

        model_command = f"gsutil cp {model_remote_path} {model_destination_path}"
        tokenizer_command = f"gsutil cp {toeknizer_remote_path} {tokenizer_destination_path}"

        os.system(model_command)
        os.system(tokenizer_command)

