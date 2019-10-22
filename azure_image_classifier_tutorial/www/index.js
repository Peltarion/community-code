let isLoading = false;
const setupSection = document.getElementById('setup-section');
const setupHeader = document.getElementById('setup-header');

const token = document.getElementById('token');
const url = document.getElementById('url');
const resultCanvas = document.getElementById('image-upload');
const resultPreview = document.getElementById('result-preview');
const imagePreview = document.getElementById('image-preview');

const uploadInput = document.getElementById('upload-input');

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

let imgFile = null;

let sasUrl = null;

const getToken = () => {
    const locationURL = new URL(window.location.href);
    const tokenParam = locationURL.searchParams.get('token');
    const urlParam = locationURL.searchParams.get('url');
    token.value = tokenParam || '';
    url.value = urlParam || '';  

};

setTimeout(() => {
    getToken();
}, 500);
// ------------------------------------------------
//
// Show & hide setup section
//
// ------------------------------------------------
setupHeader.addEventListener('click', () => {
    setupSection.classList.toggle('hidden');
    setupSection.classList.toggle('up');
});

// ------------------------------------------------
//
// Upload img & Get results actions
//
// ------------------------------------------------
const uploadImgButton = document.getElementById('upload-img-btn');
const getResultsButton = document.getElementById('get-results-btn');

uploadImgButton.addEventListener('click', (e) => {
    e.preventDefault();
    uploadInput.click();
});

getResultsButton.addEventListener('click', (e) => {
    e.preventDefault();
    if (!imgFile) {
        return;
    }
    uploadImage(resultCanvas, imgFile.name);
});


// ------------------------------------------------
//
// Drag & drop files
//
// ------------------------------------------------

function handleDroppedFile(e) {
    e.preventDefault();
    if (!isLoading) {
        saveFormdata();
        let files = extractFiles(e.dataTransfer);
        imgFile = null;
        if (files.length > 0) {
            imgFile = files[0];
            updateImage(imgFile, () => {
                getResultsButton.disabled = false;
            });
            imagePreview.classList.add('uploaded');
            getResultsButton.disabled = true;
        }
    }
    cleanupDragData(e.dataTransfer);
    return false;
}

function handleFileUpload(e) {
    console.log('reading file')
    let reader = new FileReader();
    let file = this.files[0];
    if (!file || Object.is(file, imgFile)) {
        return;
    }
    let timeout = setTimeout(() => {
        alert('FileReader not functioning');
    }, 500);
    imgFile = null;
    reader.onload = () => {
        clearTimeout(timeout);
        imgFile = file;
        updateImage(file, () => {
            getResultsButton.disabled = false;
        });
        imagePreview.classList.add('uploaded');
        getResultsButton.disabled = true;
    };
    reader.readAsDataURL(file);
}

function handleDragEnter(e) {
    e.preventDefault();
    return true;
}

const dropIcon = document.getElementById('drop-icon');
function handleDragOver(e) {
    e.preventDefault();
    if (!isLoading) {
        dropIcon.classList.add('uploaded');
    }
    return true;
}

function handleDragLeave(e) {
    e.preventDefault();
    return true;
}

function extractFiles(dataTransfer) {
    let files = [], i;
    if (dataTransfer.items) {
        for (i = 0; i < dataTransfer.items.length; i++) {
            if (dataTransfer.items[i].kind === 'file') {
                let file = dataTransfer.items[i].getAsFile();
                files.push(file);
            }
        }
    } else {
        for (i = 0; i < dataTransfer.files.length; i++) {
            files.push(dataTransfer.files[i]);
        }
    }
    return files;
}

function cleanupDragData(dataTransfer) {
    if (dataTransfer.items) {
        dataTransfer.items.clear();
    } else {
        dataTransfer.clearData();
    }
}

// ------------------------------------------------
//
// Layout actions
//
// ------------------------------------------------

const resetImage = () => {
    if (imgFile) {
        updateImage(imgFile, () => {
            getResultsButton.disabled = false;
        });
    }
}

// ------------------------------------------------
//
// Persistence & session
//
// ------------------------------------------------

const imgParamName = document.getElementById('image-param-name');
const imgWidth = document.getElementById('input-width');
const imgHeight = document.getElementById('input-height');
function saveFormdata() {
    localStorage.setItem('token', token.value);
    localStorage.setItem('url', url.value);
    localStorage.setItem('image-param-name', imgParamName.value);
    localStorage.setItem('input-width', imgWidth.value);
    localStorage.setItem('input-height', imgHeight.value);
}

