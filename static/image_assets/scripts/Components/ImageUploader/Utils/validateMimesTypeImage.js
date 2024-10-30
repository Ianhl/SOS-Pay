function validateMimesTypeImageAllowed(mime) {
  const mimesAllowed = ['image/jpeg', 'image/png'];

  if (!mimesAllowed.includes(mime)) {
    changeClassToShowOrHidden({ warning: true });
    buttonButtonBack.addEventListener('click', handleBackToImageUploader)
    return false;
  }

  return true;
}
