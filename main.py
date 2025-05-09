from easyOCR import *
import json


Config = json.load(open('./Config.json'))

def main():
  ocr_on_cropped_sample(Config)
  ocr_on_images(Config)

if __name__ == "__main__":
  main()