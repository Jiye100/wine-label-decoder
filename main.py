from easyOCR import *
import json
import os
import easyocr
import pandas as pd
import fuzzy_match
import decision_tree
import argparse
import shutil
import joblib

Config = json.load(open('./Config.json'))
dashes = '-' * shutil.get_terminal_size().columns

def main():
  # Create a parser
  parser = argparse.ArgumentParser(description="Helpful description on how to use each parameter down below")

  # Add flags
  parser.add_argument('--batch', action='store_true', help='Include the flag to input a folder of labels')
  parser.add_argument('--path', type=str, help='Input the path to the folder from this root directory')
  parser.add_argument('--pytesseract', type=str, help='Insert the path of your pytesseract from your device')
  parser.add_argument('--train', action='store_true', help='Train and save decision tree model')

  # Parse the arguments
  args = parser.parse_args()

  if args.train:
    decision_tree.decision_tree_train()
    print("Done training decision tree")
    return

  if args.pytesseract is None:
    raise Exception("Pytesseract path can't be empty.")

  if args.batch:
    Config["batch_path"] = args.path
    Config["pytesseract_path"] = args.pytesseract

    print(dashes)
    print("Extracting text from images")

    ocr_on_batch_of_images(Config)

    print(dashes)
    print("Performing fuzzy matching")
    prediction = []
    for filename in tqdm(os.listdir(Config['OCR_result']), desc="Extracting text from OCR images"):
        file_path = os.path.join(Config['OCR_result'], filename)
        with open(file_path, 'r') as f:
            text = f.read().splitlines()
        grape, region, country, keyword = fuzzy_match.extract_info(text)
        if len(keyword) == 0:
            keyword.add("Unknown")
        test_label = pd.DataFrame({'grape': [grape], 'region': [region], 'country': [country], 'designation': [list(keyword)[0]]})
        grape_law, region_law, vintage_law = decision_tree.predict_law(test_label)
        prediction.append((grape_law, region_law, vintage_law, grape, country))
    print(dashes)
    print("Generating a description for each wine")
    to_write = open('./result/' + "description.txt", 'w')
    i = 0
    for result in prediction:
        grape_law, region_law, vintage_law, grape, country = result
        grape_law, region_law, vintage_law = grape_law * 100, region_law * 100, vintage_law * 100
        
        to_write.write(f"Image number " + str(i) + "\n")
        if grape_law == region_law == vintage_law == 0:
            to_write.write(f"The grape variety is {grape} and it's from the country {country}\n\n")
        else:
            to_write.write(f"{grape_law}% of the grape must be {grape}, {region_law}% of the grape must come from the stated region, {vintage_law}% of the grape must come from the stated vintage\n\n")
        i += 1
  else:
    status = 'C'
    print("hey")
    while True:
      if status.lower() == 'q' or status.lower() == 'quit':
          break

      # user enters wine label number for now
      img = input("enter wine label:") + ".png"
      img_path = os.path.join('dataset/images',img)

      print("reading images...")
      result = reader.readtext(img_path)
      result = [text[1] for text in result]

      print("extracting information...")
      grape, region, country, keyword = fuzzy_match.extract_info(result)
      designation = ""
      if not region:
          print(f"No specific region found, using country '{country}' as the region.")
          region = country

      print("completed!\n")

      print("result")
      print(result)
      print("grape variety:", grape)
      print("region:", country)

      if country in fuzzy_match.state:
          if region is not None:
              print("AVA:", region)
              designation = "AVA"
          else:
              region = country
              designation = "Country"
      else:
          # International wines check
          if region is None:
              region = country  # Region is just the country
              if country in ["argentina", "chile", "south africa"]:
                  designation = "Country"
              else:
                  designation = "Unknown"  # Fallback, we should catch these
          else:
              # Use specific designations
              if region in fuzzy_match.country_to_region['chile']:
                  designation = "DO"
              elif region in fuzzy_match.country_to_region['argentina']:
                  # Special check for DOC
                  if region in ["luján de cuyo", "san rafael"]:
                      designation = "DOC"
                  else:
                      designation = "IG"
              elif region in fuzzy_match.country_to_region['south africa']:
                  designation = "WO"

      # --- Final fallback if none detected ---
      if designation == '' or designation == 'Unknown':
          if country in ["argentina", "chile", "south africa", "australia", "new zealand"]:
              designation = "Country"
          else:
              designation = "Unknown"  # If it's not recognized

      test_label = pd.DataFrame({'grape': [grape], 'region': [region], 'country': [country], 'designation': [designation]})

      print(f"Debug -> Grape: {grape}, Region: {region}, Country: {country}, Designation: {designation}")

      # test 76
      grape_law, region_law, vintage_law = decision_tree.predict_law(test_label)
      grape_law, region_law, vintage_law = grape_law * 100, region_law * 100, vintage_law * 100
      print(f"{grape_law}% of the grape must be {grape}, {region_law}% of the grape must come from the stated region, {vintage_law}% of the grape must come from the stated vintage")

      # ask user it they want a different input
      status = input("\nType C to continue, Q to Quit")



if __name__ == "__main__":
  main()