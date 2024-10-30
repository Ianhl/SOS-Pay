const zoneDragAndDrop = document.getElementById('dragAndDrop');
zoneDragAndDrop.addEventListener('dragover', (event) => {
  event.preventDefault();
});

zoneDragAndDrop.addEventListener('drop', (event) => {
  event.preventDefault();
  changeClassToShowOrHidden({ imageUploader: false, warning: false });

  const file = event.dataTransfer.files[0];
  
  if (!validateMimesTypeImageAllowed(file.type)) {
    return;
  }
  
  createPreviewImage(file);
});

buttonCopyLink.addEventListener('click', () => handleCopyText(textImageLink));
inputChooseImage.addEventListener('change', (event) => openImageUploading(event));


function handleBackToImageUploader() {
  changeClassToShowOrHidden({
    warning: false,
    imageUploader: true,
  });
}

async function handleChangedImage(event) {
  await delay(800);
  changeClassToShowOrHidden({ imageUploader: false, warning: false });
  
  const file = event.target.files[0];

  const isValidMimeType = validateMimesTypeImageAllowed(file.type);
  if (!isValidMimeType) {
    return event.target.value = '';
  }
  console.log(event.target.files[0])

  createPreviewImage(file);
}

function createPreviewImage(file) {
  const imageUrl = URL.createObjectURL(file)
  textImageLink.textContent = imageUrl;
  imageAdded.setAttribute('src', imageUrl);
}

async function openImageUploading(event) {
  const modal = document.querySelector('.container__modal__uploading');
  
  containerImageUploader.classList.add('none')
  modal.classList.remove('none');
  
  await handleChangedImage(event);
  
  modal.classList.add('none');
}

function handleCopyText(element = null) {
  return navigator.clipboard.writeText(element.textContent)
}