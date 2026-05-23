# 🔬 Asbestos Detection via Computer Vision (YOLOv8)

An applied machine learning and computer vision pipeline designed to autonomously detect hazardous asbestos materials in structural imagery. This project implements a custom-trained **YOLOv8** object detection architecture to achieve high-precision, real-time inference, backed by rigorous statistical evaluation.

*Note: This repository contains the architectural implementation, training pipeline, and inference scripts developed as part of original research and algorithm design.*

---

## 🧠 Core Methodology & Architecture

### 1. Object Detection Architecture
* Implemented the **YOLOv8** (You Only Look Once, version 8) framework for its optimal balance of real-time inference speed and detection accuracy.
* Engineered custom data ingestion pipelines to preprocess, normalize, and augment structural imagery for robust model training.
* Designed the inference script to load the saved `.pt` weights and output bounding boxes with confidence thresholds for unseen data.

### 2. Statistical Evaluation & Metrics
To ensure the model is reliable for detecting hazardous materials, it is evaluated beyond simple accuracy. The pipeline calculates:
* **Precision:** Minimizing false positives (incorrectly flagging safe materials).
* **Recall:** Minimizing false negatives (the critical metric of ensuring no asbestos is missed).
* **F1-Score:** Achieving the harmonic mean between precision and recall to handle potential class imbalances in the training data.

---

## 💻 Tech Stack & Libraries

| Domain | Technologies Used |
| :--- | :--- |
| **Model Architecture** | YOLOv8 (Ultralytics) |
| **Language** | Python 3.x |
| **Data Processing** | OpenCV, NumPy, Pandas |
| **Evaluation** | Matplotlib, Scikit-learn (Metrics) |
| **Environment** | Jupyter / Python Virtual Env |

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/aaryamanmodi353-rgb/Asbestos-detection.git](https://github.com/aaryamanmodi353-rgb/Asbestos-detection.git)
cd Asbestos-detection

```

### 2️⃣ Environment Setup

It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

```

### 3️⃣ Running Inference

To run the object detection model on a sample image or directory of images using the pre-trained weights:

```bash
# Example inference command (modify paths as needed)
python detect.py --weights runs/train/exp/weights/best.pt --source data/test_images/

```

### 4️⃣ Model Evaluation

To generate Precision, Recall, and F1-Score metrics on the validation dataset:

```bash
python evaluate.py --data data/dataset.yaml --weights runs/train/exp/weights/best.pt

```

---

## 📈 Research Context & Future Scope

This implementation serves as the technical foundation for a broader research initiative into automated environmental hazard detection. Future iterations of this project aim to:

1. **Edge Deployment:** Optimize the model using TensorRT for deployment on edge devices (e.g., drones or mobile inspection cameras).
2. **Dataset Expansion:** Continuously fine-tune the model with a broader variance of lighting conditions and material degradation states to improve the model's robustness in the field.

```

### Final Prep for Afford Medical:
If you are submitting this alongside your web applications, ensure your GitHub profile pins **Rent Mojo**, **AI Interviewer**, and **Asbestos Detection** right at the top. This trifecta proves you can build complex backends, modern frontends, and implement advanced mathematical algorithms.

```
