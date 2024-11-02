from FlagEmbedding import BGEM3FlagModel

bge_model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True, device=0)


def gen_dense_embedding(sentence):
    return bge_model.encode(
        sentence,
        batch_size=2,
        max_length=2048,
        return_dense=True,
        return_sparse=False,
    )['dense_vecs']


def gen_sparse_embedding(sentence):
    return bge_model.encode(
        sentence,
        batch_size=2,
        max_length=2048,
        return_dense=False,
        return_sparse=True,
    )['lexical_weights']

