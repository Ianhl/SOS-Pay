document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("imageUploaderForm");
    const captionInput = document.getElementById("caption");
    const imageInput = document.getElementById("imageFile");
    const uploadButton = document.getElementById("uploadButton");
    const doneButton = document.getElementById("doneButton");
    const statusMessage = document.getElementById("statusMessage");
    const previewContainer = document.getElementById("previewContainer");
    const previewImage = document.getElementById("previewImage");
    const captionPreview = document.getElementById("captionPreview");
    

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        statusMessage.textContent = "";
        statusMessage.className = "hidden";

        const urlParams = new URLSearchParams(window.location.search);

        const productId = urlParams.get("product_id");
        const imageFile = imageInput.files[0];

        if (!imageFile) {
            showError("Please select an image file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("product_id", productId);
        formData.append("media", imageFile);

        try {
            const response = await fetch("/tuckshop/media_upload", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                showSuccess("Image uploaded successfully!");
                updatePreview(imageFile, caption);
                
            } else {
                showError(data.message || "Failed to upload the image.");
            }
        } catch (error) {
            showError("An error occurred while uploading. Please try again.");
            console.error("Upload error:", error);
        }
    });

    function showSuccess(message) {
        statusMessage.textContent = message;
        statusMessage.className = "success";
    }

    function showError(message) {
        statusMessage.textContent = message;
        statusMessage.className = "error";
    }

    function updatePreview(file, caption) {
        const reader = new FileReader();

        reader.onload = (e) => {
            previewImage.src = e.target.result;
            captionPreview.textContent = caption;
            previewContainer.classList.remove("hidden");
            doneButton.classList.remove("hidden");
            uploadButton.classList.add("hidden");
        };

        reader.readAsDataURL(file);
    }
    function toggleUploadButton(show) {
        if (show) {
            uploadButton.classList.remove("hidden");
            doneButton.classList.add("hidden");
        } else {
            uploadButton.classList.add("hidden");
        }
    }

    // Reset form when clicking "Done"
    doneButton.addEventListener("click", () => {
        form.reset();
        previewContainer.classList.add("hidden");
        toggleUploadButton(true); // Show upload button
        statusMessage.className = "hidden"; // Clear status message
    });
});
