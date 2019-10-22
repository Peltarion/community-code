/**
Serverless cloud function that returns a time-limited SAS URI for blob upload
**/
const azure = require('azure-storage');

module.exports = function (context, req) {

    context.log('Received request for new SAS URI...')
    jsonReq = JSON.parse(req.body);
    context.log(jsonReq)

    const id = jsonReq.params.id;
    const container = 'images';

    context.log('Creating Azure Blob Service...')
    const blobService = azure.createBlobService();

    const currentDate = new Date();
    const startDate = new Date(currentDate.getTime() - 60 * 1000);
    const expiryDate = new Date(currentDate.getTime() + 5 * 60 * 1000);

    context.log('Setting SAS permissions...');
    const permissions = 
        azure.BlobUtilities.SharedAccessPermissions.READ +
        azure.BlobUtilities.SharedAccessPermissions.WRITE +
        azure.BlobUtilities.SharedAccessPermissions.CREATE;
    context.log(permissions);

    context.log('Setting SAS policy...');
    const sharedAccessPolicy = {
        AccessPolicy: {
            Permissions: permissions,
            Start: startDate,
            Expiry: expiryDate
        }
    };
    context.log(sharedAccessPolicy);

    context.log('Generating SAS token...');
    const sasToken = blobService.generateSharedAccessSignature(container, id, sharedAccessPolicy);
    context.log(sasToken)

    context.log('Creating Image Metadata Document...');
    let document = {
        id: id,
        prediction: '',
        imagePath: '',
        thumbnailPath: '',
        pToken: jsonReq.params.pToken,
        pUrl: jsonReq.params.pUrl
    };
    context.log(document)

    context.log('Generating SAS URL...');
    sasuri = blobService.getUrl(container, id, sasToken)
    context.log(sasuri)


    context.res = { 
        status: 200, body: 
        {
            url: sasuri,
            imageMetadata: document
        }
    };
    context.log(context.res);

    context.done(null, document);
};
