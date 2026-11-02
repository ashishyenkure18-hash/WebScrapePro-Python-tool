"""
main.py
-------
Interactive CLI for WebScrapePro.
"""

from scraper import Scraper
from data_cleaner import DataCleaner
from file_handler import FileHandler


class WebScrapePro:
    def __init__(self):
        self.url = ""
        self.scraper = None
        self.records = []
        self.file_handler = FileHandler()

    # ------------------------------------------------------------------
    def menu(self):
        print("\n" + "=" * 50)
        print("        WebScrapePro – Web Scraper")
        print("=" * 50)
        print("1. Enter a website URL")
        print("2. Extract headlines")
        print("3. Extract quotes / selected text")
        print("4. Display extracted records")
        print("5. Save records as JSON")
        print("6. Save records as TXT")
        print("7. View total number of extracted records")
        print("8. Exit")
        print("=" * 50)

    # ------------------------------------------------------------------
    def set_url(self):
        url = input("Enter website URL: ").strip()
        if not url:
            print("❌ URL cannot be empty.")
            return
        self.scraper = Scraper(url)
        if self.scraper.fetch():
            self.url = url
            self.records = []      # reset on new URL
            print("✅ URL set and page loaded.")
        else:
            print("❌ Could not load that URL.")

    # ------------------------------------------------------------------
    def _append_records(self, raw_texts):
        if not self.scraper:
            print("⚠️  Please enter a URL first (option 1).")
            return
        cleaner = DataCleaner(self.url)
        new_records = cleaner.build_records(raw_texts)
        if not new_records:
            print("⚠️  No valid text found on this page.")
            return
        # Merge avoiding duplicate text
        existing = {r["text"].lower() for r in self.records}
        added = 0
        for rec in new_records:
            if rec["text"].lower() not in existing:
                rec["id"] = len(self.records) + 1
                self.records.append(rec)
                existing.add(rec["text"].lower())
                added += 1
        print(f"✅ Added {added} new record(s). Total: {len(self.records)}")

    # ------------------------------------------------------------------
    def extract_headlines(self):
        if not self.scraper or not self.scraper.soup:
            print("⚠️  Please enter a URL first (option 1).")
            return
        print("🔍 Extracting headlines...")
        self._append_records(self.scraper.extract_headlines())

    def extract_quotes(self):
        if not self.scraper or not self.scraper.soup:
            print("⚠️  Please enter a URL first (option 1).")
            return
        print("🔍 Extracting quotes / paragraphs...")
        self._append_records(self.scraper.extract_quotes())

    # ------------------------------------------------------------------
    def display(self):
        if not self.records:
            print("📭 No records yet.")
            return
        print(f"\n📄 {len(self.records)} record(s):")
        for rec in self.records:
            print(f"  [{rec['id']}] {rec['text']}")

    def save_json(self):
        self.file_handler.save_json(self.records)

    def save_txt(self):
        self.file_handler.save_txt(self.records)

    def total(self):
        print(f"📊 Total extracted records: {len(self.records)}")

    # ------------------------------------------------------------------
    def run(self):
        actions = {
            "1": self.set_url,
            "2": self.extract_headlines,
            "3": self.extract_quotes,
            "4": self.display,
            "5": self.save_json,
            "6": self.save_txt,
            "7": self.total,
        }
        while True:
            self.menu()
            choice = input("Choose an option (1-8): ").strip()
            if choice == "8":
                print("👋 Goodbye! Remember to scrape responsibly.")
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("❌ Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    WebScrapePro().run()