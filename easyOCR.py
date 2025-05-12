import easyocr
import os
from fileManagement import *
from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image
import pytesseract
from collections import Counter
from thefuzz import fuzz
from thefuzz import process

reader = easyocr.Reader(['en'])

#Replace with your tesseract
pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"
# pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"

def extract_text(file):

  #Apply a bunch of filter to feature text in different lighting
  img = cv2.imread(file)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  adapt_gau = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
  gau_blur = cv2.GaussianBlur(gray, (5, 5), 0)
  filters = {
      "Original": img,
      "Gray": gray,
      "Global Binary": cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1],
      "Binary Inv": cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1],
      "Trunc": cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)[1],
      "ToZero": cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)[1],
      # "Adaptive Mean": cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                            # cv2.THRESH_BINARY, 11, 2),
      # "Adaptive Gaussian": adapt_gau,
      "Otsu": cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
      "Gaussian Blur": gau_blur
      # "Filtered (Blur+Thresh)": cv2.adaptiveThreshold(gau_blur, 255, adapt_gau),
  }

  # Performing OCR
  all_text = []
  for name, img in filters.items():
    try:
      if len(img.shape) == 2:
          img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
      else:
          img_color = img

      text_tess = pytesseract.image_to_string(img_color)
      text_easy = " ".join([line[1] for line in reader.readtext(img_color)])
      
      all_text.extend(text_tess.split('\n'))
      all_text.extend(text_easy.split('\n'))
    except Exception as e:
      print(f"Error with {name}: {e}")

  # Deduplicate lines using fuzzy matching
  unique_lines = []
  for line in all_text:
    line = line.strip()
    if not any(fuzz.ratio(line, existing) > 50 for existing in unique_lines):
      unique_lines.append(line)

  # Reconstruct original label attempt
  final_label_text = "\n".join(unique_lines)
  return final_label_text

def ocr_on_cropped_sample(Config):
  clean_easyOCRresult_cropped_images_folders(Config)
  for file in tqdm(os.listdir(Config['cropped_images']), desc="Extracting text from cropped images"):
    if not file.lower().endswith(('.png')):
      continue
    filename = file.rsplit( ".", 1 )[0]
    to_write_ocr=open(Config['cropped_sample_result'] + filename + "_result.txt",'w')
    text = extract_text(Config['cropped_images']+file)
    to_write_ocr.write(f"{text}")

def ocr_on_images(Config):
  clean_easyOCRresult_images(Config)
  for file in tqdm(os.listdir(Config['dataset_images']), desc="Extracting text from normal images"):
    if not file.lower().endswith(('.png')):
      continue
    filename = file.rsplit( ".", 1 )[0]
    to_write_ocr=open(Config['images_result'] + filename + "_result.txt",'w')
    text = extract_text(Config['dataset_images']+file)
    to_write_ocr.write(f"{text}")