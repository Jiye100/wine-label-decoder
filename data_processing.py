from datasets import load_dataset
from PIL import Image
import easyocr
import numpy as np

ds = load_dataset("Francesco/wine-labels")
reader = easyocr.Reader(['en'])

# Take first 300 labels in training set
for idx in range(300):
    data = ds['train'][idx]
    img = data['image'].convert('RGB')
    img_path = f'dataset/wine_labels/label{idx + 1}.png'
    img.save(img_path, format='PNG')

    image = Image.open(img_path)
    bboxes = data['objects']['bbox']

    for i, bbox in enumerate(bboxes):
        # Define boundary box
        region = (bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3])

        cropped_image = image.crop(region)
        result = reader.readtext(np.array(cropped_image), detail = 0)

        # If the boundary box contains text, crop and save
        if result and any(len(text.strip()) for text in result):
            cropped_image.save(f'dataset/cropped_images/image{idx+1}.{i}.png', format = 'PNG')
    
    print(f"Successfully saved label{idx+1}!")