from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import os
from dotenv import load_dotenv
import pandas as pd

# ec2에 원격 접속해 해당 프로그램 실행

# .env 파일 로드
load_dotenv()

region = os.getenv('AWS_REGION')
host = os.getenv('OPENSEARCH_HOST')
service = 'es'
index_name = 'article_infos'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

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

# pickle 파일로 저장
file_path = os.path.join(os.path.dirname(__file__), "article_infos.pkl")
df.to_pickle(file_path)