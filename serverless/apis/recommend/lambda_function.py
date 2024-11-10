import json
import os
from typing import Dict, Any, Tuple
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

from recommend import get_recommend_articles_by_url

# AWS 및 OpenSearch 설정
host = os.getenv('OPENSEARCH_HOST')
region = 'ap-northeast-2'
service = 'es'
index_name = 'article_infos'

# AWS 인증 정보 가져오기
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)

# OpenSearch 클라이언트 초기화
client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def get_current_article_by_url(url: str) -> Tuple[bool, Dict[str, Any]]:
    """
    주어진 URL에 대해 opensearch의 document를 가져오는 함수입니다.

    Parameters:
    url (str): URL

    Returns:
    Tuple[bool, Dict[str, Any]]: URL이 존재하면 (True, 데이터)를, 그렇지 않으면 (False, 빈 딕셔너리)를 반환합니다.
    """
    query = {
        "query": {
            "match": {
                "url": url
            }
        }
    }

    # X-Ray 서브세션 시작
    subsegment = xray_recorder.begin_subsegment('DBQuery')

    try:
        response = client.search(
            body=query,
            index=index_name
        )

        hits = response['hits']['hits']
        if hits:
            source = hits[0]['_source']
            return True, {
                "title": source['title'],
                "pub_date": source['pub_date'],
                "company_name": source['company_name'],
                "url": source['url'],
                "summarized_text": source['summarized_text'],
                "hashtags": source['hashtags']
            }
        else:
            return False, {}

    except Exception as e:
        print(f"Error querying OpenSearch: {e}")
        return False, {}

    finally:
        # 서브세션 종료
        xray_recorder.end_subsegment()

def create_response(message: str, body: Dict[str, Any]) -> Dict[str, Any]:
    response = {
        "message": message,
        "body": body
    }
    return response

def lambda_handler(event, context):
    # 전체 Lambda 실행 시간 측정을 위한 서브세션 시작
    segment = xray_recorder.begin_segment('recommendAPI')
    try:
        url = event.get('queryStringParameters', {}).get('url')
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps(create_response("URL parameter is missing", {})),
                'headers': {'Content-Type': 'application/json'}
            }

        isExist, current_article = get_current_article_by_url(url)
        if not isExist:
            return {
                'statusCode': 404,
                'body': json.dumps(create_response("No articles found for the given URL", {})),
                'headers': {'Content-Type': 'application/json'}
            }
        

        # 추천 로직 수행
        recommend_subsegment = xray_recorder.begin_subsegment('CoreLogic')
        try:
            recommend_articles = get_recommend_articles_by_url(url)
        finally:
            xray_recorder.end_subsegment()

        response_body = {
            "recommend" : recommend_articles,
            "current" : current_article
        }

        # 추천 결과 로그 남김
        recommend_urls = [article['url'] for article in recommend_articles]
        print(f"current : {current_article['url']}\nrecommend:{recommend_urls}")

        return {
            'statusCode': 200,
            'body': json.dumps(create_response("success", response_body)),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(create_response(str(e), {})),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    finally:
        # 전체 Lambda 실행 세그먼트 종료
        xray_recorder.end_segment()