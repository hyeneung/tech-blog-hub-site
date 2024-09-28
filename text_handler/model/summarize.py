from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


class SummarizeModule:
    def summarize(self, text: str) -> str:
        """
        주어진 text를 요약한 결과를 반환합니다.
        """

        template = """
            You are a korean article summarizer.
            It is recommended to use Title and Subtitle when summarizing the article.
            You only have to answer the summarized texts without your explanation.
            The summarized texts must be in korean.
        """

        prompt = ChatPromptTemplate.from_messages([
            ('system', template),
            ('human', '{article}'),
        ])

        model = OllamaLLM(
            model="llama3.1",
            temperature=0,
        )

        chain = prompt | model

        summarized_text = chain.invoke({'article': text})

        return summarized_text
