"""
file_handler.py
---------------
Handles saving records to JSON and TXT files.
"""

import json


class FileHandler:
    def __init__(self, json_path="quotes.json", txt_path="quotes.txt"):
        self.json_path = json_path
        self.txt_path = txt_path

    # ------------------------------------------------------------------
    def save_json(self, records: list[dict]) -> bool:
        if not records:
            print("⚠️  No records to save.")
            return False
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(records)} record(s) to {self.json_path}")
            return True
        except OSError as e:
            print(f"❌ Could not write JSON: {e}")
            return False

    # ------------------------------------------------------------------
    def save_txt(self, records: list[dict]) -> bool:
        if not records:
            print("⚠️  No records to save.")
            return False
        try:
            with open(self.txt_path, "w", encoding="utf-8") as f:
                f.write(f"WebScrapePro Export – Source: {records[0]['source']}\n")
                f.write("=" * 60 + "\n\n")
                for rec in records:
                    f.write(f"[{rec['id']}] {rec['text']}\n")
            print(f"💾 Saved {len(records)} record(s) to {self.txt_path}")
            return True
        except OSError as e:
            print(f"❌ Could not write TXT: {e}")
            return False