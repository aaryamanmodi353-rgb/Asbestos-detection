import json

# This script generates a Jupyter Notebook (.ipynb) for YOLOv11 training
# customized for your asbestos dataset.

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🏗️ YOLOv11 Training Notebook - Asbestos Detection\n",
    "\n",
    "This notebook implements the pipeline to train a YOLOv11 model on your custom asbestos dataset.\n",
    "\n",
    "### Prerequisites\n",
    "* Ensure your `data.yaml` file is configured correctly.\n",
    "* Ensure your dataset images are organized in `train`, `valid`, and `test` folders."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Install Ultralytics\n",
    "We install the official library which includes YOLOv8 and YOLOv11."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "%pip install ultralytics"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Import Libraries & Setup\n",
    "Load the necessary modules and check for GPU availability."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from ultralytics import YOLO\n",
    "import os\n",
    "import torch\n",
    "\n",
    "# Check if GPU is available\n",
    "print(f\"Setup complete. Using GPU: {torch.cuda.is_available()}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Define Dataset Path\n",
    "**ACTION REQUIRED:** Update the `data_yaml_path` variable below to point to your specific `data.yaml` file."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# REPLACE THIS PATH with the actual path to your data.yaml file\n",
    "# Example: \"C:/Users/You/Downloads/Asbestos_Dataset/data.yaml\"\n",
    "data_yaml_path = \"path/to/your/asbestos/dataset/data.yaml\"\n",
    "\n",
    "if not os.path.exists(data_yaml_path):\n",
    "    print(f\"⚠️ WARNING: File not found at {data_yaml_path}. Please check the path.\")\n",
    "else:\n",
    "    print(f\"✅ Dataset found at {data_yaml_path}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Load and Train Model\n",
    "We load the **YOLOv11 Nano** (`yolo11n.pt`) model for a balance of speed and accuracy. \n",
    "\n",
    "* `epochs`: Number of training cycles (100 is a good start).\n",
    "* `imgsz`: Image resolution (640 is standard).\n",
    "* `batch`: Adjust this if you run out of memory (try 8 or 16)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load the pre-trained YOLOv11 model\n",
    "model = YOLO(\"yolov11n.pt\") \n",
    "\n",
    "# Start Training\n",
    "results = model.train(\n",
    "    data=data_yaml_path,\n",
    "    epochs=100, \n",
    "    imgsz=640,\n",
    "    batch=16,\n",
    "    name='yolov11_asbestos',\n",
    "    device=0 if torch.cuda.is_available() else 'cpu' # Use GPU if available\n",
    ")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Validate the Model\n",
    "Evaluate the model's performance on the validation/test set to check for accuracy (mAP)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Validate the best model from the training run\n",
    "metrics = model.val(split='test')\n",
    "\n",
    "print(f\"Mean Average Precision (mAP50-95): {metrics.box.map:.4f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Run Inference (Test Prediction)\n",
    "Test the trained model on a specific image to see the bounding boxes."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# REPLACE with a path to an image from your test set\n",
    "test_image = \"path/to/your/test/image.jpg\"\n",
    "\n",
    "if os.path.exists(test_image):\n",
    "    results = model.predict(\n",
    "        source=test_image,\n",
    "        save=True,\n",
    "        conf=0.5  # Confidence threshold\n",
    "    )\n",
    "    print(\"Prediction saved!\")\n",
    "else:\n",
    "    print(\"Test image not found. Please update the path.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

# Write to file
filename = "yolo_training.ipynb"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print(f"Successfully created '{filename}'!")