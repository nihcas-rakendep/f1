import os
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="input/{name}", connection="AzureWebJobsStorage")
def move_blob(myblob: func.InputStream):
    logging.info(f"Moving blob: {myblob.name}")

    conn_str = os.environ["AzureWebJobsStorage"]

    blob_service = BlobServiceClient.from_connection_string(conn_str)

    # get blob name (file only)
    blob_name = myblob.name.split("/", 1)[1] if "/" in myblob.name else myblob.name

    source_container = "input"
    archive_container = "archive"

    source_blob = blob_service.get_blob_client(source_container, blob_name)
    archive_blob = blob_service.get_blob_client(archive_container, blob_name)

    # copy to archive
    archive_blob.start_copy_from_url(source_blob.url)

    # delete original
    source_blob.delete_blob()
    

    logging.info(f"Moved {blob_name} to archive")