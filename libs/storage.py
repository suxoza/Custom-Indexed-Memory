import hashlib
import inspect
import datetime
from random import randrange
from libs.data_types import StorageData

class Storage:

    _id: int = 0
    _url: str
    url_hostname: str = ''
    url_scheme: str = ''
    submitted_by: str = ''

    def __init__(self, data: StorageData) -> None:
        self.title = data.get('title', '')
        self.author = data.get('author', '')
        self.text = data.get('text', '')
        self.id = data.get('id', '')

        self.submitted_by = data.get('user_agent', '')
        self.created_at = datetime.datetime.now().isoformat()
        self._url = data.get('url')
        self._set_host_details()

    def _set_host_details(self):
        parse = self._url.split('://')
        [self.url_hostname, self.url_scheme] = [parse[0], parse[1].split('/')[0]]

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = f'{value}-{randrange(240)}'

    @property
    def title_md5(self):
       return hashlib.md5(self.title.encode()).hexdigest() if self.title else ''
    
    @property
    def text_md5(self):
       return hashlib.md5(self.text.encode()).hexdigest() if self.text else ''

    @property
    def title_len_ch(self):
        return len(self.title)
    
    @property
    def text_len_ch(self):
        return len(self.text)

    @property
    def title_len_words(self):
        return len(self.title.split())
    
    @property
    def text_len_words(self):
        return len(self.text.split())

    # retrieves fields based on the "schema" argument, or all of them.
    def to_json(self, schema: set = ()): 
        return {x: getattr(self, x) for x in dir(self) if (not schema or (schema and x in schema)) and not (x.startswith('_') or inspect.ismethod(getattr(self, x)))}

    def to_item(self): 
        return self.to_json(('id', 'title', 'author', 'text', 'created_at'))

    def to_rss(self):
        return dict(
            guid=f'/item/{self.id}',
            title=self.title,
            source=self.author,
            link=self._url,
            pubDat=self.created_at
        )