import json
import os
import pandas as pd
import hashlib
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from dotenv import load_dotenv
from pathlib import Path

# NAT instance에 원격 접속하여 해당 코드 실행(VPC 외부에서 opensearch 접근 불가)

class OpenSearchManager:
    def __init__(self, index_name):
        # .env 파일 로드
        load_dotenv()

        self.region = os.getenv('AWS_REGION')
        self.host = os.getenv('OPENSEARCH_HOST')
        self.service = 'es'
        
        # AWS 인증 정보 가져오기
        credentials = boto3.Session().get_credentials()
        self.awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.service,
            session_token=credentials.token
        )

        # OpenSearch 클라이언트 초기화
        self.client = OpenSearch(
            hosts=[{'host': self.host, 'port': 443}],
            http_auth=self.awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
        
        self.index_name = index_name
        
        # 파일 경로 설정
        self.settings_file_path = Path(__file__).parent / "data" / "index_settings.json"
        self.backup_file_path = Path(__file__).parent / "data" / "article_infos.pkl"

    def delete_index(self):
        """인덱스를 삭제합니다."""
        try:
            response = self.client.indices.delete(index=self.index_name)
            print(f"Deleted index: {self.index_name}")
        except Exception as e:
            print(f"Index deletion failed or index does not exist: {e}")

    def create_index(self):
        """새 인덱스를 생성합니다."""
        with open(self.settings_file_path, 'r', encoding='utf-8') as f:
            new_settings = json.load(f)

        try:
            response = self.client.indices.create(index=self.index_name, body=new_settings)
            print(f"Created index: {self.index_name}")
        except Exception as e:
            print(f"Index creation failed: {e}")

    def get_current_settings(self):
        """현재 인덱스 설정을 가져옵니다."""
        try:
            current_settings = self.client.indices.get_settings(index=self.index_name)
            print(f"Current settings for '{self.index_name}':")
            print(json.dumps(current_settings, indent=2))
        except Exception as e:
            print(f"Failed to retrieve current settings: {e}")

    def backup_data(self):
        """모든 데이터를 검색하여 DataFrame으로 변환 후 pickle 파일로 저장합니다."""
        query = {
            "query": {
                "match_all": {}
            },
            "size": 10000  # 검색 결과의 최대 크기 설정
        }

        try:
            response = self.client.search(body=query, index=self.index_name)
            hits = response['hits']['hits']
            data = [hit['_source'] for hit in hits]
            
            # DataFrame으로 변환
            df = pd.DataFrame(data)

            # 결과를 data 폴더에 pickle 파일로 저장
            result_folder = Path(__file__).parent / "data"
            result_folder.mkdir(exist_ok=True)  # data 폴더가 없으면 생성
            
            df.to_pickle(self.backup_file_path)  # 멤버 변수 사용
        
        except Exception as e:
            print(f"Data search or saving failed: {e}")

    def get_document_id(self, url):
        """URL로부터 SHA-256 해시를 사용하여 문서 ID 생성."""
        hasher = hashlib.sha256()
        hasher.update(url.encode('utf-8'))  # URL을 바이트로 인코딩
        return hasher.hexdigest()  # 16진수 다이제스트 반환

    def delete_document_by_url(self, url_to_delete):
        """URL을 기반으로 문서를 삭제합니다."""
        doc_id = self.get_document_id(url_to_delete)  # URL로부터 문서 ID 생성
        
        try:
            response = self.client.delete(index=self.index_name, id=doc_id, refresh='true')  # refresh 추가
            print(f"Document with ID '{doc_id}' deleted successfully.")
        
        except Exception as e:
            print(f"Error deleting document with ID '{doc_id}': {e}")

    def print_document_by_url(self, url_to_print):
        """URL을 기반으로 문서 내용을 출력합니다."""
        
        doc_id = self.get_document_id(url_to_print)  # URL로부터 문서 ID 생성
        
        try:
            response = self.client.get(index=self.index_name, id=doc_id)
            
            document = response['_source']  # 문서의 내용을 가져옵니다.
            
            print("Document fields and values:")
            for field, value in document.items():
                print(f"{field}: {value}")
                
            print("\n")  # 각 문서 사이에 줄바꿈 추가
        
        except Exception as e:
            print(f"Error retrieving document with ID '{doc_id}': {e}")

    def update_document(self, url, hashtags=None, summarized_text=None):
        """Update specific fields of a document identified by its URL."""
        doc_id = self.get_document_id(url)
        
        # Prepare the update body
        update_body = {}
        
        if hashtags is not None:
            update_body['hashtags'] = hashtags
        
        if summarized_text is not None:
            update_body['summarized_text'] = summarized_text
        
        if not update_body:
            print("No fields to update.")
            return
        
        try:
            response = self.client.update(
                index=self.index_name,
                id=doc_id,
                body={
                    "doc": update_body
                }
            )
            print(f"Updated document with ID: {doc_id}")
            print(response)
        except Exception as e:
            print(f"Failed to update document: {e}")

    def save_all_urls_to_file(self, filename='article_urls.txt'):
        """인덱스 내 모든 문서의 URL을 가져와 파일에 저장합니다."""
        
        query = {
            "query": {
                "match_all": {}
            },
            "_source": ["url"]  # URL 필드만 가져오기
        }

        urls = []
        
        # 초기 스크롤 요청
        response = self.client.search(
            body=query,
            index=self.index_name,
            scroll='2m',  # 스크롤 유지 시간
            size=1000  # 한 번에 가져올 문서 수
        )

        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']
        
        urls.extend(hit['_source']['url'] for hit in hits)

        # 남은 결과 스크롤
        while len(hits) > 0:
            response = self.client.scroll(
                scroll_id=scroll_id,
                scroll='2m'
            )
            
            scroll_id = response['_scroll_id']
            hits = response['hits']['hits']
            
            urls.extend(hit['_source']['url'] for hit in hits)

        # URL 목록을 result 폴더에 저장합니다.
        result_folder = Path(__file__).parent / "result"
        result_folder.mkdir(exist_ok=True)  # result 폴더가 없으면 생성
        
        with open(result_folder / filename, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")

    def insert_backup_data(self):
        """pickle 파일에서 데이터를 읽어 OpenSearch에 삽입합니다."""
        
        try:
            df = pd.read_pickle(self.backup_file_path)  # pickle 파일 읽기
            
            for _, row in df.iterrows():
                url = row['url']
                doc_id = self.get_document_id(url)  # ID 생성
                
                # 문서가 이미 존재하는지 확인
                if self.client.exists(index=self.index_name, id=doc_id):
                    print(f"Document with ID '{doc_id}' already exists. Skipping insertion.")
                    continue  # 이미 존재하면 다음 문서로 넘어감
                
                # OpenSearch에 데이터 삽입
                self.client.index(index=self.index_name, id=doc_id, body=row.to_dict())
            
            print("All new documents inserted successfully.")
        
        except Exception as e:
            print(f"Error loading and inserting data: {e}")

    def count_documents(self):
         """OpenSearch 인덱스 내의 전체 문서 수를 반환합니다."""
         try:
             response = self.client.count(index=self.index_name)
             return response['count']  # 전체 문서 수 반환
         except Exception as e:
             print(f"Error counting documents: {e}")
             return None

# 사용 예시
if __name__ == "__main__":
    index_name = 'article_infos'
    
    opensearch_manager = OpenSearchManager(index_name)

    opensearch_manager.print_document_by_url('https://medium.com/prnd/%EC%95%84%EC%9D%B4%EC%BD%98%EC%9D%84-%ED%85%8D%EC%8A%A4%ED%8A%B8-%EA%B0%80%EC%9A%B4%EB%8D%B0%EB%A1%9C-%EC%A0%95%EB%A0%AC%ED%95%98%EA%B8%B0-jetpack-compose-12d3d9d1f28')

    # # 0. 기존 인덱스 삭제
    # opensearch_manager.delete_index()

    # # 1. 새 인덱스 생성
    # opensearch_manager.create_index()    

    # 2. article_infos.pkl에서 데이터 로드 및 OpenSearch에 삽입
    # opensearch_manager.insert_backup_data()
    
    # # 3. 모든 URL 가져오기 및 파일에 저장
    # opensearch_manager.save_all_urls_to_file()

    # # 전체 문서 수 출력 예시 (사용자 호출)
    # total_documents_count = opensearch_manager.count_documents()
    # if total_documents_count is not None:
    #      print(f"Total number of documents in the index: {total_documents_count}")