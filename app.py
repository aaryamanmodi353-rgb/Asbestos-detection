import os
import cv2
import base64
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from ultralytics import YOLO

app = FastAPI(title="Asbestos Detection API", description="AI-powered asbestos detection")

# Locate the best model or fallback
MODEL_PATH = os.path.join("runs", "detect", "yolov11_fast_highres2", "weights", "best.pt")
if not os.path.exists(MODEL_PATH):
    # Fallback to base model for demo
    MODEL_PATH = "yolo11n.pt"

print(f"Loading model from {MODEL_PATH}...")
model = YOLO(MODEL_PATH)

# Ensure the static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
             raise HTTPException(status_code=400, detail="Invalid image file.")

        # Run inference
        results = model.predict(img, conf=0.25)
        
        # Plot detections on image
        annotated_img = results[0].plot()

        # Encode image to base64
        _, buffer = cv2.imencode('.jpg', annotated_img)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        
        # Extract basic detection counts for the UI summary
        detections = len(results[0].boxes)

        return {
            "image": encoded_image,
            "message": "Detection successful",
            "count": detections
        }

    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
