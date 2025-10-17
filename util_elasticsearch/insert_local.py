import hashlib
from opensearchpy import OpenSearch, RequestsHttpConnection
import pandas as pd

# ec2에서 실행

class OpenSearchManager:
    def __init__(self):
        self.index_name = "article_infos"
        self.backup_file_path = "./article_infos.pkl"

        # OpenSearch 클라이언트 초기화
        self.client = OpenSearch(
            hosts=[{'host': 'localhost', 'port': 9200}],
            http_auth=('elastic', '1234'),
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False,
            connection_class=RequestsHttpConnection
        )

    def get_document_id(self, url):
        """URL로부터 SHA-256 해시를 사용하여 문서 ID 생성."""
        hasher = hashlib.sha256()
        hasher.update(url.encode('utf-8'))  # URL을 바이트로 인코딩
        return hasher.hexdigest()  # 16진수 다이제스트 반환

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

# 사용 예시
if __name__ == "__main__":
    manager = OpenSearchManager()
    manager.insert_backup_data()
