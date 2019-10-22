import logging
import json
import azure.functions as func
from datetime import datetime  
from datetime import timedelta
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess 
from azure.storage.blob.baseblobservice import BaseBlobService
from azure.storage.blob.models import BlobPermissions

def main(req: func.HttpRequest, imageMetadataOut: func.Out[func.Document]) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')
    request = req.get_json()
    name = request["params"]["id"]
    pUrl = request["params"]["pUrl"]
    pToken = request["params"]["pToken"]

    if name:
        sasUrl = get_sas_url(name);

        imageMetadata = {
            "id" : name,
            "prediction" : "",
            "imagePath" : "/images/" + name,
            "resizedImagePath" : "",
            "pToken" : pToken,
            "pUrl" : pUrl
        }

        resp_body = {
            "url" : sasUrl, 
            "imageMetadata" : imageMetadata
        }

        resp_headers  = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "Get, Post, Options"
        }

        response = func.HttpResponse(
            headers=resp_headers, 
            body=json.dumps(resp_body)
        )

        imageMetadataDocument = func.Document(imageMetadata)
        logging.info(response)
        imageMetadataOut.set(imageMetadataDocument)

        return response
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

def get_sas_url(name):

    baseblobservice = BaseBlobService(account_name='', account_key='')

    sasToken = baseblobservice.generate_blob_shared_access_signature(
        container_name='images', 
        blob_name=name, 
        permission = BlobPermissions(read=True, write=True, create=True),
        start = datetime.now() - timedelta(hours=2),
        expiry = datetime.now() + timedelta(hours=2))

    sasurl = baseblobservice.make_blob_url('images', name, sas_token=sasToken)

    return sasurl
