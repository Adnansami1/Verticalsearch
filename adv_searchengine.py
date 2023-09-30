import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import re

class VerticalSearchEngine:
    def __init__(self):
        self.index = {}
        self.word_count = Counter()

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

            # Update word count
            words = re.findall(r'\w+', text_content.lower())
            self.word_count.update(words)

            # Extract links from the webpage and crawl them using multithreading
            links = soup.find_all('a', href=True)
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.crawl, urljoin(url, link['href']), depth-1) for link in links]

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, query):
        results = []

        # Implement a basic page ranking algorithm based on word frequency
        for url, content in self.index.items():
            score = sum(self.word_count[word] for word in query.lower().split() if word in self.word_count)
            results.append((url, score))

        # Sort results by score in descending order
        results.sort(key=lambda x: x[1], reverse=True)

        return [result[0] for result in results]

# Example usage with a simple command-line interface:
search_engine = VerticalSearchEngine()
search_engine.crawl('https://quotes.toscrape.com/', depth=2)

while True:
    user_query = input("Enter your search query (type 'exit' to end): ")
    if user_query.lower() == 'exit':
        break

    search_results = search_engine.search(user_query)
    print("Search Results:")
    for result in search_results:
        print(result)
