def get_nhs_search_urls(keywords):
    nhs_search_urls = []
    if "," not in keywords:  
        keywords = keywords.replace(" ", "%20").strip() 
        nhs_search_urls.append(f"https://www.nhs.uk/search/results?q={keywords}")
    else:  
        for keyword in keywords.split(","):
            keyword = keyword.strip().replace(" ", "%20")
            if keyword: 
                nhs_search_urls.append(f"https://www.nhs.uk/search/results?q={keyword}")
    return nhs_search_urls

keywords = "vomiting, blood, tummy ache"  
search_urls = get_nhs_search_urls(keywords)
for url in search_urls:
    print(url)

