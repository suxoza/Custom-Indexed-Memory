from collections import deque
from fuzzysearch import find_near_matches

from libs.storage import Storage
from libs.data_types import StorageData, Index

STORAGE_MAX_LENGTH = 150

class Storages:
    
    _storage = {
        'data': deque([], maxlen=STORAGE_MAX_LENGTH),
        'indexes': deque([], maxlen=STORAGE_MAX_LENGTH)
    }
    
    storage: StorageData

    def add(self, data: StorageData) -> None:
        self.storage = Storage({**data, 'id': self.length + 1})
        index = Index(id=self.storage.id, title=self.storage.title, author=self.storage.author)
        self._storage['data'].append(self.storage)
        self._storage['indexes'].append(index)
        return self.storage

    @property
    def length(self):
        return len(self._storage['data'])

    def get_item(self, item_id: int):
        index = next((index for (index, d) in enumerate(self._storage['indexes']) if d["id"] == item_id), -1)
        return self._storage['data'][index].to_json() if index > -1 else {}
        
    def search(self, searchData, is_rss = False):
        size = 50
        try:
            size = int(searchData.get('size', 50))
        except TypeError:
            pass

        rss_or_item = 'to_item' if not is_rss else 'to_rss'

        title = searchData.get('title')
        author = searchData.get('author')
        
        # If no title or author are provided, all records will be retrieved. depends on "size" arg, in reversed order
        if not any([title, author]):
            return [getattr(self._storage['data'][i - 1], rss_or_item)() for i in range(min(self.length, size), 0, -1)]
            
        responce = []

        # search in indexes-storage, 
        # reversed loop, to give the new items priority
        for index in range(min(self.length, size), 0, -1):
            i = index-1
            index_data = self._storage['indexes'][i]

            # author exact search
            if author and not author == index_data['author']:
                continue

            # title fuzzy search
            if title and not find_near_matches(title, index_data['title'], max_l_dist=1):
                continue

            # data.to_rss() if is_rss else data.to_item()
            responce.append(getattr(self._storage['data'][i], rss_or_item)())

        return responce or []

if __name__ == '__main__':
    d = {
        'id': 11,
        'title': 'some',
        'author': 'some-author',
        'text': 'some-text',
        'url': 'http://stackoverflow.com/questions/1234567/blah-blah-blah-blah'
    }
    storage = Storages()
    storage.add(d)
    storage.add({**d, 'title': 'second'})
    storage.add({**d, 'title': 'thirdconthr'})
    storage.add({**d, 'title': 'fourth'})

    data = storage.search({
        'title': '',
        'size': 2
    })
    for item in data:
        print(item)
    print('--------------')
    print(storage.get_item(1))