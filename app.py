# ask user for input image
import os
import easyocr
import pandas as pd
import fuzzy_match
import decision_tree

reader = easyocr.Reader(['en'])

def main():
    status = 'C'
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