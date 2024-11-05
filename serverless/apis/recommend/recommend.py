import json
import os
from typing import List, Dict, Any
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# AWS 및 OpenSearch 설정
region = os.getenv('AWS_REGION')
host = os.getenv('OPENSEARCH_HOST')
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

def validate_url(url: str) -> bool:
    """
    주어진 URL이 OpenSearch에 존재하는지 검증하는 함수입니다.

    Parameters:
    url (str): 검증할 URL입니다.

    Returns:
    bool: URL이 존재하면 True, 그렇지 않으면 False를 반환합니다.
    """
    response = client.search(
        index=index_name,
        body={
            "query": {
                "match": {
                    "url": url
                }
            }
        }
    )
    
    return response['hits']['total']['value'] > 0

def get_recommend_articles_by_url(url: str) -> List[Dict[str, Any]]:
    """
    사용자가 방문한 기술 블로그 게시글 URL을 받아 추천할 게시글들을 반환하는 함수입니다.

    Parameters:
    url (str): 사용자가 방문한 게시글의 URL입니다.
    
    Returns:
    List[Dict[str, Any]]: 
        - 유사한 게시글의 정보를 담고 있는 딕셔너리 리스트입니다.
        - 각 딕셔너리는 다음과 같은 키를 포함합니다:
            - "title" : 게시글 제목
            - "pubDate" : 게시일
            - "companyName" : 게시글을 작성한 회사 이름
            - "url" : 게시글 URL
            - "summarizedText" : 게시글 요약
            - "hashtags" : 게시글의 해시태그 리스트 ex) ['Backend', 'Infra']

    return 예시:
        [
            {
                "title": "Understanding Backend Architecture",
                "pubDate": "2023-11-06",
                "companyName": "someCompany1",
                "url": "https://techinsights.com/backend-architecture",
                "summarizedText": "This article explores the fundamentals of backend architecture...",
                "hashtags": ["Backend", "Architecture", "Tech"]
            },
            {
                "title": "Infrastructure as Code: Best Practices",
                "pubDate": "2023-11-05",
                "companyName": "someCompany2",
                "url": "https://devopsweekly.com/infrastructure-as-code",
                "summarizedText": "Learn how to manage your infrastructure through code...",
                "hashtags": ["Infra", "DevOps", "Automation"]
            }
        ]
    """
    
    # bigquery 폴더의 사용자 로그 기반 추천 모듈 이용
    # opensearch 폴더의 컨텐츠 기반 추천 모듈 이용

    return None

def create_response(message: str, article_infos: List[Dict[str, Any]]) -> Dict[str, Any]:
    response = {
        "message": message,
        "articleInfos": article_infos
    }
    return response

def lambda_handler(event, context):
    try:
        url = event.get('queryStringParameters', {}).get('url')
        
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps(create_response("URL parameter is missing", [])),
                'headers': {'Content-Type': 'application/json'}
            }

        # URL 검증
        if not validate_url(url):
            return {
                'statusCode': 400,
                'body': json.dumps(create_response("No articles found for the given URL", [])),
                'headers': {'Content-Type': 'application/json'}
            }

        articles = get_recommend_articles_by_url(url)

        response = create_response("success", articles)

        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(create_response(str(e), [])),
            'headers': {
                'Content-Type': 'application/json'
            }
        }