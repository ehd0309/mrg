import logging
from functools import wraps
from time import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_execution_time(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            logging.info(f"[{name}] Execution Started")
            result = func(*args, **kwargs)
            end_time = time()
            elapsed_time = end_time - start_time
            logging.info(f"[{name}] Execution finished, took {elapsed_time:.2f} seconds")
            return result

        return wrapper

    return decorator
