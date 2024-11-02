from flask import Flask, jsonify, request
from flask_cors import CORS

from models import gen_dense_embedding, gen_sparse_embedding

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return 'TF API SERVER'


@app.route("/api/embed/dense", methods=["POST"])
def gen_dense_embeddings():
    request_json = request.get_json()
    sentence = request_json['sentence']
    results = gen_dense_embedding(sentence)
    response = results.tolist()
    del results
    return jsonify(
        {
            "embeddings": response
        }
    )


@app.route("/api/embed/sparse", methods=["POST"])
def gen_sparse_embeddings():
    request_json = request.get_json()
    sentence = request_json['sentence']
    results = gen_sparse_embedding(sentence)
    response = []
    for result in results:
        to_json = {key: float(value) for key, value in result.items()}
        response.append(to_json)
        del to_json
    del results
    return jsonify(
        {
            "embeddings": response
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)