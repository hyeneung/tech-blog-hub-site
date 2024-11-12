from google.cloud import bigquery
from google.oauth2 import service_account

# BigQuery 클라이언트 설정
credentials = service_account.Credentials.from_service_account_file('recommendAPIBigQueryKey.json')
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# 데이터셋 목록 가져오기
datasets = list(client.list_datasets())

for dataset in datasets:
    print(f"\nDataset: {dataset.dataset_id}")
    
    # 각 데이터셋의 테이블 목록 가져오기
    tables = list(client.list_tables(dataset.reference))
    for table in tables:
        print(f"\nTable: {table.table_id}")
        
        # 테이블의 전체 행을 가져와 DataFrame으로 변환
        query = f"""
        SELECT *
        FROM `{dataset.dataset_id}.{table.table_id}`
        """
        
        try:
            df = client.query(query).to_dataframe()
            print("\nFirst 5 rows:")
            print(df.head())
            print("\nColumn names:")
            print(df.columns.tolist())
            print(f"\nShape: {df.shape}")
        except Exception as e:
            print(f"Error querying table {table.table_id}: {str(e)}")