class EnvFinder(object):
    environ = ''

    def __init__(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        self.environ = os.environ

    def get_env(self, key: str):
        return self.environ[key]

    def get_transformers_url(self):
        return self.environ['TRANSFORMER_URL']

    def get_ollama_url(self):
        return self.environ['OLLAMA_URL']

    def get_openai_key(self):
        return self.environ['OPENAI_API_KEY']

    def get_milvus_url(self):
        return self.environ['MILVUS_URL']

    def get_ocr_url(self):
        return self.environ['OCR_URL']
