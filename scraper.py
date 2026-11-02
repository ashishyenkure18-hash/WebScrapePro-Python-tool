"""
scraper.py
----------
Handles HTTP requests and HTML parsing using Requests + BeautifulSoup.
All CSS selectors / extraction rules are centralized in the CONFIG section.
"""

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# CONFIGURATION – tweak selectors here without touching logic
# ---------------------------------------------------------------------------
CONFIG = {
    "timeout": 10,                      # seconds
    "request_delay": 2,                 # polite delay between requests
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36 WebScrapePro/1.0"
    ),
    "headline_tags": ["h1", "h2", "h3"],
    # CSS selectors used for quote / text extraction (tried in order)
    "quote_selectors": [
        "blockquote",
        "p.quote",
        "div.quote span.text",
        "article p",
        "main p",
    ],
    # Only scrape these public-friendly domains by default (extendable)
    "blocked_keywords": ["login", "signin", "account", "checkout", "admin"],
}


class Scraper:
    """Fetches and parses a webpage."""

    def __init__(self, url: str):
        self.url = url.strip()
        self.html = None
        self.soup = None

    # ------------------------------------------------------------------
    # URL validation
    # ------------------------------------------------------------------
    def is_valid_url(self) -> bool:
        parsed = urlparse(self.url)
        if parsed.scheme not in ("http", "https"):
            print("❌ URL must start with http:// or https://")
            return False
        if not parsed.netloc:
            print("❌ URL is missing a domain name.")
            return False
        # Responsible scraping: block obvious login/admin pages
        for kw in CONFIG["blocked_keywords"]:
            if kw in self.url.lower():
                print(f"🚫 Refusing to scrape '{kw}' page (login-protected / private).")
                return False
        return True

    # ------------------------------------------------------------------
    # HTTP fetch
    # ------------------------------------------------------------------
    def fetch(self) -> bool:
        if not self.is_valid_url():
            return False

        headers = {"User-Agent": CONFIG["user_agent"]}
        print(f"🌐 Fetching: {self.url}")
        try:
            time.sleep(CONFIG["request_delay"])  # polite delay
            response = requests.get(
                self.url, headers=headers, timeout=CONFIG["timeout"]
            )
        except requests.exceptions.Timeout:
            print("❌ Request timed out.")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ Connection error – check your internet / URL.")
            return False
        except requests.exceptions.MissingSchema:
            print("❌ Invalid URL schema.")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False

        # Status handling
        if response.status_code == 403:
            print("🚫 403 Forbidden – site blocks automated access.")
            return False
        if response.status_code == 404:
            print("❌ 404 Not Found – page does not exist.")
            return False
        if response.status_code == 500:
            print("❌ 500 Server Error on target site.")
            return False
        if response.status_code != 200:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False

        self.html = response.text
        self.soup = BeautifulSoup(self.html, "html.parser")
        print("✅ Page fetched successfully.")
        return True

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------
    def extract_headlines(self) -> list[str]:
        if not self.soup:
            return []
        found = []
        for tag in CONFIG["headline_tags"]:
            for el in self.soup.find_all(tag):
                text = el.get_text(strip=True)
                if text:
                    found.append(text)
        return found

    def extract_quotes(self) -> list[str]:
        if not self.soup:
            return []
        found = []
        for selector in CONFIG["quote_selectors"]:
            for el in self.soup.select(selector):
                # Safe get_text – element existence already guaranteed by select()
                text = el.get_text(strip=True)
                if text and len(text) > 20:  # skip tiny fragments
                    found.append(text)
            if found:            # stop at first selector that yields results
                break
        return found