import os
import pickle
import numpy as np
import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account
from als_train_model import ALSTrainModel
from ga4_log_preprocessor import GA4LogPreprocessor

class RecommenderTrainer:
    def __init__(self, f, reg_param, iters, a):
        # 모델 및 학습 준비
        print("Initialize..")
        self.model = ALSTrainModel(factors=f, regularization=reg_param, iterations=iters, alpha=a)
        self.user_logs = None
        self.user_item_matrix = None
        self.user_latent_matrix = None
        self.item_latent_matrix = None

        # BigQuery 클라이언트 설정
        file_path = os.path.join(os.path.dirname(__file__), 'bigqueryKey.json')
        credentials = service_account.Credentials.from_service_account_file(file_path)
        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 학습 전체 과정 수행. caution - 현재 시점에서 저장되어있는 게시글 정보 기반 학습
    def execute(self):
        print("Get user logs from bigquery..")
        self.user_logs = self.get_logs_from_bigquery()

        self.preprocess()

        self.make_user_item_matrix(self.user_logs)

        print("Execute training..")
        self.train()
        
        # self.transform_user_latent_matrix()
        self.transform_item_latent_matrix()

        self.save_data()
        
        print("Execute Complete")

    def get_logs_from_bigquery(self):
        # 데이터셋 목록 가져오기
        datasets = list(self.client.list_datasets())

        # 전체 결과를 저장할 DataFrame 초기화
        total_df = pd.DataFrame()

        # 각 데이터셋의 테이블을 순회
        for dataset in datasets:
            tables = list(self.client.list_tables(dataset.reference))
            for table in tables:
                # 테이블 이름이 'events_'로 시작하는 경우만 선택
                if table.table_id.startswith('events_'):
                    query = f"""
                    SELECT event_timestamp, event_name, event_params, user_pseudo_id
                    FROM `{dataset.dataset_id}.{table.table_id}`
                    """
                    
                    try:
                        # 쿼리 결과를 DataFrame으로 변환 후 병합
                        df = self.client.query(query).to_dataframe()
                        total_df = pd.concat([total_df, df], ignore_index=True)
                    except Exception as e:
                        print(f"Error querying table {table.table_id}: {str(e)}")

        return total_df
    
    # 획득한 로그에서 사전 정의한 부적절한 로그 제거
    def preprocess(self):
        ga4_preprocessor = GA4LogPreprocessor(self.user_logs)
        ga4_preprocessor.preprocess()
        self.user_logs = ga4_preprocessor.logs

    # 로그 기반 user-item matrix 제작
    def make_user_item_matrix(self, user_log_df: pd.DataFrame):
        """
        user_log_df schema
        event_timestamp, event_name, event_params, user_pseudo_id
        """
        # 각 행을 순회, post_click과 summary_click을 만나면 dict를 탐색하며 user_item_matrix를 추가
        # article_num은 pkl 까봐야 알 듯..

        # matrix size 결정
        file_path = os.path.join(os.path.dirname(__file__), 'recommend_utils', 'article_infos.pkl')
        with open(file_path, 'rb') as f:
            article_info_df = pickle.load(f)
        filtered_logs = user_log_df[user_log_df['event_name'].isin(['post_click', 'summary_click'])]

        # article_info_df에서 url 열의 내용 가져오기
        unique_user_names = filtered_logs['user_pseudo_id'].unique()  # 고유한 유저 ID
        article_urls = article_info_df['url'].tolist()  # URL 리스트로 변환

        user_item_matrix = pd.DataFrame(
        data=np.zeros((len(unique_user_names), len(article_urls))),  # 유저 수 x 게시글 크기의 0으로 초기화된 배열
        index=unique_user_names,  # 행 인덱스를 유저 이름으로 설정
        columns=article_urls      # 열 이름을 URL로 설정
        )

        # 각 행을 순회하며 user_item_matrix 값 업데이트
        for _, row in user_log_df.iterrows():
            user_id = row['user_pseudo_id']
            event_name = row['event_name']
            event_params = row['event_params']

            # post_click 또는 summary_toggle_click 이벤트에 대해서만 처리
            if event_name in ['post_click', 'summary_toggle_click']:
                # engagement_time_msec 값을 찾기
                engagement_time_msec = next(
                    (param['value'].get('int_value') for param in event_params if param['key'] == 'engagement_time_msec'),
                    None
                )
                # post_url 값을 찾기
                post_url = next(
                    (param['value'].get('string_value') for param in event_params if param['key'] == 'post_url'),
                    None
                )

                # engagement_time_msec와 post_url이 모두 존재해야 처리
                if engagement_time_msec is not None and post_url is not None:
                    # 이벤트 점수 계산
                    score = self.calc_event_score(event_name, engagement_time_msec)

                    # user_item_matrix에 해당 유저와 URL에 대해 점수 추가
                    if post_url in user_item_matrix.columns and user_id in user_item_matrix.index:
                        user_item_matrix.loc[user_id, post_url] += score

        self.user_item_matrix = user_item_matrix

    def calc_event_score(self, event_name, engagement_time_msec):
        if event_name == "post_click":
            score = 0.5 + min(10000, engagement_time_msec) / 10000
            return round(score, 2)
        elif event_name == "summary_toggle_click":
            score = 0.05 + 0.1 * min(10000, engagement_time_msec) / 10000
            return round(score, 2)
        else:
            return 0

    # ALS 기반 학습 진행
    def train(self):
        """user_itme_matrix DataFrame을 ndarray로 바꾸어야 함"""
        self.model.fit(self.user_item_matrix)
        self.user_latent, self.item_latent_matrix = self.model.get_user_item_factors()

    def transform_item_latent_matrix(self):
        self.item_latent_matrix = pd.DataFrame(self.item_latent_matrix.round(2))
        file_path = os.path.join(os.path.dirname(__file__), 'recommend_utils', 'article_infos.pkl')
        with open(file_path, 'rb') as f:
            article_info_df = pickle.load(f)
        article_urls = article_info_df['url'].tolist()  # URL 리스트로 변환
        self.item_latent_matrix.insert(0, 'url', article_urls)

    # 해당 파일을 지정된 위치에 저장
    def save_data(self):
        # 영행이 아닌 행만 필터링하여 item_latent_matrix 생성
        filtered_item_latent = self.item_latent_matrix.loc[~(self.item_latent_matrix == 0).all(axis=1)]

        file_path = os.path.join(os.path.dirname(__file__), 'recommend_utils', 'trained_article_latent_matrix.pkl')
        filtered_item_latent.to_pickle(file_path)
