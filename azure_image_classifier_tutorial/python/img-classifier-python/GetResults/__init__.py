import logging
import azure.functions as func

def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    if not documents:
        logging.warning("document not found")
        return "Bad robot! :("
    else:
        logging.info("Found Document, Description=%s",
                     documents[0].to_json())

        resp_headers  = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "Get, Post, Options"
        }

        response = func.HttpResponse(
            headers=resp_headers, 
            body=documents[0].to_json()
        )

        return response