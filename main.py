from ultralytics import YOLO
import os

def main():
    # --- 1. Load a Pre-trained Model ---
    
    # We'll use YOLOv11n (nano), which is small and fast.
    # For YOLOv8, simply change this to: model = YOLO("yolov8n.pt")
    model = YOLO("yolov11n.pt")  #

    # You can also use a model built from scratch
    # model = YOLO("yolov11n.yaml") 

    print("Model loaded.")

    # --- 2. Define Your Dataset ---
    
    # !! IMPORTANT: Change this path to point to your 'data.yaml' file !!
    data_yaml_path = r"path/to/your/asbestos/dataset/data.yaml"

    if not os.path.exists(data_yaml_path):
        print(f"Error: 'data.yaml' file not found at {data_yaml_path}")
        print("Please download your dataset from Roboflow and update the path.")
        return

    # --- 3. Train the Model ---
    
    print("Starting model training...")
    # This will train the model, validate it, and save the best version.
    results = model.train(
        data=data_yaml_path,
        epochs=100,         # Number of times to loop over the dataset (start with 100)
        imgsz=640,          # Image size (640 is standard for this dataset)
        batch=16,           # Adjust based on your GPU memory (lower if you get errors)
        name='yolov11n_asbestos_detector' # Name of the output folder
    )
    
    print("Training complete.")

    # --- 4. Validate the Best Model ---
    
    # The 'results.save_dir' contains the path to the 'runs' folder
    # where your best model is saved (e.g., 'runs/detect/yolov11n_asbestos_detector/weights/best.pt')
    
    # You can also validate manually on the 'test' split
    print("Validating model on the test set...")
    best_model_path = os.path.join(results.save_dir, 'weights', 'best.pt')
    
    # Load the best model you just trained
    best_model = YOLO(best_model_path)
    
    # Run validation
    metrics = best_model.val(split='test')
    print("--- Test Set Metrics ---")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"mAP50: {metrics.box.map50:.4f}")
    print("-------------------------")

    # --- 5. Run a Prediction ---
    
    print("Running prediction on a test image...")
    # Find an image to test (replace with a real image path from your test set)
    # This is just an example path
    test_image_path = "path/to/your/asbestos/dataset/test/images/some_image.jpg"

    if os.path.exists(test_image_path):
        predict_results = best_model.predict(
            source=test_image_path,
            save=True,     # Save the image with bounding boxes
            conf=0.5       # Confidence threshold (don't show boxes below 50%)
        )
        print(f"Prediction saved to: {predict_results[0].save_dir}")
    else:
        print(f"Test image not found at {test_image_path}, skipping prediction demo.")

if __name__ == "__main__":
    main()