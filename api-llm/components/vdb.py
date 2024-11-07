from typing import Union, List, Literal, Any

from langchain_milvus.vectorstores.milvus import EmbeddingType
from langchain_milvus import MilvusCollectionHybridSearchRetriever

from utils import EnvFinder
from langchain_milvus import Milvus
from langchain_core.documents import Document
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    WeightedRanker
)
import datetime


class VectorDatabase(object):
    _db_vendor_name: str = 'milvus'
    _db_endpoint: str = ''
    _db_port: str = '10690'
    _db_host: str = 'localhost'
    _env_finder: EnvFinder = None

    # fields
    dense_vector_field: str = 'vector'
    sparse_vector_field: str = 'sparse_vector'
    text_field_name: str = 'text'
    filename_field: str = 'filename'
    additional_content_field: str = 'additional_content'
    category_field: str = 'category'
    last_modified_field: str = 'last_modified'

    def __init__(self):
        self._env_finder = EnvFinder()
        self._db_endpoint = self._env_finder.get_milvus_url()
        self._db_port = self._db_endpoint.split(":")[2]
        self._db_host = self._db_endpoint.split(":")[1].replace("//", "")

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

    def load_hybrid_retriever(self,
                              collection_name: str,
                              dense_embedding: EmbeddingType,
                              sparse_embedding: EmbeddingType,
                              top_k: int
                              ):
        dense_param = VectorDatabase.get_idx('dense')
        sparse_param = VectorDatabase.get_idx('sparse')
        collection = self.get_collection(collection_name)
        retriever = MilvusCollectionHybridSearchRetriever(
            collection=collection,
            rerank=WeightedRanker(0.8, 0.2),
            field_embeddings=[dense_embedding, sparse_embedding],
            field_search_params=[dense_param, sparse_param],
            anns_fields=[self.dense_vector_field, self.sparse_vector_field],
            top_k=top_k,
            text_field='text'
        )
        return retriever

    @staticmethod
    def get_idx(type: Literal['dense', 'sparse']):
        if type == 'dense':
            return {"index_type": "FLAT", "metric_type": "COSINE"}
        if type == 'sparse':
            return {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"}

    def get_collection(self, collection_name: str) -> Collection:
        connections.connect(host=self._db_host, port=self._db_port)
        fields = [
            FieldSchema(name='pk', dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
            FieldSchema(name=self.dense_vector_field, dtype=DataType.FLOAT_VECTOR, dim=1024),
            FieldSchema(name=self.sparse_vector_field, dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(name=self.text_field_name, dtype=DataType.VARCHAR, max_length=65_535),
            FieldSchema(name=self.category_field, dtype=DataType.VARCHAR, max_length=65_535),
            FieldSchema(name=self.filename_field, dtype=DataType.VARCHAR, max_length=65_535),
            FieldSchema(name=self.additional_content_field, dtype=DataType.VARCHAR, max_length=65_535),
            FieldSchema(name=self.last_modified_field, dtype=DataType.VARCHAR, max_length=65_535),
        ]
        schema = CollectionSchema(fields=fields, enable_dynamic_field=True)
        collection = Collection(
            name=collection_name, schema=schema,
        )
        return collection

    def generate_collection_idx(self, collection_name: str):
        collection = self.get_collection(collection_name=collection_name)
        collection.create_index(self.dense_vector_field, VectorDatabase.get_idx(type='dense'))
        collection.create_index(self.sparse_vector_field, VectorDatabase.get_idx(type='sparse'))
        collection.flush()
        print('index-generated', datetime.datetime.now())

    def hybrid_embedding(self, collection_name: str, dense_embedding: EmbeddingType, sparse_embedding: EmbeddingType,
                         docs: List[Document],
                         keywords: list[str]
                         , **kwargs):
        collection = self.get_collection(collection_name=collection_name)
        entities = []
        for idx, doc in enumerate(docs):
            entity = {
                self.text_field_name: doc.page_content,
                self.dense_vector_field: dense_embedding.embed_documents([doc.page_content])[0],
                self.sparse_vector_field: sparse_embedding.embed_documents([keywords[idx]])[0],
                self.category_field: doc.metadata[self.category_field],
                self.additional_content_field: doc.metadata[self.additional_content_field],
                self.filename_field: doc.metadata[self.filename_field],
                self.last_modified_field: doc.metadata[self.last_modified_field]
            }
            entities.append(entity)
        collection.insert(entities)
        collection.load()
        print('embedding-done', datetime.datetime.now())
