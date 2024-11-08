import json
import re
from math import ceil, floor
from typing import List, Tuple
from pathlib import Path

from openai import OpenAI

# CAUTION : get_preprocessed_text를 통해 얻어진 텍스트에 맞춰 함수 작성 -> 해당 함수 return 형식이 달라지면 버그 발생 가능성 있음
from hashtag.text_processing_utils import TextProcessingUtils
from hashtag.llm_request_utils import LLMRequestUtils

class HashtaggingModule:
    def __init__(self, api_key):
        self.text_process_utils = TextProcessingUtils()
        self.llm_utils = LLMRequestUtils()
        self.api_key = api_key
        self.input_token = 0
        self.output_token = 0
    
    # 싱글턴 클래스. 재사용될 시 초기화
    def init_token_usage(self):
        self.input_token = 0
        self.output_token = 0

    def __add_input_token_usage(self, usage):
        self.input_token += usage

    def __add_output_token_usage(self, usage):
        self.output_token += usage

    def get_total_api_cost(self):
        ex_rate = 1380
        input_cost = (0.15 / 1000000) * self.input_token
        output_cost = (0.6 / 1000000) * self.output_token
        return (input_cost + output_cost) * ex_rate
    
    def run_llm_request(self, prompt: str, token_label: str = "Token") -> List[str]:
        # LLM 요청을 보내고 응답에서 키워드를 추출하는 Helper 함수 (token_label로 요청 구분)
        messages = [
            {"role": "user", "content": prompt}
        ]
        responses = OpenAI(api_key=self.api_key).chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
        )
        self.__add_input_token_usage(responses.usage.prompt_tokens)
        self.__add_output_token_usage(responses.usage.completion_tokens)
        return responses.choices[0].message.content.split(', ')


    def get_keywords_from_intro(self, intro_blocks: List[List[Tuple[str, str]]]) -> List[str]:
        """
        Intro에 해당하는 block들을 받아 LLM을 통해 keywords를 추출하는 함수입니다.

        Parameters:
        intro_blocks (List[List[Tuple[str, str]]]): Intro에 해당하는 block들
        
        Returns:
        List[str]: LLM 모델이 선정한 keywords 리스트
        """
        final_prompt = self.llm_utils.make_prompt_for_intro_blocks(intro_blocks=intro_blocks)
        return self.run_llm_request(final_prompt, token_label="INTRO TOKEN")


    def get_candidates_from_block(self, body_block: List[Tuple[str, str]]) -> List[str]:
        """
        body에 해당하는 특정 block을 입력받아 LLM을 통해 keywords를 추출하는 함수입니다.

        Parameters:
        body_block (List[Tuple[str, str]]): 분석하고자 하는 body에 해당하는 block
        
        Returns:
        List[str]: LLM 모델이 선정한 keywords 리스트
        """
        final_prompt = self.llm_utils.make_prompt_for_unit_block(body_block=body_block)
        return self.run_llm_request(final_prompt, token_label="BLOCK TOKEN")


    def make_keywords_from_candidates(self, candidates: List[str]) -> List[str]:
        """
        여러 block들에서 모아진 keywords들(candidates)를 받아 LLM을 통해 적절한 keywords만을 재추출하는 함수입니다.

        Parameters:
        candidates (List[str]): 기존의 여러 block들에서 추출된 keywords들이 모인 리스트
        
        Returns:
        List[str]: LLM 모델이 선정한 keywords 리스트
        """
        final_prompt = self.llm_utils.make_prompt_for_candidates(candidates)
        return self.run_llm_request(final_prompt, token_label="CANDIDATES TOKEN")


    # CAUTION - Not currently used : generate_hashtags에 사용되지는 않은 함수, body에서 keywords를 잘 뽑아내는 지 중간 테스트용으로 사용
    def get_keywords_from_body(self, body: List[List[Tuple[str, str]]]) -> List[str]:
        """
        body 부분에 해당되는 block들을 입력받아, LLM을 통해 적절한 keywords을 재추출하는 함수입니다.
        (반드시, body 부분에 해당되는 blocks list만 입력받아야 합니다.)

        Parameters:
        body (List[List[Tuple[str, str]]]): 전처리된 텍스트에서 body에 해당되는 block들의 list
        
        Returns:
        List[str]: LLM 모델이 선정한 keywords 리스트
        """
        total_candidates = []

        for block in body:
            candidates = self.get_candidates_from_block(block)
            total_candidates = total_candidates + candidates
        
        return self.make_keywords_from_candidates(total_candidates)


    def get_keywords_from_category(self, keywords: List[str]) -> List[str]:
        """
        keywords를 입력받아, keywords의 내용을 바탕으로 하여
        category json에 정의된 active한 분류 중 적절한 분류를 추출하는 함수

        Parameters:
        keywords (List[str]) : 사전추출이 완료된 핵심단어 리스트
        
        Returns:
        result (List[str]) : category에 정의된 분류 중, 적절한 분류 리스트
        """
        final_prompt = self.llm_utils.make_prompt_for_category(keywords)
        return self.run_llm_request(final_prompt, token_label="CATEGORY TOKEN")

    
    def dedup_list(self, keywords:List[str]) -> List[str]:
        # keywords 내에 동일한 글자를 가진 단어가 여러개라면, 한 단어만 남기고 나머지를 제거하는 함수입니다.
        # 함수의 예시는 다음과 같습니다: ["machine learning, MachineLearning", "Deep Learning"] -> ["machine Learning", "Deep Learning"]
        dedup_dict = {}
        
        for word in keywords:
            standard_word = word.lower().replace(" ", "")
            if standard_word not in dedup_dict:
                dedup_dict[standard_word] = word
        
        return list(dedup_dict.values())


    def sort_hashtags_by_category_order(self, hashtags: List[str]) -> List[str]:
        """
        category_file_path에 명시된 순서대로 정렬된 해시태그 리스트를 반환합니다.
        (해당 파일에 포함되지 않은 해시태그는 후위로 배치됩니다.)
        
        Parameters:
            hashtags (List[str]): 추출된 해시태그 리스트
            category_file_path (str): category가 정의되어 있는 파일의 위치
            
        Returns:
            List[str] : 정렬된 해시태그 리스트
        """
        # JSON 파일에서 카테고리 순서 로드
        category_file_path = Path(__file__).parent / "category.json"
        with open(category_file_path, 'r') as file:
            categories = json.load(file)
        
        # JSON에 있는 카테고리 순서에 맞춰 정렬 순서 리스트 생성
        category_order = [category['name'] for category in categories]
        
        # 정렬 수행: JSON에 명시된 순서에 있는 해시태그는 해당 순서대로, 없는 해시태그는 후순위
        return sorted(hashtags, key=lambda x: (x not in category_order, category_order.index(x) if x in category_order else float('inf')))


    def postprocess_keywords(self, keywords: List[str]) -> List[str]:
        """
        get_keywords 계열 함수를 통해 얻어진 keywords를 모아, 후처리하여 최종 해시태그 리스트를 반환하는 함수입니다.

        Parameters:
        keywords (List[str]): 해시태그로 추출될 최종 후보군
        
        Returns:
        List[str]: 후처리된 keywords (= 최종 해시태그)
        """
        cleaned_keywords = keywords  # 초기 입력 keywords를 클린업하여 저장할 변수

        # 이상 단어 제거
        cleaned_keywords = [re.sub(r'KEYWORDS: ', '', hashtag, flags=re.IGNORECASE) if "KEYWORDS: " in hashtag.upper() else hashtag for hashtag in cleaned_keywords]
        cleaned_keywords = [re.sub(r'CATEGORY: ', '', hashtag, flags=re.IGNORECASE) if "CATEGORY: " in hashtag.upper() else hashtag for hashtag in cleaned_keywords]
        cleaned_keywords = [item for item in cleaned_keywords if not re.search(r'[가-힣]', item)]

        # 블랙리스트 단어 제거
        """
        모델 성능에 따라서 필요없다고 판단될 시, 이 부분은 제거되어도 괜찮습니다.
        """
        blacklist = ["Kurly", "TechBlog", "Blog"]
        filtered_keywords = [word for word in cleaned_keywords if word not in blacklist]

        # LLM에 보내기 전에, 키워드가 비어 있을 경우 대비
        if not filtered_keywords:
            return ["ExperienceArticle"]

        # 중복 키워드 제거
        unique_keywords = self.dedup_list(filtered_keywords)

        # 의미적으로 동일한 키워드 제거 (ex. AI & Artificial Intelligence)
        """
        200토큰 정도밖에 사용안하긴 하지만, 효율이 많이 떨어지는 것으로 추정됩니다.
        경험적이든 실증적이든 딱히 남길 이유가 없다고 판단될 시 이 부분은 제거될 예정입니다.
        """
        final_prompt = self.llm_utils.make_prompt_for_postprocess(unique_keywords)
        processed_keywords = self.run_llm_request(final_prompt, token_label="POSTPROCESS TOKEN")

        # 비정상적으로 긴 단어 제거
        LENGTH_THROSHOLD = 25
        processed_keywords = [word for word in processed_keywords if len(word) <= LENGTH_THROSHOLD]

        # 형식 변환 (Camel Case로 변환)
        final_hashtags = self.text_process_utils.to_camel_case(processed_keywords)

        return self.sort_hashtags_by_category_order(final_hashtags)


    def generate_hashtags(self, html_text: str) -> List[str]:
        """
        전처리된 텍스트를 받아 해시태그를 추출하는 함수입니다.

        Parameters:
        html_text (str): 전처리된 html text
        
        Returns:
        List[str]: 추출된 해시태그 list
        """
        parsed_list = self.text_process_utils.make_blocks_from_preprocessed_text(html_text)
        
        NUM_PARAGRAPHS_TRESHOLD = 5 # 어떤 이유로 파싱에 실패하거나, 글의 길이가 짧은 경우에 해당하는 최소 문단 수
        FOOTER_RATIO = 0.1  # 글의 마지막 부분 중 분석에서 제외할 비율 (마무리나 글쓴이의 프로필 정보 등 불필요한 부분)
        n = len(parsed_list)
        footer_length = ceil(FOOTER_RATIO * n)
        extract_ratio = 0.75 # body_part에서 추출할 비율

        intro_keywords, candidates, body_keywords, category_keywords = [], [], [], []

        if n < NUM_PARAGRAPHS_TRESHOLD:
            # intro_keywords = [] (intro_keywords는 추출 생략)
            extracted_part = max(parsed_list, key=lambda x: len(x[1][1])) # 가장 긴 block에 대하여 추출
            if extracted_part[0][0] != 'Title':
                title = parsed_list[0][0][1]
                extracted_part = [('Subtitle', f"{title}, {extracted_part[0][1]}"), extracted_part[1]]
            body_keywords = self.get_candidates_from_block(extracted_part)
            candidates = body_keywords # 후보군 = 가장 긴 block의 keywords로 대체
        else:
            intro_part = parsed_list[:2]
            body_part = parsed_list[2:-footer_length]
            
            intro_keywords = self.get_keywords_from_intro(intro_part)
            body_part = self.text_process_utils.make_merged_block_list(body_part)

            b = ceil(extract_ratio * len(body_part))
            extracted_part = sorted(body_part, key=lambda x: len(x[1][1]), reverse=True)[:b]
            for block in extracted_part:
                candidates.extend(self.get_candidates_from_block(block))
            body_keywords = self.make_keywords_from_candidates(candidates=candidates)
        
        # candidates를 통해 category 선정
        category_keywords = self.get_keywords_from_category(candidates)

        hashtags = self.dedup_list(self.postprocess_keywords(intro_keywords + body_keywords) + category_keywords)

        return self.sort_hashtags_by_category_order(hashtags=hashtags)