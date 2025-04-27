# ask user for input image
import os
import easyocr
import fuzzy_match

reader = easyocr.Reader(['en'])

# user enters wine label number for now
img = input("enter wine label:") + ".png"
img_path = os.path.join('dataset\images',img)

print("reading images...")
result = reader.readtext(img_path)

# find country
print("finding region...")
country = fuzzy_match.fuzzy_matching_country(result)

# if country is not found (guess country by region) or US wine (need to find AVA)
if country is None or country in fuzzy_match.state:
    region = fuzzy_match.fuzzy_matching_regions(result)

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
grape = fuzzy_match.fuzzy_matching_grapes(result, country)

print("completed!\n")

print("result")
print("grape variety:", grape)
print("region:", country)

if country in fuzzy_match.state and region is not None:
    print("AVA:", region)