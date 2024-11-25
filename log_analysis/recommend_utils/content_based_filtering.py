from random import sample
import os
import pickle
from typing import List, Dict, Any

def hashtags_recommended_urls(n: int, url: str, post_label: str) -> List[Dict[str, Any]]:
    """
    주어진 URL과 유사한 해시태그를 보유한 URL들을 JSON 형식으로 반환하는 함수입니다.

    Parameters:
        n (int): 반환할 URL의 개수입니다.
        input_url (str): 유사한 URL을 찾고자 하는 기준 URL입니다.
        post_label (str): 기존 저장된 게시글에서 찾을 지, 비교적 신규 게시글에서 찾을 지 결정하는 레이블입니다.

    Returns:
        List[Dict[str, Any]]: 유사한 해시태그를 가진 URL 목록을 JSON 형식으로 반환합니다.
    """
    
    # pickle 파일에서 DataFrame 불러오기
    article_info_file_path = os.path.join(os.path.dirname(__file__), 'article_infos.pkl')
    with open(article_info_file_path, 'rb') as f:
        article_info_df = pickle.load(f)
    
    trained_data_file_path = os.path.join(os.path.dirname(__file__), 'trained_article_latent_matrix.pkl')
    with open(trained_data_file_path, 'rb') as f:
        trained_data_df = pickle.load(f)
    
    # 입력한 URL에 대한 해시태그 집합 추출
    input_hashtags = set(article_info_df.loc[article_info_df['url'] == url, 'hashtags'].iloc[0])

    # 게시글의 학습 여부에 따라 구분하여 추출
    similarity_scores = []
 
    # post_label에 따라 URL 필터링
    if post_label == "trained":
        # trained_data_df의 모든 URL을 가져옴
        trained_urls = trained_data_df['url']
        # article_info_df에서 trained_urls에 포함된 URL만 필터링
        filtered_urls = article_info_df[article_info_df['url'].isin(trained_urls)]['url']
        
    elif post_label == "non_trained":
        # trained_data_df의 모든 URL을 가져옴
        trained_urls = trained_data_df['url']
        # article_info_df에서 trained_urls에 포함되지 않은 URL만 필터링
        filtered_urls = article_info_df[~article_info_df['url'].isin(trained_urls)]['url']
    else:
        return
    
    for url in filtered_urls:
        # URL에 해당하는 해시태그 집합 추출
        hashtags = set(article_info_df.loc[article_info_df['url'] == url, 'hashtags'].iloc[0])
        # 입력 URL과의 Jaccard 유사도 계산
        similarity = jaccard_similarity(input_hashtags, hashtags)
        # 유사도 점수를 저장
        similarity_scores.append((url, similarity))

    # 유사도 점수 내림차순 정렬
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # 동점자 처리를 고려하여 n개 추출
    selected_urls = []
    candidates = []
    for i, (url, similarity) in enumerate(similarity_scores):
        # 현재 유사도 그룹을 가져옴
        if not candidates or candidates[-1][1] == similarity:
            candidates.append((url, similarity))
        else:
            # 이전 그룹 처리
            if len(selected_urls) + len(candidates) <= n:
                selected_urls.extend(candidates)
            else:
                # 남은 자리를 채우기 위해 무작위로 선택
                remaining_spots = n - len(selected_urls)
                selected_urls.extend(sample(candidates, remaining_spots))
                break
            candidates = [(url, similarity)]

    # 마지막 그룹 처리
    if len(selected_urls) < n and candidates:
        remaining_spots = n - len(selected_urls)
        if len(candidates) <= remaining_spots:
            selected_urls.extend(candidates)
        else:
            selected_urls.extend(sample(candidates, remaining_spots))
    
    # 해당 URL의 정보를 찾아 최종 반환
    result = []

    for url, _ in selected_urls:
        row = article_info_df.loc[article_info_df['url'] == url].iloc[0]
        result.append(row.to_dict())

    return result

def jaccard_similarity(set1, set2):
    # 두 집합의 Jaccard 유사도 계산
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0