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
            connection_class=RequestsHttpConnection,
            timeout=30  # 30초로 타임아웃 설정
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

    def search_articles(self, params):
        """
        주어진 파라미터를 사용하여 기사를 검색합니다.
        
        :param params: utils.SearchParams 객체
        :return: 검색 결과
        """
        query = self.build_search_query(params)
        
        try:
            response = self.client.search(
                index=self.index_name,
                body=query
            )
            return response['hits']
        except Exception as e:
            print(f"Search failed: {e}")
            return None

    def build_search_query(self, params):
        filter_clauses = []
        must_clauses = []

        # Hashtags query (AND condition) using keyword field
        if params['hashtags']:
            hashtag_clauses = [
                {"term": {"hashtags.keyword": hashtag}}
                for hashtag in params['hashtags']
            ]
            filter_clauses.append({"bool": {"filter": hashtag_clauses}})

        # Company name query
        if params['company']:
            filter_clauses.append({"term": {"company_name": params['company']}})

        # Determine the sorting criteria based on the presence of a search query
        sort_criteria = []
        if params['query']:
            must_clauses.append({
                "multi_match": {
                    "query": params['query'],
                    "fields": ["title^3", "summarized_text^2", "hashtags"],
                    "type": "best_fields",
                    "operator": "or",
                    "fuzziness": "AUTO",
                    "prefix_length": 3,
                    "max_expansions": 10,
                }
            })
            sort_criteria = [
                {"_score": {"order": "desc"}},
                {"pub_date": {"order": "desc"}},
            ]
        else:
            sort_criteria = [{"pub_date": {"order": "desc"}}]

        query = {
            "bool": {
                "filter": filter_clauses,
                "must": must_clauses,
            }
        }

        return {
            "query": query,
            "from": 0 * 10,
            "size": 10,
            "sort": sort_criteria,
        }

'''
https://techblog.lycorp.co.jp/ko/define-and-manage-kubernetes-custom-resources-with-controller
https://techblog.lycorp.co.jp/ko/increase-vm-performance-to-reduce-global-warming
http://labs.brandi.co.kr//2024/08/23/shinnr.html
https://tech.kakao.com/posts/654
'''


# 사용 예시
if __name__ == "__main__":
    index_name = 'article_infos'
    params = {'hashtags': [], 'query': "", "company" : ""}
    
    opensearch_manager = OpenSearchManager(index_name)

    # opensearch_manager.get_current_settings()
    # opensearch_manager.save_all_urls_to_file()
    opensearch_manager.backup_data()
    # print(opensearch_manager.search_articles(params))
    # print(opensearch_manager.count_documents())
    # opensearch_manager.delete_index()
    # opensearch_manager.create_index()
    # opensearch_manager.get_current_settings()
    # opensearch_manager.insert_backup_data()
    # opensearch_manager.save_all_urls_to_file()
    # print(opensearch_manager.count_documents())

    # url = "https://techblog.lycorp.co.jp/ko/define-and-manage-kubernetes-custom-resources-with-controller"
    # hashtags = ['Infra', 'Kubernetes', 'Controller', 'ResourceManagement', 'CustomResource']
    # opensearch_manager.update_document(url, hashtags=hashtags, summarized_text=None)

    # url = "https://techblog.lycorp.co.jp/ko/increase-vm-performance-to-reduce-global-warming"
    # summarized_text = "가상 머신의 성능 문제를 분석하고 개선 방법을 제시하는 글입니다.\n목차:\n1. 가상 머신과 물리 서버의 성능 비교\n2. 가상 머신 성능 문제 발견 과정\n3. 성능 측정 및 분석\n4. 가상 머신 성능 개선 방안\n5. 가상 머신의 환경적 이점\n6. 결론 및 향후 방향"
    # opensearch_manager.update_document(url, hashtags=None, summarized_text=summarized_text)

    # url = "http://labs.brandi.co.kr//2024/08/23/shinnr.html"
    # summarized_text = "혼자서 검색 시스템을 구축하고 운영하는 방법에 대한 경험과 노하우를 공유하는 글입니다.\n목차:\n1. 검색 시스템 구축 배경\n2. 검색 파이프라인 도입기\n3. 데이터 엔지니어링 관점에서의 검색 데이터 파이프라인\n4. 증분 색인 도입기\n5. 검색 API 개발\n6. 모니터링 및 관리\n7. 클라우드와 온프레미스 비교\n8. 향후 계획\n9. 마무리 및 감사의 말"
    # opensearch_manager.update_document(url, hashtags=None, summarized_text=summarized_text)

    # url = "https://tech.kakao.com/posts/654"
    # summarized_text = "if(kakaoAI)2024에서 진행되는 모바일 기술 세션에 대한 소개입니다.\n목차:\n1. if(kakaoAI)2024 개요\n2. 모바일 기술 세션 일정\n3. 세션 장소 및 트랙 정보\n4. 관련 기술 세션 목록"
    # opensearch_manager.update_document(url, hashtags=None, summarized_text=summarized_text)


    # # 3. 모든 URL 가져오기 및 파일에 저장
    # opensearch_manager.save_all_urls_to_file()

    # # 전체 문서 수 출력 예시 (사용자 호출)
    # total_documents_count = opensearch_manager.count_documents()
    # if total_documents_count is not None:
    #      print(f"Total number of documents in the index: {total_documents_count}")