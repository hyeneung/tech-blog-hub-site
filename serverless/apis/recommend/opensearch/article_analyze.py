from aws_xray_sdk.core import xray_recorder
from opensearchpy import OpenSearch
from itertools import combinations
from random import shuffle
from typing import List, Dict, Any
import pandas as pd

def get_db_dataframe(client: OpenSearch) -> pd.DataFrame:
    # X-Ray 서브세션 시작
    subsegment = xray_recorder.begin_subsegment('DBQueryAll')
    # 모든 데이터 검색
    index_name = 'article_infos'
    query = {
        "query": {
            "match_all": {}
        },
        "size": 10000
    }

    response = client.search(
        body = query,
        index = index_name
    )    
    # 검색 결과를 DataFrame으로 변환
    hits = response['hits']['hits']
    data = [hit['_source'] for hit in hits]
    # X-Ray 서브세션 종료
    xray_recorder.end_subsegment()
    return pd.DataFrame(data)

def get_contents_base_recommendations(client: OpenSearch, input_url: str) -> List[Dict[str, Any]]:
    """
    주어진 URL과 유사한 해시태그를 보유한 URL들을 JSON 형식으로 반환하는 함수입니다.

    Parameters:
        input_url (str): 유사한 URL을 찾고자 하는 기준 URL입니다.

    Returns:
        List[Dict[str, Any]]: 유사한 해시태그를 가진 URL 목록을 JSON 형식으로 반환합니다.
    """
    # X-Ray 서브세션 시작
    subsegment = xray_recorder.begin_subsegment('AnalyzeSimilarity')
    
    df = get_db_dataframe(client)

    # input_url에 해당하는 행 추출
    input_row = df[df['url'] == input_url]
    
    # input_url의 해시태그 목록 추출 및 길이 확인
    input_hashtags = list(input_row['hashtags'].values[0])
    n = len(input_hashtags)
    
    # input_url을 제외한 다른 URL들을 후보 목록으로 설정하고 무작위로 섞기
    candidates = df[df['url'] != input_url].copy()
    candidtates_length = len(candidates)
    candidates = candidates.sample(frac=1).reset_index(drop=True)
    
    # 최대 반환할 URL 개수 설정
    M = 10
    result = []
    
    # 해시태그 부분집합 크기 n에서 1까지 감소시키며 유사한 URL 찾기
    for i in range(n, 0, -1):
        now_result = []
        # 현재 크기 i에 대한 해시태그 부분집합 생성
        n_subsets = list(combinations(input_hashtags, i))
        shuffle(n_subsets)  # 부분집합 순서를 무작위로 섞음

        # 각 부분집합을 포함하는 URL들을 후보 목록에서 찾기
        for subset in n_subsets:
            for j in range(candidtates_length):
                if set(subset).issubset(set(candidates.iloc[j]['hashtags'])):
                    now_result.append(list(candidates.iloc[j]))
        
        # 중복을 피하면서 결과에 추가, M개가 채워지면 중단
        for sublist in now_result:
            if len(result) == M:
                break
            if sublist not in result:
                result.append(sublist)
        
        # 최소 절반 이상이 채워지면 중단
        if len(result) >= M // 2:
            break
    
    # 결과를 JSON 형식으로 변환
    columns = list(df.columns)
    json_data = [dict(zip(columns, item[:len(item)-1])) for item in result] # 'created_at'은 제외

    # X-Ray 서브세션 종료
    xray_recorder.end_subsegment()
    return json_data