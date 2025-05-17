from PIL import Image
import fuzzy_match
import os

def run_fuzzy_match():
    f= open('fuzzy_match_example.txt', 'w')

    for idx in range(1, 77):
        filename = f'img{idx}_result.txt'
        txt_path = os.path.join('easyOCRresult_images', filename)
        f.write(f"img{idx}\n")
        with open(txt_path, 'r', encoding="utf-8") as file:
            result = file.read().splitlines()


        best_grape, best_region, best_country, keywords = fuzzy_match.extract_info(result)

        # f.write(f"Grape: {best_grape} ({grape_score}% with {grape_matching})\n")
        f.write(f"grape: {best_grape}\n")
        if best_region is not None:
        # f.write(f"Region: {best_region} ({region_score}% with {region_matching})\n")
            f.write(f"region: {best_region}\n")
        else:
            f.write("region:\n")
        if best_country is not None:
            f.write(f"country: {best_country}\n")
        else:
            f.write(f"country:\n")

        f.write("keyword:")
        if len(keywords) > 0:
            for keyword in sorted(keywords):
                if keyword == 'd.o.' and best_country != 'chile':
                    continue
                f.write(f" {keyword}")
        f.write("\n")
        # f.write(f"Country/State: {best_country} ({country_score}% with {country_matching})\n")
        f.write("\n")

        print(f"{filename} completed\n")

def evaluate_fuzzy_match():
    incorrects = 0
    with open('fuzzy_match_expected.txt', 'r') as f1, open('fuzzy_match_example.txt', 'r') as f2:
        expected_lines = f1.readlines()
        actual_lines = f2.readlines()

        max_lines = max(len(expected_lines), len(actual_lines))

        for i in range(max_lines):
            expected_line = expected_lines[i].rstrip() if i < len(expected_lines) else "<no line>"
            actual_line = actual_lines[i].rstrip() if i < len(actual_lines) else "<no line>"

            if expected_line != actual_line:
                incorrects += 1
                print(f"Line {i+1}:\n  Expected: {expected_line}\n  Actual:   {actual_line}\n")

        print(f"Result: {incorrects} out of {max_lines} incorrect")

run_fuzzy_match()
evaluate_fuzzy_match()