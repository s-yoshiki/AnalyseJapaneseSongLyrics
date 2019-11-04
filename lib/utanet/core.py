import urllib3
import re
import certifi
from bs4 import BeautifulSoup
from . import config as config
from . import util

HTTP_PROXY = ''

def set_http_proxy(proxy):
    global HTTP_PROXY
    HTTP_PROXY = proxy

def get_lyrics_by_artistid(id):
    """
    歌詞IDを元に歌詞を取得する
    """
    url = config.BASE_URL + "song/%s/" % id
    return util.get_detail(url)

def search_artists(key):
    url = config.BASE_URL + "search/?Aselect=1&Bselect=3&Keyword=%s&sort=&pnum=%s"
    # ページサイズ取得
    page_max = util.get_pnum_from_url(
        url % (key, 1)
    )
    all_lists = []
    for page_id in list(range(1, page_max + 1)):
        records = util.get_records(url % (key, page_id))
        all_lists.extend(records)
    return all_lists
