import pandas as pd
import hashlib
import json
from elasticsearch import Elasticsearch
from pathlib import Path
from datetime import datetime

class ElasticsearchManager:
    def __init__(self, index_name):
        self.host = "13.209.155.193"
        self.port = 9200
        self.username = "elastic"
        self.password = "1234"
        
        # SSL 컨텍스트 생성
        # ssl_context = ssl.create_default_context(cafile="./ca.crt")
        
        # Elasticsearch 클라이언트 초기화
        self.client = Elasticsearch(
            [f"https://{self.host}:{self.port}"],
            basic_auth=(self.username, self.password),
            verify_certs=False,
            ssl_show_warn=False
        )
        
        self.index_name = index_name
        
        # 파일 경로 설정
        self.settings_file_path = Path(__file__).parent / "data" / "index_settings.json"
        self.backup_file_path = Path(__file__).parent / "data" / "article_infos.pkl"

    def get_document_id(self, url):
        """URL로부터 SHA-256 해시를 사용하여 문서 ID 생성."""
        hasher = hashlib.sha256()
        hasher.update(url.encode('utf-8'))
        return hasher.hexdigest()

    def insert_backup_data(self):
        """pickle 파일에서 데이터를 읽어 Elasticsearch에 삽입합니다."""
        try:
            df = pd.read_pickle(self.backup_file_path)
            
            for _, row in df.iterrows():
                url = row['url']
                doc_id = self.get_document_id(url)
                
                # 문서가 이미 존재하는지 확인
                if self.client.exists(index=self.index_name, id=doc_id):
                    print(f"Document with ID '{doc_id}' already exists. Skipping insertion.")
                    continue
                
                # Elasticsearch에 데이터 삽입
                self.client.index(index=self.index_name, id=doc_id, body=row.to_dict())
            
            print("All new documents inserted successfully.")
        
        except Exception as e:
            print(f"Error loading and inserting data: {e}")
    def print_document_by_url(self, url_to_print):
        """URL을 기반으로 문서 내용을 출력합니다."""
        
        doc_id = self.get_document_id(url_to_print)  # URL로부터 문서 ID 생성
        
        try:
            response = self.client.get(index=self.index_name, id=doc_id)
            
            document = response['_source']  # 문서의 내용을 가져옵니다.
            
            print("Document fields and values:")
            for field, value in document.items():
                print(f"{field}: {repr(value)}")
                
            print("\n")  # 각 문서 사이에 줄바꿈 추가
        
        except Exception as e:
            print(f"Error retrieving document with ID '{doc_id}': {e}")
    
    def search_and_print(self, query=None, hashtags=None, company=None, size=10):
        """
        주어진 매개변수로 검색을 수행하고 결과를 출력합니다.
        
        :param query: 검색어 (선택적)
        :param hashtags: 해시태그 리스트 (선택적)
        :param company: 회사명 (선택적)
        :param size: 반환할 결과의 수 (기본값 10)
        """
        search_body = self.build_search_query(query, hashtags, company, size)
        
        try:
            response = self.client.search(index=self.index_name, body=search_body)
            
            hits = response['hits']['hits']
            total_hits = response['hits']['total']['value']
            
            print(f"총 {total_hits}개의 결과 중 {len(hits)}개 출력:\n")
            
            for hit in hits:
                source = hit['_source']
                print(f"제목: {source['title']}")
                print(f"회사: {source['company_name']}")
                print(f"URL: {source['url']}")
                print(f"요약: {source['summarized_text'][:100]}...")  # 요약 텍스트의 처음 100자만 출력
                print(f"해시태그: {', '.join(source['hashtags'])}")
                print(f"발행일: {source['pub_date']}")
                print("\n")  # 각 문서 사이에 빈 줄 추가
        
        except Exception as e:
            print(f"검색 중 오류 발생: {e}")

    def build_search_query(self, query, hashtags, company, size):
        """검색 쿼리를 구성합니다."""
        must = []
        filter = []

        if query:
            must.append({
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "summarized_text^2", "hashtags"],
                    "type": "best_fields",
                    "operator": "or",
                    "fuzziness": "AUTO",
                    "prefix_length": 3,
                    "max_expansions": 10
                }
            })

        if hashtags:
            for hashtag in hashtags:
                filter.append({"term": {"hashtags.keyword": hashtag}})

        if company:
            filter.append({"term": {"company_name": company}})

        search_body = {
            "query": {
                "bool": {
                    "must": must,
                    "filter": filter
                }
            },
            "size": size,
            "sort": [
                {"_score": {"order": "desc"}},
                {"pub_date": {"order": "desc"}}
            ]
        }

        return search_body
    
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

            # 현재 날짜와 시간을 파일 이름에 추가
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            # file_name = f"{self.backup_file_path[:-len(".pkl")]}_{current_time}.pkl"
            file_name = self.backup_file_path

            # DataFrame을 pickle 파일로 저장
            df.to_pickle(file_name)
            print(f"Data successfully backed up to {file_name}")
        
        except Exception as e:
            print(f"Data search or saving failed: {e}")
    
    def recreate_index_and_restore_data(self):
        """기존 인덱스를 삭제하고, 새로운 설정으로 인덱스를 생성한 후 백업 데이터를 복원합니다."""
        try:
            # 1. 기존 인덱스 삭제
            if self.client.indices.exists(index=self.index_name):
                self.client.indices.delete(index=self.index_name)
                print(f"기존 인덱스 '{self.index_name}' 삭제 완료")

            # 2. 설정 파일에서 새로운 인덱스 설정 읽기
            with open(self.settings_file_path, 'r', encoding='utf-8') as f:
                index_settings = json.load(f)

            # 3. 새로운 인덱스 생성
            self.client.indices.create(index=self.index_name, body=index_settings)
            print(f"새로운 인덱스 '{self.index_name}' 생성 완료")

            # 4. 백업 데이터 복원
            self.insert_backup_data()
            print("백업 데이터 복원 완료")

        except Exception as e:
            print(f"인덱스 재생성 및 데이터 복원 중 오류 발생: {e}")


