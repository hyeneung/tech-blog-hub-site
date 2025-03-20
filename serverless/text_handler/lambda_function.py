import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from typing import List, Tuple

from hashtag.hashtaggingModule import HashtaggingModule
from summarize.summarizeModule import SummarizeModule
from utils.preprocess import get_preprocessed_text

API_KEY = os.environ['LLM_API_KEY']

summarize_module = SummarizeModule(API_KEY)
hashtagging_module = HashtaggingModule(API_KEY)
executor = ThreadPoolExecutor(max_workers=10)

async def process_text(preprocessed_text_with_subtitle: str, preprocessed_text : str) -> Tuple[str, List[str]]:
    summarize_task = asyncio.create_task(summarize_url(preprocessed_text))
    hashtag_task = asyncio.create_task(generate_hashtags(preprocessed_text_with_subtitle))

    try:
        summarized_text, hashtags = await asyncio.wait_for(
            asyncio.gather(summarize_task, hashtag_task),
            timeout=300
        )
    except asyncio.TimeoutError:
        print("Operation timed out after 5 minutes")

    return summarized_text, hashtags

async def summarize_url(preprocessed_text: str) -> str:
    summarize_module.init_token_usage()
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(executor, summarize_module.summarize, preprocessed_text)
    except Exception as e:
        return f"Summarization failed: {str(e)}"

async def generate_hashtags(preprocessed_text: str) -> List[str]:
    hashtagging_module.init_token_usage()
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(executor, hashtagging_module.generate_hashtags, preprocessed_text)
    except Exception as e:
        return [f"Hashtag generation failed: {str(e)}"]

def lambda_handler(event, context):
    try:
        # URL을 이벤트에서 추출
        url = event['url']

        print(f"processing {url}")
        # 텍스트 전처리
        preprocessed_text_with_subtitle, preprocessed_text = get_preprocessed_text(url)

        # 비동기 처리 실행
        summarized_text, hashtags = asyncio.run(process_text(preprocessed_text_with_subtitle, preprocessed_text))

        # 결과 로그 남김
        total_cost = hashtagging_module.get_total_api_cost() + summarize_module.get_total_api_cost()
        print(f'url : {url}, hashtags : {hashtags}, summarized_text : {summarized_text}, LLM API 비용 : {total_cost}')

        # 결과 반환
        return {
            'statusCode': 200,
            'body': json.dumps({
                'summarized_text': summarized_text,
                'hashtags': hashtags
            })
        }
    except Exception as e:
        print(f"Error in text_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }