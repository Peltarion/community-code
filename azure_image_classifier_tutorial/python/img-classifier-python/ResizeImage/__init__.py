import logging

import azure.functions as func
import  PIL
import io
from PIL import Image

'''

'''
def main(myblob: func.InputStream, imageMetadataInList: func.DocumentList, imageMetadataOut: func.Out[func.Document]):

    logging.info(f"Python blob trigger function processed blob \n"
        f"Name: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes")

    imageMetadataIn = imageMetadataInList[0]
    logging.info(imageMetadataIn)
    
    logging.info("Opening BLOB as image...")
    image = Image.open(myblob)

    logging.info("Resizing image...")
    resizedImage = image.resize((28, 28), Image.BILINEAR)
    imgByteArr = io.BytesIO()

    logging.info("Converting image to byte array...")
    resizedImage.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()

    logging.info("Updating image metadata...")
    imageMetadataIn['resizedImagePath'] = "/resized-images/" + myblob.name
    imageMetadataOut.set(imageMetadataIn)

    return imgByteArr