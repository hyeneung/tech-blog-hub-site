import json
import os
from typing import Dict, Any, Tuple
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from aws_xray_sdk.core import xray_recorder
import pandas as pd
import json
from model import ALSModel

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

def lambda_handler(event, context):
    # 모든 데이터 검색
    query = {
        "query": {
            "match_all": {}
        },
        "size": 10000  # 검색 결과의 최대 크기 설정
    }

    response = client.search(
        body = query,
        index = index_name
    )

    # 검색 결과를 DataFrame으로 변환
    hits = response['hits']['hits']
    data = [hit['_source'] for hit in hits]
    df = pd.DataFrame(data)
    article_url_list = df['url'].tolist()
    try:
        # RecommenderTrainer 인스턴스 생성
        trainer = ALSModel(f=100, reg_param=0.1, iters=20, a=40, article_url_list=article_url_list)
        
        # execute 메서드 실행
        trainer.execute()
        
        return {
            'statusCode': 200,
            'body': json.dumps('RecommenderTrainer execution completed successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error occurred: {str(e)}')
        }