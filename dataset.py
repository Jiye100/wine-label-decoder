import easyocr
import os

# Use pre-trained model to extract bounding boxes from the wine label images
# Record extracted text and bounding boxes in pretrained.txt
# Review pretrained.txt and manually correct any mistakes. The corrected label will be recorded in labels.txt
# labels.txt will be used for fine-tuning the OCR model

# Initialize EasyOCR reader (added English, French, Spanish, German, Italian, Portuguese)
reader = easyocr.Reader(['en', 'fr', 'es', 'de', 'it', 'pt'])

image_folder = 'dataset\images'
output_file = 'dataset\pretrained.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for i in range(0, 129):
        results = reader.readtext(f'dataset\images\img{i}.png', paragraph = True) # what about detail?

        for (bbox, text) in results:
            x1, y1 = map(int, bbox[0])
            x2, y2 = map(int, bbox[2])
            f.write(f"img{i}\t{text}\t{x1} {y1} {x2} {y2}\n")
        print(f"Label{i} completed")