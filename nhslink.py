def get_nhs_search_url(keyword):
    # Format the keyword for the URL (replace spaces with '+')
    formatted_keyword = keyword.replace(" ", "+")
    nhs_search_url = f"https://www.nhs.uk/search/results?q={formatted_keyword}"
    return nhs_search_url

# Example usage
keyword = "pikjxhdfsiuh"
search_url = get_nhs_search_url(keyword)
print(f"Search NHS: {search_url}")


