from typing import Union, List

from langchain_milvus.vectorstores.milvus import EmbeddingType

from utils import EnvFinder
from langchain_milvus import Milvus


class VectorDatabase(object):
    _db_vendor_name: str = 'milvus'
    _db_endpoint: str = ''
    _env_finder: EnvFinder = None

    def __init__(self):
        self._env_finder = EnvFinder()
        self._db_endpoint = self._env_finder.get_milvus_url()

    def load(self,
             collection_name: str,
             embeddings: Union[EmbeddingType, List[EmbeddingType]],
             **kwargs) -> Milvus:
        vector_store = Milvus(
            embedding_function=embeddings,
            collection_name=collection_name,
            connection_args={"uri": self._db_endpoint},
            **kwargs
        )
        return vector_store
