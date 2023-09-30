import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class VerticalSearchEngine:
    def __init__(self):
        self.index = {}

    def crawl(self, url, depth=3):
        if depth == 0:
            return
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content from the webpage
            text_content = soup.get_text()

            # Index the content
            self.index[url] = text_content

            # Extract links from the webpage and crawl them recursively
            links = soup.find_all('a', href=True)
            for link in links:
                absolute_url = urljoin(url, link['href'])
                if absolute_url not in self.index:
                    self.crawl(absolute_url, depth-1)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, query):
        results = []
        for url, content in self.index.items():
            if query.lower() in content.lower():
                results.append(url)
        return results

# Example usage:
search_engine = VerticalSearchEngine()
search_engine.crawl('https://quotes.toscrape.com/', depth=2)
search_results = search_engine.search('harry')

print("Search Results:")
for result in search_results:
    print(result)