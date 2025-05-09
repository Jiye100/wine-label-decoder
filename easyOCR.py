import easyocr
import os
from fileManagement import *
from tqdm import tqdm
reader = easyocr.Reader(['en'])


def ocr_on_cropped_sample(Config):
  clean_easyOCRresult_cropped_images_folders(Config)
  for file in tqdm(os.listdir(Config['cropped_images']), desc="Extracting text from cropped images"):
    if not file.lower().endswith(('.png')):
      continue
    filename = file.rsplit( ".", 1 )[0]
    to_write_ocr=open(Config['cropped_sample_result'] + filename + "_result.txt",'w')
    ocr_results = reader.readtext(Config['cropped_images'] + file)
    for bbox, text, conf in ocr_results:
      to_write_ocr.write(f"{text}\n")

def ocr_on_images(Config):
  clean_easyOCRresult_images(Config)
  for file in tqdm(os.listdir(Config['dataset_images']), desc="Extracting text from normal images"):
    if not file.lower().endswith(('.png')):
      continue
    filename = file.rsplit( ".", 1 )[0]
    to_write_ocr=open(Config['images_result'] + filename + "_result.txt",'w')
    ocr_results = reader.readtext(Config['dataset_images'] + file)
    for bbox, text, conf in ocr_results:
      to_write_ocr.write(f"{text}\n")