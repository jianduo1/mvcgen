from dotenv import load_dotenv, dotenv_values, find_dotenv, get_key, set_key, unset_key
from typing import Dict

class DotEnv:
    def __init__(self) -> None:
        self._path: str = self.file()
        self.load()
    def file(self) -> str:
        return find_dotenv()
    def values(self) -> Dict[str, str | None]:
        return dict(dotenv_values(self._path))
    def load(self) -> bool:
        return load_dotenv(self._path, verbose=True)
    def get(self, key: str, default: str | None = None, raise_error: bool = False) -> str | None:
        value = get_key(self._path, key)
        if not value and raise_error:
            raise ValueError(f"请设置环境变量: {key}")
        return value or default
    def set(self, key: str, value: str) -> None:
        set_key(self._path, key, value)
    def unset(self, key: str) -> None:
        unset_key(self._path, key)
    def __contains__(self, key: str) -> bool:
        return key in dotenv_values(self._path) 


env = DotEnv()