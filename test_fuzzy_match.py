import easyocr
from PIL import Image
import fuzzy_match
import os

f = open('fuzzy_match_result.txt', 'w')

reader = easyocr.Reader(['en'])

for filename in os.listdir('dataset\images'):
    img_path = os.path.join('dataset\images', filename)
    result = reader.readtext(img_path)

    f.write(filename + "\n")
    for (_, text, _) in result:
        f.write(text + "\n")

    f.write("\n")

    best_country, country_score, country_matching  = fuzzy_match.fuzzy_matching_country(result)
    best_region, region_score, region_matching = None, None, None

    # if country is not found or us wine (need to find AVA)
    if best_country is None or best_country in fuzzy_match.state:
        best_region, region_score, region_matching = fuzzy_match.fuzzy_matching_regions(result)
        # check if state wine (AVA does not match state)
        if best_country in fuzzy_match.state and best_region not in fuzzy_match.country_to_region[best_country]:
            best_region = None
        else:
            # find country using region
            for candidate in fuzzy_match.country_to_region.keys():
                if best_region in fuzzy_match.country_to_region[candidate]:
                    f.write("Country found by region\n")
                    best_country = candidate
                    break

    # find grape variety
    best_grape, grape_score, grape_matching = fuzzy_match.fuzzy_matching_grapes(result, best_country)

    f.write(f"Grape: {best_grape} ({grape_score}% with {grape_matching})\n")
    if best_region is not None:
        f.write(f"Region: {best_region} ({region_score}% with {region_matching})\n")
    f.write(f"Country/State: {best_country} ({country_score}% with {country_matching})\n")
    f.write("\n")

    print(f"{filename} completed")