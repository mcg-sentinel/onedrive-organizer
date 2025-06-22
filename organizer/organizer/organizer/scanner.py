import requests
from tqdm import tqdm

class Scanner:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _list_children(self, item_id=None):
        url = (
            "https://graph.microsoft.com/v1.0/me/drive/root/children"
            if item_id is None
            else f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/children"
        )
        while url:
            r = self.session.get(url)
            r.raise_for_status()
            data = r.json()
            for item in data.get("value", []):
                yield item
            url = data.get("@odata.nextLink")

    def scan(self):
        """Yield file metadata dictionaries for every file in OneDrive."""
        for item in tqdm(self._list_children(), desc="Scanning OneDrive"):
            if "file" in item:
                yield {
                    "id": item["id"],
                    "name": item["name"],
                    "size": item["size"],
                    "path": item["parentReference"]["path"],
                    "hash": item["file"].get("hashes", {}).get("sha1Hash"),
                    "downloadUrl": item.get("@microsoft.graph.downloadUrl"),
                }
