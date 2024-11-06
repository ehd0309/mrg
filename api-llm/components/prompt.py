from langchain import hub
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class Prompt(object):

    @staticmethod
    def rag():
        sys = """
        당신은 질문-답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다. 
        당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
        검색된 다음 문맥(context) 을 사용하여 질문(question) 에 답하세요. 
        만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
        답변은 한글로 답변해 주세요.
        """
        human = """
        #Question: 
        {question} 

        #Context: 
        {context} 

        #Answer:
        """
        return ChatPromptTemplate.from_messages(
            [sys, human])

    @staticmethod
    def rag_with_meta():
        sys = """
        당신은 질문-답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다. 
        당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
        검색된 다음 문맥(context) 을 사용하여 질문(question) 에 답하세요. 
        만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
        답변은 한글로 답변해 주세요.
        """
        human = """
        #Question: 
        {question} 

        #Context: 
        {context} 

        #Answer:
        """
        return ChatPromptTemplate.from_messages(
            [sys, human])

    @staticmethod
    def table_summary():
        sys = """
        You are an assistant tasked with summarizing tables and text for retrieval.
        These summaries will be embedded and used to retrieve the raw text or table elements.
        Give a concise summary of the html table that is well optimized for retrieval.
        """
        human = """
        #Table:
        {table}

        #Summary:
        """
        return ChatPromptTemplate.from_messages(
            [sys, human])

    @staticmethod
    def question_abstraction():
        sys = """
        당신은 {subject} 문서에 대한 질문(question)에 대해 분석 및 판독을 수행하는 AI 어시스턴트입니다.
        주어진 질문(question)이 구체적인지(specific) 추상적인지(abstract) 판단하세요.

        기준:
        - "specific": The question includes specific entities, numbers, or seeks detailed information on a particular topic.
        - "abstract": The question is general, conceptual, or asks for {subject} documentation as a whole rather than targeting specific information.
        
        아래와 같이 문자열로만 답변을 작성하세요.

        결과 예시:
        "specific"
        "abstract"
        """

        human = """
        #question:
        {question}

        #classification:
        """
        return ChatPromptTemplate.from_messages(
            [sys, human])
