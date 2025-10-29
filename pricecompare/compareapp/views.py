from django.shortcuts import render
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

# .env file se keys load karo
load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

def search_page(request):
    return render(request, "compare.html")


def compare_prices(request):
    query = request.GET.get('query')  # user input (search bar)
    google_products = []
    ebay_products = []
    amazon_products = []

    if query:
        # --- GOOGLE SHOPPING ---
        google_params = {
            "engine": "google_shopping",
            "q": query,
            "gl": "in",
            "api_key": api_key,
        }
        google_search = GoogleSearch(google_params)
        google_results = google_search.get_dict()

        for item in google_results.get("shopping_results", []):
            google_products.append({
                "title": item.get("title"),
                "price": item.get("price"),
                "link": item.get("link"),
                "thumbnail": item.get("thumbnail"),
                "source": "Google Shopping"
            })

        # --- eBAY ---
        ebay_params = {
            "engine": "ebay",
            "_nkw": query,
            "ebay_domain": "ebay.com",
            "api_key": api_key
        }
        ebay_search = GoogleSearch(ebay_params)
        ebay_results = ebay_search.get_dict()

        for item in ebay_results.get("organic_results", []):
            ebay_products.append({
                "title": item.get("title"),
                "price": item.get("price"),
                "link": item.get("link"),
                "thumbnail": item.get("thumbnail"),
                "source": "eBay"
            })

        # --- AMAZON ---
        amazon_params = {
            "engine": "amazon",
            "k": query,
            "amazon_domain": "amazon.com",
            "api_key": api_key
        }
        amazon_search = GoogleSearch(amazon_params)
        amazon_results = amazon_search.get_dict()

        for item in amazon_results.get("organic_results", []):
            amazon_products.append({
                "title": item.get("title"),
                "price": item.get("price"),
                "link": item.get("link"),
                "thumbnail": item.get("thumbnail"),
                "source": "Amazon"
            })

    context = {
        "query": query,
        "google_products": google_products,
        "ebay_products": ebay_products,
        "amazon_products": amazon_products
    }

    return render(request, "compare_results.html", context)
