from typing_extensions import TypedDict

class StorageData(TypedDict):
    title: str
    author: str
    text: str
    url: str

    id: int
    submitted_by: str

class Index(TypedDict):
    id: int
    title: str
    author: str