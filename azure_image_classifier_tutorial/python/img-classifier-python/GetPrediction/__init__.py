import logging
import azure.functions as func
import sidekick
import  PIL
from PIL import Image

def main(myblob: func.InputStream, imageMetadataInList: func.DocumentList) -> func.Document:
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    imageMetadataIn = imageMetadataInList[0]

    logging.info(imageMetadataIn)

    client = sidekick.Deployment(
        url=imageMetadataIn['pUrl'],
        token=imageMetadataIn['pToken'],
        dtypes_in={'Image': 'Image (28x28x3)'},
        dtypes_out={'Number': 'Categorical (10)'}
    )

    logging.info("Loading image...")
    image = Image.open(myblob)

    logging.info("Getting predictions from model")
    prediction = client.predict(Image=image)
    logging.info(prediction)

    logging.info("Updating the image metadata with the prediction...")

    classifications = prediction['Number']

    top_score = top_key = 0
    for key, score in classifications.items():
        if score > top_score:
            top_score = score
            top_key = key

    logging.info("Prediction: " + top_key)

    imageMetadataIn['prediction'] = top_key
    return imageMetadataIn


