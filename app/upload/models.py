from django.db import models
from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()

class Upload:
    @staticmethod
    def upload_image(file, filename):
        print(f"UPLOADING: {filename}")
        try:
            target_path = '/images/' + filename
            print(f"target_path: {target_path}")
            path = storage.save(target_path, file)
            print(f"target_path: {target_path}")
            return storage.url(path)
        except Exception as e:
            print("models: Failed to upload!")
