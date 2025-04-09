import requests
from bs4 import BeautifulSoup

def get_trends():
    try:
        url = "https://en.wikipedia.org/wiki/Electronics_industry"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content = soup.find('div', {'id': 'mw-content-text'})
        return "\n".join([p.text for p in content.find_all('p')[2:6]])
    except Exception as e:
        return "Latest industry trends unavailable. Focus on IoT, AI in electronics, and renewable energy systems."
