import json
from abc import ABC, abstractmethod


class ConfigObject(ABC):

    def set_kwargs(self, kwargs: dict):
        for k, v in kwargs:
            setattr(self, k, v)

    @classmethod
    def from_json_file(cls, filepath: str) -> object:
        obj = None
        with open(filepath) as file:
            obj = cls.from_json(json.load(file))

        if not obj:
            raise Exception("Object could not be created")
        return obj

    @staticmethod
    @abstractmethod
    def _from_json(self, json_dict: dict) -> object:
        raise NotImplementedError

    @classmethod
    def from_json(cls, json_dict: dict) -> object:
        return cls._from_json(json_dict)

