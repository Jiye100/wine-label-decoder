from rapidfuzz import process, fuzz
import string

# using rapidfuzz instead of fuzzywuzzy because it's faster

# grape variety
grape_variety = ['pinotage',
                 'cabernet sauvignon',
                 'pinot noir',
                 'sauvignon blanc',
                 'malbec',
                 'riesling',
                 'chardonnay',
                 'carmenere',
                 'torrentes', 
                 'pinot gris', 
                 'syrah', 
                 'chenin blanc', 
                 'merlot',
                 'zinfandel',
                 'cabernet franc',
                 'viognier',
                 'shiraz',
                 'bonarda',
                 'semillon',
                 'muscat',
                 'muscadet',
                 'gewurztraminer',
                 'gamay',
                 'cabernet',
                 'sauvignon'
                ]

regions = ["columbia valley", "yakima valley", "walla walla valley", "red mountain", "horse heaven hills",
           "willamette valley", "dundee hills", "yamhill-carlton", "mcminnville", "ribbon ridge", "chehalem mountains", "umpqua valley", "rogue valley", "applegate valley",
           "finger lakes", "cayuga lake", "seneca lake", "north fork of long island", "hamptons", "hudson river region", "lake erie",
           "napa", "napa valley", 'sonoma valley', 'russian river valley', 'alexander valley', 'sonoma county','mendocino','santa barbara county','monterey county','paso robles',
           "mendoza", "san juan", "salta", "la rioja", "catamarca",
           "marlborough", "martinborough", "central otago",
           "western cape", "stellenbosch", "simonsberg",
           "elqui valley", "limari valley", "aconcagua", "maipo valley", "cachapoal valley", "colchagua valley", "maule valley",
           "hunter valley", "yarra valley", "adelaide hills", "barossa valley", "clare valley", "mclaren vale", "margaret river", "rutherglen", "coonawarra", "mornington peninsula", "tasmania",
           "nantais", "anjou", "savennieres", "saumur", "touraine", "sancerre", "pouilly-fume", "reuilly", "quincy", "vouvray", "chinon", "bourgueil"
           ]

country_to_region = {
    "california": ["napa valley", 'sonoma valley', 'russian river valley', 'alexander valley', 'sonoma county','mendocino','santa barbara county','monterey county','paso robles'],
    "washington": ["columbia valley", "yakima valley", "walla walla valley", "red mountain", "horse heaven hills"],
    "new york": ["finger lakes", "cayuga lake", "seneca lake", "north fork of long island", "hamptons", "hudson river region", "lake erie"],
    "oregon": ["willamette valley", "dundee hills", "yamhill-carlton", "mcminnville", "ribbon ridge", "chehalem mountains", "umpqua valley", "rogue valley", "applegate valley"],
    "argentina": ["mendoza", "san juan", "salta", "la rioja", "catamarca"],
    "new zealand": ["marlborough", "martinborough", "central otago"],
    "south africa": ["western cape", "stellenbosch", "simonsberg"],
    "chile": ["elqui valley", "limari valley", "aconcagua", "maipo valley", "cachapoal valley", "colchagua valley", "maule valley"],
    "australia": ["hunter valley", "yarra valley", "adelaide hills", "barossa valley", "clare valley", "mclaren vale", "margaret river", "rutherglen", "coonawarra", "mornington peninsula", "tasmania", "geographe"]
}

possible_keywords = ["estate", "e$tate", "reserva", "d.o", "d.0", "d,o", "d,0", "sur lie"
                    #  "vins de france", "igp", "i.g.p", "indication geographique protegee", "aoc", "appellation d'origine controlee".
                    #  "cremant", "saumur brut", "montlouis sur loire", "anjou mousseux", "touraine mousseux", "vouvray", "grand cru",
                    #  "vendanges tardives", "selection de grains nobles", "gentil", "edelzwicker"
                     ]
translator = str.maketrans('', '', string.punctuation)
keyword = {"estate": "estate", 
           "e$tate": "estate",
           "reserve": "reserve",
           "reserva": "reserve",
           "d.o": "d.o.",
           "d.0": "d.o.",
           "d,o": "d.o.",
           "d,0": "d.o.",
           "sur lie": "sur lie"
           }

region_to_country = {region: country for country in country_to_region.keys() for region in country_to_region[country]}

# country or states
country_state = ["california", "oregon", "new york", "washington", "south africa", "argentina", "new zealand", "chile", "australia", "loire", "alsace"]
state = ['california', 'oregon', 'new york', 'washington']

# common error words that should be ignored
common_error = ['vineyard', 'region', 'valley', 'hills', 'vineyards', 'hill']

