from collections import defaultdict

class Deduplicator:
    """Detect duplicate files by SHA‑1 hash."""

    def find_duplicates(self, files):
        by_hash = defaultdict(list)
        for f in files:
            h = f.get("hash")
            if h:
                by_hash[h].append(f)
        return {h: items for h, items in by_hash.items() if len(items) > 1}
