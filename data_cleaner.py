"""
data_cleaner.py
---------------
Cleans, de-duplicates, and formats extracted text into records.
"""

from datetime import date


class DataCleaner:
    def __init__(self, source_url: str):
        self.source_url = source_url
        self.today = str(date.today())

    # ------------------------------------------------------------------
    @staticmethod
    def _normalize(text: str) -> str:
        """Collapse whitespace and strip."""
        return " ".join(text.split()).strip()

    # ------------------------------------------------------------------
    def build_records(self, raw_texts: list[str]) -> list[dict]:
        """
        Convert a list of raw strings into clean records:
        {id, text, source, extracted_at}
        Removes duplicates, empty strings, and normalizes spacing.
        """
        seen = set()
        records = []
        counter = 1

        for raw in raw_texts:
            if not raw:
                continue
            clean = self._normalize(raw)
            if not clean or len(clean) < 3:
                continue
            key = clean.lower()
            if key in seen:
                continue
            seen.add(key)
            records.append({
                "id": counter,
                "text": clean,
                "source": self.source_url,
                "extracted_at": self.today,
            })
            counter += 1

        return records