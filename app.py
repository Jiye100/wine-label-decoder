# ask user for input image
import os
import easyocr
import pandas as pd
import fuzzy_match
import decision_tree

reader = easyocr.Reader(['en'])

# user enters wine label number for now
img = input("enter wine label:") + ".png"
img_path = os.path.join('dataset/images',img)

print("reading images...")
result = reader.readtext(img_path)

result = [text[1] for text in result]


# find country
print("finding region...")
country = fuzzy_match.fuzzy_matching_country(result)[0]
region = ''
designation = ''

# if country is not found (guess country by region) or US wine (need to find AVA)
if country is None or country in fuzzy_match.state:
    region = fuzzy_match.fuzzy_matching_regions(result)[0]

    # check if state wine (AVA does not match state)
    if country in fuzzy_match.state and region not in fuzzy_match.country_to_region[country]:
        region = None
    else:
        # find country using region
        for candidate in fuzzy_match.country_to_region.keys():
            if region in fuzzy_match.country_to_region[candidate]:
                country = candidate
                break

# If no specific region found, use the country as the region
if not region:
    print(f"No specific region found, using country '{country}' as the region.")
    region = country

# find grape variety
print("finding grapes...")
grape = fuzzy_match.fuzzy_matching_grapes(result, country)[0]
print(result)
print("completed!\n")

print("result")
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