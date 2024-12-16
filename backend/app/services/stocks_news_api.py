import finnhub
import os
from dotenv import load_dotenv
load_dotenv()
FINNHUB_KEY = os.getenv("STOCKS_NEWS_KEY")
finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)


def get_company_news(symbol, start, end):
    """
    very basic function
    inputs: stock symbol, start date, end date (YYYY-MM-DD)
    output: json format response
    keys: category, datetime, headline, id, image, related, source, summary, url
    we will most likely use: headline, image, source, summary, url
    """
    company_news = finnhub_client.company_news(symbol, _from=start, to=end)
    return company_news


def get_general_news():
    """
    No args, just returns json data of general news right now related to stocks
    same keys as get_company_news()
    """
    general_news = finnhub_client.general_news('general', min_id=0)
    return general_news
