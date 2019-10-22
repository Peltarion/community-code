const Jimp = require("jimp");

module.exports = function (context, myBlob) {
    
    context.log("JavaScript blob trigger function processed blob \n Name:", 
        context.bindingData.name, "\n Blob Size:", 
        myBlob.length, "Bytes");

    Jimp.read(myBlob).then(image => {
        context.log('Resizing to: ' + '28 x 28')
        image
        /* TODO: Take in resize dimenstions from request */
            
            .cover(28, 28) 
            .quality(60)
            .getBuffer(Jimp.MIME_JPEG, (error, stream) => {
                if (error) {
                    context.log('Error resizing image!')
                    context.done(error);
                } else {
                    context.log('Resize Successful! Writing the resized image to the blob storage...')
                    context.bindings.thumbnail = stream;
                    let document = {
                        id: context.bindingData.name,
                        prediction: '',
                        imgPath: "/images/" + context.bindingData.name,
                        thumbnailPath: "/thumbnails/" + context.bindingData.name,
                        pToken: context.bindings.documentBefore.pToken,
                        pUrl: context.bindings.documentBefore.pUrl
                    };
                    context.log('Updated Image Metadata Document: ');
                    context.log(document);
                    context.done(null, document)
                }
            });
    });
};