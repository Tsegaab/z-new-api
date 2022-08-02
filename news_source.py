import json
import time
from typing import Union
from abc import ABC, abstractmethod

import requests

import settings
import models


class BaseAPI:
 
    @abstractmethod
    def get_news_list(self, q: Union[str, None] = 'e') -> list:
        pass
 


class RedditAPI(BaseAPI):

    URL = 'https://www.reddit.com'
    source_name = 'reddit'

    def __init__(self) -> None:
        self.token = None
        self.token_time = None

    def get_token(self):
        if self.token is None or (self.token_time is not None
                                  and time.time() - self.token_time > 3590):
            response = requests.post(
                f'{self.URL}/api/v1/access_token',
                data={
                    'grant_type': 'password',
                    'username': settings.REDDIT_USERNAME,
                    'password': settings.REDDIT_PASSWORD
                },
                headers={
                    'user-agent':
                    f'{settings.REDDIT_APP_NAME} by {settings.REDDIT_USERNAME}'
                },
                auth=requests.auth.HTTPBasicAuth(settings.REDDIT_APP_ID,
                                                 settings.REDDIT_APP_SECRET))
            response_json = response.json()
            self.token = response_json['access_token']
            self.token_time = time.time()
        return self.token

    def get_news_list(self, q: Union[str, None] = 'e ') -> list:
        url = 'https://oauth.reddit.com/subreddits/search?'
        if q:
            url += f'q={q}'
        response = requests.get(
            url=url,
            params=dict(sort='relevance', limit=25),
            headers={
                'Authorization':
                f'bearer {self.get_token()}',
                'User-Agent':
                f'{settings.REDDIT_APP_NAME} by {settings.REDDIT_USERNAME}'
            })
        response_json = response.json()
        news_list = []
        if response_json:
            for element in response_json['data']['children']:
                a = element['data']
                news_list.append(
                    models.News(headline=a['title'],
                                link=self.URL + a['url'],
                                source=self.source_name,
                                image_url=a['']))
        return news_list


class NewsAPI(BaseAPI):

    URL = 'https://newsapi.org/v2'
    source_name = 'newsapi'

    def __init__(self) -> None:
        pass

    def get_news_list(self, q: Union[str, None] = 'e') -> list:
        url = f'{self.URL}/everything?'
        if q:
            url += f'q={q}'
        response = requests.get(url=url,
                                params=dict(apiKey=settings.NEWS_API_KEY,
                                            language='en')).json()
        if 'articles' not in response:
            raise Exception(
                'Unexpected respinse from NewsAPI. "{}"'.format(response))
        news_list = []
        for a in response['articles']:
            news_list.append(
                models.News(headline=a['title'],
                            link=a['url'],
                            source=self.source_name))
        return news_list