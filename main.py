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
    # TODO
    # Should we split decision tree to train and predict? or we gonna train everytime right before predict?
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
    grape_list = []
    region_list = []
    country_list = []
    designation_list = []
    for file in tqdm(os.listdir(Config['OCR_result']), desc="Extracting text from OCR images"):
        # TODO
        # Convert each text into valid word and then create a pandas table to put in decision tree
        text = []
        for line in file:
            text.append(line.strip())
    
    test_label = pd.DataFrame({'grape': grape_list, 'region': region_list, 'country': country_list, 'designation': designation_list})
    
    # Load the trained model
    model = joblib.load('models/decision_tree_model.pkl')
    prediction = model.predict(test_label)

    print(dashes)
    print("Generating a description for each wine")
    to_write = open('./result/' + "description.txt", 'w')
    for result in prediction:
        grape_law, region_law, vintage_law = decision_tree.predict_law(test_label)
        grape_law, region_law, vintage_law = grape_law * 100, region_law * 100, vintage_law * 100
        to_write.write(f"Image number " + {i} + "\n")
        to_write.write(f"{grape_law}% of the grape must be {grape}, {region_law}% of the grape must come from the stated region, {vintage_law}% of the grape must come from the stated vintage\n")
        # TODO need a name and a region
        generated_text = generate_wine_description(name, region)
        to_write.write(generated_text + "\n\n")

    print("worked")
    return
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