import os
import shutil
from tqdm import tqdm

def clean_easyOCRresult_cropped_images_folders(Config):
  for file in tqdm(os.listdir(Config['cropped_sample_result']), desc="Cleaning OCR cropped images result"):
    os.remove(Config['cropped_sample_result']+file)

def clean_easyOCRresult_images(Config):
  for file in tqdm(os.listdir(Config['images_result']), desc="Cleaning OCR normal images result"):
    os.remove(Config['images_result']+file)

def clean_OCR_result_folder(Config):
  for file in tqdm(os.listdir(Config['OCR_result']), desc="Cleaning images result"):
    os.remove(Config['OCR_result']+file)