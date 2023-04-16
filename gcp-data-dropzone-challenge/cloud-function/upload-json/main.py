import json
import os
from datetime import datetime
from http.client import HTTPException

from google.cloud import storage


def upload_json(request):
    if not request.method == 'POST':
        raise HTTPException('Incorrect request method!')

    file = request.files.get('file_upload')
    if not file:
        raise HTTPException('Empty JSON file provided!')

    file_content = json.loads(file.read())
    current_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(os.environ.get("BUCKET_NAME"))
    blob = bucket.blob(f"{current_timestamp}_{file.filename}")
    blob.upload_from_string(json.dumps(file_content), content_type='application/json')

    return "JSON data successfully uploaded!"
