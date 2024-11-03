from flask import Flask, jsonify, request
from flask_cors import CORS

from dotenv import load_dotenv
from core import pdf_to_md, pdf_to_md_v2

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return 'OCR API SERVER'


@app.route("/v1/ocr/md", methods=["POST"])
def gen_md_with_prepared_image():
    request_json = request.get_json()
    index_name = request_json['index']
    results = pdf_to_md(index_name)
    return jsonify(
        {
            "md_paths": results
        }
    )


@app.route("/v2/ocr/md", methods=["POST"])
def gen_md_with_prepared_image():
    request_json = request.get_json()
    index_name = request_json['index']
    results = pdf_to_md_v2(index_name)
    return jsonify(
        {
            "md_paths": results
        }
    )


@app.after_request
def after_request(response):
    import torch
    torch.cuda.empty_cache()
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