# 사용 예시
if __name__ == "__main__":
    # es_manager.insert_backup_data() # 복원
    es_manager = ElasticsearchManager("article_infos")
    # es_manager.recreate_index_and_restore_data()
        
    es_manager.backup_data() # 백업 .pkl로 저장
    # 검색 예시
    # es_manager.search_and_print(
    #     query=None,
    #     hashtags=None,
    #     company=None,
    #     size=10
    # )
    
    document_url = "https://medium.com/daangn/%EA%B5%AC%EA%B8%80%EC%B2%98%EB%9F%BC-%EB%B3%B5%EC%9E%A1%ED%95%9C-%EA%B6%8C%ED%95%9C-%EC%89%BD%EA%B2%8C-%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0-feat-graphql-9ce80d34d39b"
    # 요약 정보 수정
    es_manager.print_document_by_url(document_url)
    # summarized_text = "이 글은 Spring 기반 멀티모듈 프로젝트에서 환경변수를 설정하는 다양한 방법을 비교하고, 최적의 방식을 선택하는 과정을 설명합니다.\n\n목차:\n1. 멀티모듈 프로젝트의 정의와 장점\n2. 환경변수 설정의 필요성\n3. 환경변수 설정 방법 소개\n4. spring 기반 멀티 모듈\n5. @PropertySource를 이용한 설정\n6. @Profile과 @PropertySource 조합을 이용한 설정\n7. 결론 및 향후 방향"
    summarized_text = """GraphQL을 활용하여 복잡한 권한 관리를 간소화하는 방법에 대한 글입니다.
목차:
1. 권한 관리의 중요성
2. GraphQL의 기본 개념
3. 복잡한 권한 구조 이해하기
4. GraphQL을 통한 권한 관리 구현
5. 사례 연구: 성공적인 권한 관리
6. 결론 및 향후 전망""" 
    hashtag = ['GraphQL', 'Permissions', 'Management', 'SoftwareEngineering']
    es_manager.update_document(document_url, hashtags=hashtag, summarized_text=summarized_text)
    es_manager.print_document_by_url(document_url)

    