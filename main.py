from typing import Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from news_source import RedditAPI, NewsAPI
from models import News

SOURCE_APIS = [RedditAPI, NewsAPI]

api = FastAPI()


@api.get('/', include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@api.get(
    '/news', )
def news(q: Union[str, None] = 'e'):
    return NewsAPI().get_news_list(q=q) + RedditAPI().get_news_list(q=q)


@api.get(
    '/r/news', )
def reddit_news():
    RedditAPI().get_news_list()