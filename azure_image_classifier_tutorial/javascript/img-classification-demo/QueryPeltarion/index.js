const axios = require('axios');
const FormData = require('form-data');

module.exports = function(context, myBlob) {

    let imageMetadata = context.bindings.documentBefore
    context.log('Loading Image Metadata Document...');
    context.log(imageMetadata);

    context.log('Creating the request header & parameters');
    let config = {
        headers: {
             'Authorization': 'Bearer ' + imageMetadata.pToken
             }};
    context.log('Headers:')
    context.log(config)

    let params = {};
    let typedBlob = myBlob.slice(0, myBlob.length, 'application/octet-stream');
    context.log(typedBlob);

    params['Image'] = ['myBlob', imageMetadata.id.split('.')[0] + '.jpg'];

    context.log('Parameters:')
    context.log(params)

    let formData = new FormData();
    let p;
    for (p in params) {
        formData.append.apply(formData, [p].concat(params[p]));
    }   

    context.log('Form-data:')
    context.log(formData)

    context.log('Sending the request to: ' + imageMetadata.pUrl)
    axios.post(imageMetadata.pUrl, formData, config)
    .then((res) => {
        context.log('Successful request!')
        context.res(response);
	}).catch(error => {
        context.log('Ugh! Something is broken!')
        context.log(error)
    });

    context.done();
}