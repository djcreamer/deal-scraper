import requests
from bs4 import BeautifulSoup
import re

def scrape_transactions():
    url = "https://www.multifamilybiz.com/news"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.5481.77 Safari/537.36"
        )
    }

    # Keywords to filter articles
    KEYWORDS = [
        "sale", "acquisition", "purchase", "transaction", "renovation", "kitchen",
        "upgrade"
    ]

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        # Adjust the selector based on the website's structure
        for article in soup.find_all("a", class_="article-content__subhead"):
            title = article.get_text(strip=True)
            link = "https://www.multifamilybiz.com" + article.get("href", "")
            articles.append({
                "title": title,
                "url": link
            })

        # Fetch and filter articles based on keywords
        relevant_articles = []
        for article in articles:
            article_data = fetch_article_details(article["url"], headers, KEYWORDS)
            if article_data:
                relevant_articles.append(article_data)

        return relevant_articles

    except requests.RequestException as e:
        print(f"Error fetching the main page: {e}")
        return []

def fetch_article_details(url, headers, keywords):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract article date
        date_tag = soup.find("time")
        article_date = date_tag.get_text(strip=True) if date_tag else "No date provided"

        # Extract article headline
        headline_tag = soup.find("h1")
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline provided"

        # Extract article body
        content = soup.find("div", itemprop="articleBody")
        if not content:
            return None

        full_text = content.get_text(separator=" ", strip=True)

        # Check for presence of any keywords (case-insensitive)
        if any(re.search(rf"\b{kw}\b", full_text, re.IGNORECASE) for kw in keywords):
            return {
                "title": headline,
                "url": url,
                "date": article_date,
                "headline": headline,
                "full_text": full_text
            }
        else:
            return None

    except requests.RequestException as e:
        print(f"Error fetching article at {url}: {e}")
        return None

# For testing purposes
if __name__ == "__main__":
    articles = scrape_transactions()
    for idx, article in enumerate(articles, start=1):
        print(f"{idx}. {article['title']} ({article['date']})\nURL: {article['url']}\n")
