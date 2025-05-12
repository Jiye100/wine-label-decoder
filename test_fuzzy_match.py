from PIL import Image
import fuzzy_match
import os
#with open('fuzzy_match_expected.txt', 'r') as expect:
#    content = expect.read()
#with open('fuzzy_match_expected.txt', 'w') as expect:
#    expect.write(content.lower())

f = open('fuzzy_match_result.txt', 'w')

for idx in range(1, 77):
    filename = f'img{idx}_result.txt'
    txt_path = os.path.join('easyOCRresult_images', filename)
    f.write(f"img{idx}\n")
    with open(txt_path, 'r') as file:
        result = file.read().splitlines()


    best_grape, best_region, best_country, keywords = fuzzy_match.extract_info(result)

    # f.write(f"Grape: {best_grape} ({grape_score}% with {grape_matching})\n")
    f.write(f"grape: {best_grape}\n")
    if best_region is not None:
    # f.write(f"Region: {best_region} ({region_score}% with {region_matching})\n")
        f.write(f"region: {best_region}\n")
    if best_country is not None:
        f.write(f"country: {best_country}\n")

    if len(keywords) > 0:
        f.write("keyword:")
        for keyword in keywords:
            if keyword == 'd.o.' and best_country != 'chile':
                continue
            f.write(f" {keyword}")
        f.write("\n")
    # f.write(f"Country/State: {best_country} ({country_score}% with {country_matching})\n")
    f.write("\n")

    print(f"{filename} completed\n")