import json
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
import logging

load_dotenv()


def gen_history(index_name: str, history):
    # history.json 파일 경로
    history_path = Path(__file__).parent.parent / 'assets/history.json'

    if history_path.exists():
        with open(history_path, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
    else:
        history_data = {}

    history_data[index_name] = history

    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=4)

    print(f"Updated history.json with index: {index_name}")


def check_history_exists(index_name: str) -> bool:
    history_path = Path(__file__).parent.parent / 'assets/history.json'
    logging.log(msg=history_path, level=logging.INFO)
    if not history_path.exists():
        return False

    with open(history_path, 'r', encoding='utf-8') as f:
        history_data = json.load(f)
    return index_name in history_data


def get_existing_keys() -> list:
    history_path = Path(__file__).parent.parent / 'assets/history.json'

    if not history_path.exists():
        return []

    with open(history_path, 'r', encoding='utf-8') as f:
        history_data = json.load(f)

    return list(history_data.keys())


def get_values_from_history(index_name: str) -> Dict[str, Any]:
    history_path = Path(__file__).parent.parent / 'assets/history.json'
    if not history_path.exists():
        return {}
    with open(history_path, 'r', encoding='utf-8') as f:
        history_data = json.load(f)
    history = history_data.get(index_name, {})
    return history
