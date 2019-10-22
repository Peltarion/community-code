module.exports = function (context, req, documents) {
    context.log(context.bindings)
    context.res = documents;
    context.done();
};