# fuzzy matching for grape varieties
def fuzzy_matching_grapes(result, country=None):
    best_match = None
    matching_text = None
    best_score = 0 # no threshold

    cabernet, sauvignon = False, False

    for text in result:
        text = text.lower()

        # ignore common errors or short text
        if text in common_error or len(text) < 4:
            continue

        # find the best match
        choice, score, _ = process.extractOne(text, grape_variety)

        if choice == 'cabernet' and score > 85:
            cabernet = True
        elif choice == 'sauvignon':
            sauvignon = True
        elif best_score < score:
            best_match = choice
            best_score = score
            matching_text = text

        if cabernet and sauvignon:
            best_match = 'cabernet sauvignon' 
            break
        elif sauvignon:
            best_match = 'sauvignon blanc'
            break
        elif cabernet:
            best_match = 'cabernet franc'
            break
        
    #     # torrentes is argentina's signature grape (unlikely to be seen if region is not argentina)
    #     if country != 'argentina' and choice == 'torrentes':
    #         continue

    #     # pinotage is south africa's signature grape (unlikely to be seen if region is not south africa)
    #     if country != 'south africa' and choice == 'pinotage':
    #         continue

    #     # compute Levenshtein Distance similarity ratio between two strings
    #     ratio_score = fuzz.ratio(choice, text)
    #     token_set_score = fuzz.token_set_ratio(choice, text)

    #     if best_score < token_set_score:
    #         best_match = choice
    #         best_score = token_set_score
    #         matching_text = text
    #     elif best_score < ratio_score:
    #         best_match = choice
    #         best_score = ratio_score
    #         matching_text = text


    return best_match, best_score, matching_text

def fuzzy_matching_regions(result):
    best_match = None
    best_score = 60 # threshold of 60
    matching_text = None

    for text in result:
        text = text.lower()

        # ignore common errors or grape varieties or short text
        if text in common_error or text in grape_variety or len(text) < 4:
            continue

        # find best match using token set ratio and partial ratio
        token_choice, token_score, _ = process.extractOne(text, regions, scorer=fuzz.token_set_ratio)
        partial_choice, partial_score, _ = process.extractOne(text.replace(' ', ''), regions, scorer=fuzz.partial_ratio)
        choice, score = None, 0
        # print("text:", text)
        # print("token scoring:", token_choice, token_score)
        # print("partial scoring:", partial_choice, partial_score, "\n")
        if token_score < partial_score:
            choice, score = partial_choice, partial_score
        else:
            choice, score = token_choice, token_score

        # short tokens need to have higher threshold
        if choice == 'salta':
            if score > 90:
                best_match = choice
                best_score = score
                matching_text = text
            continue

        if choice == 'napa':
            if score == 100:
                best_match = 'napa valley'
                best_score = score
                matching_text = text
                break

        if best_score < score:
            best_match = choice
            best_score = score
            matching_text = text


    return best_match, best_score, matching_text

def fuzzy_matching_country(result):
    best_match = None
    best_score = 60 # threshold of 60
    matching_text = None

    for text in result:
        text = text.lower()

        # ignore common errors or grape varieties or short text
        if text in common_error or text in grape_variety or len(text) < 4:
            continue

        # find best match
        choice, _, _ = process.extractOne(text, country_state)

        # compute Levenshtein Distance similarity ratio between two strings
        ratio_score = fuzz.ratio(choice, text)

        # OCR can read countries/states with high accuracy
        partial_token_set_score = fuzz.token_set_ratio(choice, text)

        # check if Levenshtein Distance similarity ratio between two strings is higher
        if partial_token_set_score == 100:
            best_match = choice
            best_score = partial_token_set_score
            matching_text = text
            break
        elif best_score < ratio_score:
            best_match = choice
            best_score = ratio_score
            matching_text = text
    
    return best_match, best_score, matching_text

def fuzzy_matching_keyword(result):
    scores = set()
    threshold = 85
    for text in result:
        text = text.lower()

        # ignore short words
        if len(text) < 4:
            continue

        token_choice, token_score, _ = process.extractOne(text, possible_keywords, scorer=fuzz.partial_token_set_ratio)
        partial_choice, partial_score, _ = process.extractOne(text.replace(' ', ''), possible_keywords, scorer=fuzz.partial_ratio)

        if token_score < partial_score:
            choice, score = keyword[partial_choice], partial_score
        else:
            choice, score = keyword[token_choice], token_score

        # print("text", text)
        # print("choice", choice, f"({score})")

        if choice == 'd.o.':
            # only add D.O. to keyword when it's 100% certain (tends to get higher similarity score because it's short)
            if score == 100:
                scores.add(choice)
            continue

        # ignore if similarity score is high because of the word 'state'
        if choice == 'estate' and score < fuzz.partial_ratio(text.lower(), 'state'):
            continue

        if score > threshold:
            scores.add(choice)

    return scores

def extract_info(result):
    best_country, country_score, country_matching  = fuzzy_matching_country(result)
    best_region, region_score, region_matching = fuzzy_matching_regions(result)

    # if country is not found or us wine (need to find AVA)
    if best_country is None or best_country in state:
        # check if state wine (AVA does not match state)
        if best_country in state and best_region not in country_to_region[best_country]:
            best_region = None
        else:
            # find country using region
            best_country = region_to_country[best_region]

    # check if region and country match (set it to match the higher scored one)
    if best_region is not None and best_region not in country_to_region[best_country]:
        if region_score < country_score:
            best_region = None
        else:
            best_country = region_to_country[best_region]

    # find grape variety
    best_grape, _, _ = fuzzy_matching_grapes(result, best_country)

    # find keywords
    keywords = fuzzy_matching_keyword(result)

    return best_grape, best_region, best_country, keywords