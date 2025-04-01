def get_nhs_search_urls(keywords):
    nhs_search_urls = []
    formatted_keywords = keywords.split(",")
    for k in formatted_keywords:
        k = k.strip()
        nhs_search_urls.append(f"https://www.nhs.uk/search/results?q={k}")
    return nhs_search_urls

# Example usage, using bad spacing and typos in the keywords
keywords = "coughing ,  bleeding, sneexing, sore throat"
search_urls = get_nhs_search_urls(keywords)
for url in search_urls:
    print(url)


