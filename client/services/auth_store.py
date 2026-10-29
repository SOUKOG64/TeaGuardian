import json
from pathlib import Path


class AuthStore:
    def __init__(self, app_dir: str):
        self.path = Path(app_dir) / "tea_guardian_tokens.json"

    def read(self):
        if not self.path.exists():
            return None
        try:
            with self.path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return None

    def write(self, token_data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(token_data, file, ensure_ascii=False)

    def clear(self):
        if self.path.exists():
            self.path.unlink()
