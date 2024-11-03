from typing import Literal, Optional

from langchain_core.language_models import BaseLLM

from utils import EnvFinder
from langchain_ollama import OllamaLLM


class LLM(object):
    openai_api_key: Optional[str] = None
    ollama_url: str = ''
    env_finder: EnvFinder = None

    def __init__(self):
        self.env_finder = EnvFinder()
        self.ollama_url = self.env_finder.get_ollama_url()

    def load_local(self, temp: Optional[float] = 0.1,
                   model: Optional[Literal[
                       'qwen/qwen-7b-fp16:latest',
                       'qwen/qwen-14b-fp16:latest',
                       'yanolja/eeve-10.8b-fp16:latest'
                   ]] = 'yanolja/eeve-10.8b-fp16:latest'
                   , **kwargs) -> BaseLLM:
        return OllamaLLM(base_url=self.ollama_url, temperature=temp, model=model,
                         **kwargs)

    def load_openai(self, temp: Optional[float] = 0.1):
        from langchain_openai import ChatOpenAI
        self.openai_api_key = self.env_finder.get_openai_key()
        return ChatOpenAI(
            api_key=self.openai_api_key,
            temperature=temp,
            model_name='gpt-4o-mini'
        )


if __name__ == '__main__':
    llm = LLM().load_local()
    res = llm.invoke(input='hello world')
    print(res)
