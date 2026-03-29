document.addEventListener("DOMContentLoaded", () => {
    const glassPanel = document.getElementById("glass-panel");
    const glare = document.getElementById("glare");

    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    
    // Using the new active-class logic for sections
    const uploadSection = document.getElementById("upload-section");
    const loadingSection = document.getElementById("loading-section");
    const resultSection = document.getElementById("result-section");
    
    const resultImage = document.getElementById("result-image");
    const btnReset = document.getElementById("btn-reset");
    const badge = document.getElementById("detection-badge");

    /**
     * =========================================
     * 3D Card Tilt & Glare Effect
     * =========================================
     */
    const THRESHOLD = 15; // Max tilt rotation in degrees

    glassPanel.addEventListener('mousemove', (e) => {
        const { clientX, clientY } = e;
        const { clientWidth, clientHeight, offsetLeft, offsetTop } = glassPanel;
        const rect = glassPanel.getBoundingClientRect();
        
        // Calculate mouse position relative to the element (center is 0,0)
        const xPos = clientX - rect.left;
        const yPos = clientY - rect.top;

        // Calculate rotation angles
        const centerX = clientWidth / 2;
        const centerY = clientHeight / 2;
        const rotateX = ((yPos - centerY) / centerY) * -THRESHOLD;
        const rotateY = ((xPos - centerX) / centerX) * THRESHOLD;

        // Apply 3D Transform
        glassPanel.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        
        // Move Glare Highlight
        glare.style.transform = `translate(${xPos - (clientWidth*1.25)}px, ${yPos - (clientHeight*1.25)}px)`;
    });

    glassPanel.addEventListener('mouseleave', () => {
        // Reset transform & glare smoothly when mouse leaves
        glassPanel.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        glare.style.opacity = '0';
    });

    glassPanel.addEventListener('mouseenter', () => {
        glare.style.opacity = '1';
    });

    /**
     * =========================================
     * Logic: View Transitions & API Handling
     * =========================================
     */
    function switchSection(activeSection) {
        // Remove active class from all
        uploadSection.classList.remove("active");
        loadingSection.classList.remove("active");
        resultSection.classList.remove("active");

        // Add to the chosen one
        activeSection.classList.add("active");
    }

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
        switchSection(uploadSection);
        fileInput.value = ""; // Reset input container
    });

    function handleFile(file) {
        if (!file.type.startsWith("image/")) {
            alert("Please upload a valid image file.");
            return;
        }

        // Smoothly Transition to loading
        switchSection(loadingSection);

        const formData = new FormData();
        formData.append("file", file);

        // Upload to FastAPI Backend
        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server error / API prediction failed.");
            }
            return response.json();
        })
        .then(data => {
            // Set Image payload
            resultImage.src = "data:image/jpeg;base64," + data.image;

            // Update badge text and aesthetic based on detections
            if (data.count > 0) {
                badge.textContent = `${data.count} Asbestos Component(s) Found`;
                badge.className = "badge badge-danger";
            } else {
                badge.textContent = `Safe - Clean Sample`;
                badge.className = "badge badge-success";
            }

            // Reveal Result UI
            switchSection(resultSection);
        })
        .catch(err => {
            console.error("Inference Error:", err);
            alert("An error occurred during inference. Check connection.");
            // Revert on failure
            switchSection(uploadSection);
        });
    }
});
