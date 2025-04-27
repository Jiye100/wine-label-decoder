from rapidfuzz import process, fuzz

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
                 'muscat'
                ]

regions = ["columbia valley", "yakima valley", "walla walla valley", "red mountain", "horse heaven hills",
           "willamette valley", "dundee hills", "yamhill-carlton", "mcminnville", "ribbon ridge", "chehalem mountains", "umpqua valley", "rogue valley", "applegate valley",
           "finger lakes", "cayuga lake", "seneca lake", "north fork of long island", "hamptons", "hudson river region", "lake erie",
           "napa valley", 'sonoma valley', 'russian river valley', 'alexander valley', 'sonoma county','mendocino','santa barbara county','monterey county','paso robles',
           "mendoza", "san juan", "salta", "la rioja", "catamarca",
           "marlborough", "martinborough", "central otago",
           "western cape", "stellenbosch", "simonsberg",
           "elqui valley", "limari valley", "aconcagua", "maipo valley", "cachapoal valley", "colchagua valley", "maule valley",
           "hunter valley", "yarra valley", "adelaide hills", "barossa valley", "clare valley", "mclaren vale", "margaret river", "rutherglen", "coonawarra", "mornington peninsula", "tasmania", "geographe"
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

# country or states
country_state = ["california", "oregon", "new york", "washington", "south africa", "argentina", "new zealand", "chile", "australia"]
state = ['california', 'oregon', 'new york', 'washington']

# common error words that should be ignored
common_error = ['vineyard', 'region', 'valley', 'hills', 'vineyards', 'hill']

# fuzzy matching for grape varieties
def fuzzy_matching_grapes(result, country):
    best_match = None
    matching_text = None
    best_score = 0 # no threshold

    # should not decide grape variety just by looking at 'cabernet' or 'sauvignon'
    cabernet, sauvignon = False, False

    for (_, text, _) in result:
        text = text.lower().replace(' ', '')

        # ignore common errors or short text
        if text in common_error or len(text) < 4:
            continue

        # find the best match
        choice, _, _ = process.extractOne(text, grape_variety)
        
        # torrentes is argentina's signature grape (unlikely to be seen if region is not argentina)
        if country != 'argentina' and choice == 'torrentes':
            continue

        # pinotage is south africa's signature grape (unlikely to be seen if region is not south africa)
        if country != 'south africa' and choice == 'pinotage':
            continue

        # check if subsections are matched (remove any whitespace)
        if choice in ['cabernet sauvignon', 'sauvignon blanc', 'cabernet franc']:
            if fuzz.ratio(text, 'cabernet sauvignon') > 60:
                cabernet, sauvignon = True, True
                best_match = choice
                matching_text = text
                continue
            if fuzz.ratio(text, 'cabernet') > 60:
                cabernet = True
            if fuzz.ratio(text, 'sauvignon') > 60:
                sauvignon = True

        # compute Levenshtein Distance similarity ratio between two strings
        ratio_score = fuzz.ratio(choice, text)
        # compare subsection of the strings (useful when one string is a substring of another)
        partial_ratio_score = fuzz.partial_ratio(choice, text)

        if best_score < ratio_score:
            best_match = choice
            best_score = ratio_score
            matching_text = text
        # elif best_score < partial_ratio_score:
        #     best_match = choice
        #     best_score = partial_ratio_score
        #     matching_text = text

    if cabernet and sauvignon:
        best_match = 'cabernet sauvignon'
    elif sauvignon:
        best_match = 'sauvignon blanc'
    elif cabernet:
        best_match = 'cabernet franc'

    return best_match, best_score, matching_text

def fuzzy_matching_regions(result):
    best_match = None
    best_score = 60 # threshold of 60
    matching_text = None

    for (_, text, _) in result:
        text = text.lower()

        # ignore common errors or grape varieties or short text
        if text in common_error or text in grape_variety or len(text) < 4:
            continue

        text = text.replace(' ', '')

        if text == 'napa':
            best_match = 'napa valley'
            best_score = 100
            matching_text = text

        # find best match
        choice, _, _ = process.extractOne(text, regions)

        # compute Levenshtein Distance similarity ratio between two strings
        ratio_score = fuzz.ratio(choice, text)
        # compare subsection of the strings (useful when one string is a substring of another)
        partial_ratio_score = fuzz.partial_ratio(choice, text)

        if best_score < ratio_score:
            best_match = choice
            best_score = ratio_score
            matching_text = text
        elif best_score < partial_ratio_score:
            best_match = choice
            best_score = partial_ratio_score
            matching_text = text

    return best_match, best_score, matching_text

def fuzzy_matching_country(result):
    best_match = None
    best_score = 60 # threshold of 60
    matching_text = None

    for (_, text, _) in result:
        text = text.lower()

        # ignore common errors or grape varieties or short text
        if text in common_error or text in grape_variety or len(text) < 4:
            continue

        text = text.replace(' ', '')

        # find best match
        choice, _, _ = process.extractOne(text, country_state)

        # compute Levenshtein Distance similarity ratio between two strings
        ratio_score = fuzz.ratio(choice, text)
        # don't compare subsections since countries are short and they rarely break up into multiple strings

        # check if Levenshtein Distance similarity ratio between two strings is higher
        if best_score < ratio_score:
            best_match = choice
            best_score = ratio_score
            matching_text = text
    
    return best_match, best_score, matching_text