document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    
    const uploadSection = document.getElementById("upload-section");
    const loadingSection = document.getElementById("loading-section");
    const resultSection = document.getElementById("result-section");
    
    const resultImage = document.getElementById("result-image");
    const btnReset = document.getElementById("btn-reset");
    const badge = document.getElementById("detection-badge");

    // File Drop Handlers
    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length) {
            handleFile(fileInput.files[0]);
        }
    });

    btnReset.addEventListener("click", () => {
        resultSection.classList.add("hidden");
        uploadSection.classList.remove("hidden");
        fileInput.value = ""; // Reset input
    });

    function handleFile(file) {
        if (!file.type.startsWith("image/")) {
            alert("Please upload a valid image file.");
            return;
        }

        // Show loading
        uploadSection.classList.add("hidden");
        loadingSection.classList.remove("hidden");

        const formData = new FormData();
        formData.append("file", file);

        // Upload to FastAPI Backend
        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server error/Prediction failed.");
            }
            return response.json();
        })
        .then(data => {
            // Hide loading, show results
            loadingSection.classList.add("hidden");
            resultSection.classList.remove("hidden");

            // Set Image payload
            resultImage.src = "data:image/jpeg;base64," + data.image;

            // Update badge text based on detections
            if (data.count > 0) {
                badge.textContent = `${data.count} Asbestos Component(s) Found!`;
                badge.className = "badge badge-danger";
            } else {
                badge.textContent = `Safe - 0 Detections`;
                badge.className = "badge badge-success";
            }
        })
        .catch(err => {
            console.error(err);
            alert("An error occurred during inference. Check console.");
            // Reset UI
            loadingSection.classList.add("hidden");
            uploadSection.classList.remove("hidden");
        });
    }
});
