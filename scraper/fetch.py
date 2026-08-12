import requests
import time
import random
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (prototype research project)"
}


def fetch_perfume_page(url: str) -> BeautifulSoup:
    """Busca uma página de perfume individual, com delay para não sobrecarregar o site."""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    time.sleep(random.uniform(2, 4))  # delay educado entre requests
    return BeautifulSoup(resp.text, "html.parser")