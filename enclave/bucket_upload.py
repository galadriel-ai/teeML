from google.cloud import storage
from google.oauth2 import service_account

KEY_PATH = "sidekik.json"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

storage_client = storage.Client(
    project="sidekik-ai",
    credentials=credentials,
)
bucket = storage_client.bucket("galadriel-assets")
blob = bucket.blob("kaspar.txt")
blob.upload_from_string(
    "hello world2", content_type="text/plain"
)
