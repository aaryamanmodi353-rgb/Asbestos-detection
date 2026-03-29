import json

with open('yolo_training.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            line = line.replace('yolov8n.pt', 'yolov11s.pt')
            line = line.replace('epochs=200', 'epochs=300')
            line = line.replace('yolov11_fast_highres', 'yolov11s_fast_highres')
            new_source.append(line)
        cell['source'] = new_source

with open('yolo_training.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
