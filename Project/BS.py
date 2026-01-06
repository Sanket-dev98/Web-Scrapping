import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

def scrape_books_project():
    base_url = "https://books.toscrape.com/"
    current_url = "https://books.toscrape.com/catalogue/page-1.html"

    # Mapping for rating logic
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    all_books = []

    while current_url:
        print(f"Scraping: {current_url}")

        response = requests.get(current_url)
        response.encoding = "utf-8"   # ✅ FIXED encoding issue
        soup = BeautifulSoup(response.text, "html.parser")

        # Targeting each book container
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            # Book title
            title_tag = article.find("a", title=True)
            title = title_tag["title"]

            # Book price
            price_text = article.find("p", class_="price_color").text
            price = float(price_text.replace("£", ""))

            # Book rating
            star_tag = article.find("p", class_="star-rating")
            rating_word = star_tag["class"][1]
            rating_num = rating_map.get(rating_word, 0)

            # Stock availability
            stock_text = article.find(
                "p", class_="instock availability"
            ).text.strip()

            all_books.append({
                "Title": title,
                "Price (£)": price,
                "Rating": rating_num,
                "Stock": stock_text
            })

        # Pagination handling
        next_button = soup.find("li", class_="next")
        if next_button:
            next_url_relative = next_button.find("a")["href"]
            current_url = urljoin(current_url, next_url_relative)
            time.sleep(1)  # Ethical delay
        else:
            current_url = None

    # Save scraped data to CSV
    df = pd.DataFrame(all_books)
    df.to_csv("all_books_data.csv", index=False)
    print("Success! Data saved to all_books_data.csv")

if __name__ == "__main__":
    scrape_books_project()
