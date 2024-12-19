from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import scraper

app = FastAPI(title="Multifamily Transactions Scraper API")

class Article(BaseModel):
    title: str
    url: str
    date: str
    headline: str
    full_text: str

@app.get("/scrape", response_model=List[Article])
def get_scraped_articles():
    try:
        articles = scraper.scrape_transactions()
        if not articles:
            raise HTTPException(status_code=404, detail="No relevant articles found.")
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multifamily Transactions Scraper API. Use the /scrape endpoint to get relevant articles."}
