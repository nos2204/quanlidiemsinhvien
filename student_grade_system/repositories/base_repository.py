"""
Base Repository — Student Grade Management System
Layer: Data Access Layer
Pattern: Repository Pattern with JSON file persistence
"""

import json
import os
from typing import Any


class JSONRepository:
    _filepath: str = ""

    def __init__(self, data_dir: str = "data"):
        self._data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self._full_path = os.path.join(data_dir, self._filepath)
        self._cache: list[dict] = self._load()

    def _load(self) -> list[dict]:
        if not os.path.exists(self._full_path):
            return []
        with open(self._full_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        with open(self._full_path, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, indent=2, ensure_ascii=False)

    def get_all(self) -> list[Any]:
        return [self._deserialize(item) for item in self._cache]

    def find_by_id(self, entity_id: str) -> Any | None:
        for item in self._cache:
            if item.get(self._id_field) == entity_id:
                return self._deserialize(item)
        return None

    def save(self, entity: Any) -> None:
        data = entity.to_dict()
        for i, item in enumerate(self._cache):
            if item.get(self._id_field) == data[self._id_field]:
                self._cache[i] = data
                self._save()
                return
        self._cache.append(data)
        self._save()

    def delete(self, entity_id: str) -> bool:
        before = len(self._cache)
        self._cache = [
            item for item in self._cache
            if item.get(self._id_field) != entity_id
        ]
        if len(self._cache) < before:
            self._save()
            return True
        return False

    def _deserialize(self, data: dict) -> Any:
        raise NotImplementedError

    @property
    def _id_field(self) -> str:
        raise NotImplementedError