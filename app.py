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

# find grape variety
print("finding grapes...")
grape = fuzzy_match.fuzzy_matching_grapes(result, country)[0]

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

test_label = pd.DataFrame({'grape': [grape], 'region': [region], 'country': [country], 'designation': [designation]})

# test 76
grape_law, region_law, vintage_law = decision_tree.predict_law(test_label)
grape_law, region_law, vintage_law = grape_law * 100, region_law * 100, vintage_law * 100

print(f"{grape_law}% of the grape must be {grape}, {region_law}% of the grape must come from the stated region, {vintage_law}% of the grape must come from the stated vintage")