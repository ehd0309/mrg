from typing import List

import requests
from pathlib import Path

from utils import EnvFinder


class OCRResolver(object):
    _ocr_endpoint: str = ''
    _ocr_result_path: Path = Path(__file__).parent.parent / 'assets/outputs'

    def __init__(self):
        env_finder = EnvFinder()
        self._ocr_endpoint = env_finder.get_ocr_url()

    def gen_md_from_pdf_v1(self, index_name: str) -> List[str]:
        path = self._ocr_endpoint + '/v1/ocr/md'
        response = requests.post(
            path,
            json={"index": index_name}
        )
        if response.status_code != 200:
            raise ValueError(f"Request failed: {response.status_code}, {response.text}")
        result = response.json()
        return result["md_paths"]

    def gen_md_from_pdf_v2(self, index_name: str) -> List[str]:
        path = self._ocr_endpoint + '/v2/ocr/md'
        response = requests.post(
            path,
            json={"index": index_name}
        )
        if response.status_code != 200:
            raise ValueError(f"Request failed: {response.status_code}, {response.text}")
        result = response.json()
        return result["md_paths"]

    def get_md_result_files(self, index_name: str) -> List[str]:
        md_files = [str(file) for file in (self._ocr_result_path / index_name).glob("**/*.md")]
        return md_files


if __name__ == '__main__':
    ocr = OCRResolver()
    # results = ocr.gen_md_from_pdf_v1(index_name='yun-v1')
    results = ocr.get_md_result_files(index_name='yunv1')
    print(results)
