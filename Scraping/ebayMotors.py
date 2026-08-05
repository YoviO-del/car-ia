import requests

base_url = "https://api.ebay.com/buy/browse/v1/item_summary/"

def get_listing_info(search_query):
    url = f"{base_url}search?q={search_query}&limit=10"
    response = requests.get(url)
    print(response)


get_listing_info("Mercedes Benz e55 amg")