function restoreFormdata() {
    token.value = localStorage.getItem('token') || '';
    url.value = localStorage.getItem('url') || '';
    imgParamName.value = localStorage.getItem('image-param-name') || '';
    imgWidth.value = localStorage.getItem('input-width') || '';
    imgHeight.value = localStorage.getItem('input-height') || '';
}


// ------------------------------------------------
//
// View & UI
//
// ------------------------------------------------


function renderImage(ctx, img, w, h) {
    let cw = ctx.canvas.width;
    let ch = ctx.canvas.height;
    ctx.clearRect(0, 0, cw, ch);
    ctx.fillStyle = 'rgb(0, 0, 0)';
    ctx.fillRect(0, 0, cw, ch);
    ctx.save();
    ctx.drawImage(img, (cw - w) * 0.5, (ch - h) * 0.5, w, h);
    ctx.restore();
}

function updateImage(file, callback) {
    let canvasBig = document.getElementById('image-big');
    let canvasUpload = resultCanvas;
    let ctxBig = canvasBig.getContext('2d');
    let ctxUpload = canvasUpload.getContext('2d');
    let img = new Image;
    let imageWidth = imgWidth.value;
    let imageHeight = imgHeight.value;

    canvasUpload.setAttribute('width', imageWidth);
    canvasUpload.setAttribute('height', imageHeight);

    img.src = URL.createObjectURL(file);
    img.onload = () => {
        let bigScale = Math.min(img.width, img.height);
        bigScale = Math.min(320 / bigScale, 1);
        let w = img.width * bigScale;
        let h = img.height * bigScale;

        renderImage(ctxBig, img, w, h);
        renderImage(ctxUpload, img, imageWidth, imageHeight);

        callback();
    }
}

function printStatus(message, isResult) {
    resultPreview.classList.toggle('result', isResult);
    document.getElementById('result').textContent = message;
}

// ------------------------------------------------
//
// API interaction
//
// ------------------------------------------------

function uploadImage(canvasElement, filename) {
    let config = {
            params : {
                'id' : filename,
                'pToken': token.value,
                'pUrl': url.value,
                'pInputName' : imgParamName.value,
                'pResizeDimensions' : { 
                    'imgWidth' : imgWidth.value, 
                    'imgHeigth' : imgHeight.value 
                }
            }
        }
    axios.post('https://img-classifier-python.azurewebsites.net/api/UploadImage', JSON.stringify(config))
        .then((res) => {
            /* Store returned SAS URL to upload image to */
            sasUrl = res.data.url
        }).catch(error => {
            printStatus('Bad robot!');
            console.log(error)
        });
    console.log(imgFile)
    _uploadBlob(sasUrl, imgFile)
    _getResults(imgFile.name)
}

function _getResults(id){
    resultsUrl = 'https://img-classifier-python.azurewebsites.net/api/GetResults?id=' + id
    printStatus('querying...')
    axios.get(resultsUrl)
        .then((res) => {
            if (res.data.prediction === ""){
                printStatus('...')
                sleep(5000).then(() => {
                  _getResults(id)
                  console.log('retrying')
                  printStatus('querying...')
                })
            } else {
                console.log(res.data.prediction);
                printStatus(res.data.prediction);
            }
        }).catch(error => {
            printStatus('Bad robot!');
            console.log(error)
        });
}

function _uploadBlob(sasUrlp, file) {
    const config = {
        headers: {
            'Content-Type': 'application/octet-stream',
            'x-ms-version': '2017-04-17',
            'x-ms-blob-type': 'BlockBlob',
            'x-ms-blob-content-type': file.type
        }
    }
    return axios.put(sasUrlp, file, config)
        .then(function (res) {
            console.log('Image uploaded!');
        })
        .catch(function (err) {
            printStatus('Bad robot!');
            console.log(err);
        });
}

// ------------------------------------------------
//
// Main & startup
//
// ------------------------------------------------


window.addEventListener('drop', handleDroppedFile, false);
window.addEventListener('dragenter', handleDragEnter, false);
window.addEventListener('dragover', handleDragOver, false);
window.addEventListener('dragenter', handleDragLeave, false);
uploadInput.addEventListener('change', handleFileUpload, false);
restoreFormdata();