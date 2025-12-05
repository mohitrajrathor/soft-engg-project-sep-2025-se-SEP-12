import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from typing import Set, List, Dict
import mimetypes
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecursiveCrawler:
    def __init__(self, base_url: str, max_depth: int = 2, download_dir: str = "data/ingestion"):
        self.base_url = base_url
        self.max_depth = max_depth
        self.download_dir = download_dir
        self.visited_urls: Set[str] = set()
        self.downloaded_files: List[Dict[str, str]] = []
        
        # Allowed extensions for documents
        self.allowed_extensions = {
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.ppt', '.pptx'
        }
        
        # Create download directory if it doesn't exist
        os.makedirs(self.download_dir, exist_ok=True)

    def is_valid_url(self, url: str) -> bool:
        """Check if the URL belongs to the same domain, strictly within the base path, and hasn't been visited."""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        
        # Ensure strict path adherence (e.g., if base is /ds/, don't crawl /archive.html)
        # We normalize paths to ensure consistent comparison
        base_path = parsed_base.path.rstrip('/')
        url_path = parsed_url.path.rstrip('/')
        
        return (
            parsed_url.netloc == parsed_base.netloc and
            url_path.startswith(base_path) and
            url not in self.visited_urls and
            not url.startswith('mailto:') and
            not url.startswith('javascript:')
        )

    def get_file_extension(self, url: str) -> str:
        """Get file extension from URL or Content-Type header."""
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        return ext

    def download_file(self, url: str) -> str:
        """Download file from URL and return the local path."""
        try:
            response = self._make_request(url, stream=True)
            if not response:
                return ""
            
            # Determine filename
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "index.html"
                
            # Handle duplicate filenames
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(self.download_dir, filename)):
                filename = f"{base}_{counter}{ext}"
                counter += 1
                
            filepath = os.path.join(self.download_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded: {url} -> {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")
            return ""

    def _make_request(self, url: str, stream: bool = False, retries: int = 3):
        """Helper to make requests with retries and delay."""
        for attempt in range(retries):
            try:
                response = requests.get(url, stream=stream, timeout=10)
                response.raise_for_status()
                return response
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                time.sleep(2 * (attempt + 1))  # Exponential backoff
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    logger.error(f"404 Not Found: {url}")
                    return None # Don't retry 404s
                logger.warning(f"HTTP Error {e} for {url}")
                
        logger.error(f"Max retries reached for {url}")
        return None

    def crawl(self, url: str = None, depth: int = 0):
        """Recursively crawl the website."""
        if url is None:
            url = self.base_url
            
        if depth > self.max_depth or not self.is_valid_url(url):
            return

        logger.info(f"Crawling: {url} (Depth: {depth})")
        self.visited_urls.add(url)

        try:
            response = self._make_request(url)
            if not response:
                return

            soup = BeautifulSoup(response.text, 'html.parser')

            # Process current page as a document if it's HTML
            # We save the HTML content itself as a text file for processing
            html_filename = f"page_{len(self.visited_urls)}.html"
            html_path = os.path.join(self.download_dir, html_filename)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            self.downloaded_files.append({
                "url": url,
                "path": html_path,
                "type": "html"
            })

            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                # Check if it's a document file
                ext = self.get_file_extension(full_url)
                if ext in self.allowed_extensions:
                    if full_url not in self.visited_urls and self.is_valid_url(full_url): # Check valid url for docs too
                        filepath = self.download_file(full_url)
                        if filepath:
                            self.downloaded_files.append({
                                "url": full_url,
                                "path": filepath,
                                "type": ext
                            })
                        self.visited_urls.add(full_url)
                
                # Continue crawling if it's a web page
                elif self.is_valid_url(full_url):
                    # Add a small delay to be polite
                    time.sleep(1.0)
                    self.crawl(full_url, depth + 1)

        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")

    def run(self):
        """Start the crawling process."""
        logger.info(f"Starting crawl of {self.base_url}")
        self.crawl()
        logger.info(f"Crawl completed. Downloaded {len(self.downloaded_files)} files.")
        return self.downloaded_files

if __name__ == "__main__":
    # Test the crawler
    crawler = RecursiveCrawler("https://study.iitm.ac.in/ds/", max_depth=1)
    files = crawler.run()
    print(f"Total files downloaded: {len(files)}")
