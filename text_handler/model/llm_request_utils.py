import json
from pathlib import Path
from typing import List, Tuple

from langchain.prompts import PromptTemplate, FewShotPromptTemplate

import fewshot_examples

# 주로 LLM에 전송할 request와 prompt에 대한 utility 클래스, HashtaggingModule 보조
class LLMRequestUtils:
    category_json_file_path = Path(__file__).parent / "category.json" # category.json은 hashtags.py와 동일한 폴더 내에 있어야 함.

    def __init__(self):
        pass

    # CAUTION - Not currently used : llama3.1-70b 모델 사용시 사용되는 request 생성 함수. 참고용으로만 사용할 것.
    def make_request_json(self, prompt: str) -> dict:
        """
        prompt를 받아 LLM 모델에게 전송할 request를 만드는 함수입니다.
        
        Parameters:
        prompt (str): request에 실릴 프롬프트의 내용
        
        Returns:
        api_request_json (dict): dict형식으로 표현된 request
        """
        api_request_json = {
        "model": "llama3.1-70b",
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "options": {
            "seed": 42,
            "temperature":0
            }
        }

        return api_request_json
    
    def make_prompt_for_intro_blocks(self, intro_blocks: List[List[Tuple[str, str]]]) -> str:
        """
        Intro에 해당하는 블록들을 받아 LLM 모델에게 전송할 프롬프트를 만드는 함수입니다.
        (HashtaggingModule의 get_keywords_from_intro 함수에 사용되는 프롬프트를 만드는 함수입니다.)
        
        Parameters:
        intro_blocks (List[List[Tuple[str, str]]]): Intro에 해당하는 block들
        
        Returns:
        final_prompt (str): LLM 모델에게 전송할 프롬프트
        """
        examples = fewshot_examples.intro_examples
        example_prompt = PromptTemplate.from_template(
            "TITIE: {title}\nCONTENT: {intro_content}\nSUBTITLE: {subtitle}\nCONTENT: {subtitle_content}\nKEYWORDS: {keywords}")

        prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt = example_prompt,
        prefix = """
        You are an excellent English Key word extractor.
        Your role is to extract one to three key words related to technology.
        If the contents of CONTENT are empty, extract keywords based on the contents of Title or Subtitle.
        Each keyword should consist of **one or two** words.
        If it is not a technical term or not mentioned, extract it again except for the corresponding word.
        If the extracted word is not related to technology, extract it again except for it.
        If there is any keyword in Korean, you must translate it to English before including it in the result.
        Only respond with English keywords.
        Ensure that the output is separated by commas and contains no further explanation.
        """,
        
        suffix="TITIE: {title}\nCONTENT: {intro_content}\nSUBTITLE: {subtitle}\nCONTENT: {subtitle_content}\nKEYWORDS: ",)

        final_prompt = prompt.format(
            title=intro_blocks[0][0][1], intro_content=intro_blocks[0][1][1],
            subtitle=intro_blocks[1][0][1], subtitle_content=intro_blocks[1][1][1])

        return final_prompt

    def make_prompt_for_unit_block(self, body_block: List[Tuple[str, str]]) -> str:
        """
        body 내의 block을 받아 LLM 모델에게 전송할 프롬프트를 만드는 함수입니다.
        (HashtaggingModule의 get_candidates_from_block 함수에 사용되는 프롬프트를 만드는 함수입니다.)
        
        Parameters:
        body_block (List[Tuple[str, str]]): 분석하고자 하는 body에 해당하는 block
        
        Returns:
        final_prompt (str): LLM 모델에게 전송할 프롬프트
        """
        examples = fewshot_examples.body_examples
        example_prompt = PromptTemplate.from_template(
            "SUBTITLE: {subtitle}\nCONTENT: {content}\nKEYWORDS: {keywords}")

        prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt = example_prompt,
        prefix = """
        You are an excellent English Key word extractor.
        Your role is to extract one to three key words related to technology term.
        If CONTENT is empty, extract keywords based on the Subtitle.
        KEYWORDS should be the words mentioned in the article.
        Each keyword should consist of **one or two** words.
        KEYWORDS are English only, translate if in Korean.
        Ensure that the output is separated by commas and contains no further explanation.
        """,
        
        suffix="SUBTITLE: {subtitle}\nCONTENT: {content}\nKEYWORDS: ",)

        final_prompt = prompt.format(subtitle=body_block[0][1], content=body_block[1][1])

        return final_prompt
    
    def make_prompt_for_candidates(self, candidates: List[str]) -> str:
        """
        여러 block들에서 모아진 keywords들(candidates)를 받아 LLM에게 전송할 프롬프트를 만드는 함수입니다.
        (HashtaggingModule의 make_keywords_from_candidates에서 사용되는 함수입니다.)
        
        Parameters:
        candidates (List[str]): 분석에 사용한 모든 block들에서 모아진 모든 keywords들
        
        Returns:
        final_prompt (str): LLM 모델에게 전송할 프롬프트
        """
        examples = fewshot_examples.candidates_examples
        example_prompt = PromptTemplate.from_template("CANDIDATES: {candidates}\nKEYWORDS: {keywords}")

        prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt = example_prompt,
        prefix = """
        You are an excellent English Key word extractor.
        Your role is to extract one to three KEYWORDS from a given CANDIDATES.
        Basically, extract from the words in CANDIDATES, but if there is a word that shows features of CANDIDATES well, include that word.
        Each keyword should consist of one or two words.
        Ensure that the output is separated by commas and contains no further explanation.
        """,
        
        suffix="CANDIDATES: {candidates}\nKEYWORDS: ",)

        final_prompt = prompt.format(candidates = ', '.join(candidates))

        return final_prompt

    def make_prompt_for_category(self, keywords: List[str]) -> str:
        """
        keywords를 받아 LLM에게 전송할 프롬프트를 만드는 함수입니다.
        (HashtaggingModule의 get_keywords_from_category 함수에 사용되는 프롬프트를 만드는 함수입니다.)
        
        Parameters:
        keywords (List[str]): category를 뽑는데 사용될 keywords들
        
        Returns:
        final_prompt (str): LLM 모델에게 전송할 프롬프트
        """
        examples = fewshot_examples.category_examples

        example_prompt = PromptTemplate.from_template("KEYWORDS: {keywords}\nFIELDS:{active_category}\nCATEGORY: {final_category}")

        prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix="""
            You are an excellent English Keyword Classifier.
            Your role is to check KEYWORDS and then choose one or two CATEGORY from FIELDS that best represents the words in KEYWORDS.
            CATEGORY must be selected from the words in FIELDS.
            Even if there is no proper CATEGORY in FIELDS, force to choose one.
            Ensure that the output is separated by commas and contains no further explanation.
            """,
            suffix="KEYWORDS: {keywords}\nFIELDS: {fields}\nCATEGORY: ",
        )

        # get_category_from_json 메서드 호출로 fields 가져오기
        fields = self.get_category_from_json()
        final_prompt = prompt.format(fields=', '.join(fields), keywords=', '.join(keywords))

        return final_prompt
    
    def get_category_from_json(self) -> List[str]:
        # category에 정의된 active한 항목을 찾아 리스트로 반환하는 함수입니다.
        file_path = self.category_json_file_path
        data = json.loads(Path(file_path).read_text())
        
        return [field['name'] for field in data if field['active']]
    
    def make_prompt_for_postprocess(self, keywords: List[str]) -> str:
        """
        keywords를 받아 LLM에게 전송할 프롬프트를 만드는 함수입니다.
        (HashtaggingModule의 postprocess_keywords 함수에 사용되는 프롬프트를 만드는 함수입니다.)
        
        Parameters:
        keywords (List[str]): 추출된 keywords
        
        Returns:
        final_prompt (str): LLM 모델에게 전송할 프롬프트
        """
        examples = fewshot_examples.postprocess_examples
        example_prompt = PromptTemplate.from_template("BEFORE_KEYWORDS: {keywords}\nAFTER_KEYWORDS: {hashtags}")

        prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt = example_prompt,
        prefix = """
        You are an excellent English Keyword extractor.
        Even if the form or structure is different, such as singular/plural form or abbreviation, only one word with similar meaning is left and removed.
        when removing duplicate words, the form of the word to be left is not converted.
        Ensure that the output is separated by commas and contains no further explanation.
        """,
        
        suffix="BEFORE_KEYWORDS: {keywords}\nAFTER_KEYWORDS: ")

        final_prompt = prompt.format(keywords=', '.join(keywords))

        return final_prompt