import easyocr
import os
import json

with open(r'dataset\via_annotation.json', 'r') as f:
    via_data = json.load(f)

annotations = []

for _, data in via_data.items():
    regions = data['regions']
    boxes = []
    texts = []


    for region in regions:
        shape = region['shape_attributes']
        x, y, w, h = shape['x'], shape['y'], shape['width'], shape['height']
        text = region['region_attributes']['text']

        boxes.append([x, y, x + w, y + h])
        texts.append(text)

    annotations.append({'image' :data['filename'], 'boxes': boxes, 'text': texts})
    print(f"{data['filename']} completed")

with open('annotation.json', 'w') as f:
    json.dump(annotations, f, indent=2)

print("Annotation saved")