import os
import pickle
from random import sample
from typing import List, Dict, Tuple, Any

def exploratory_recommended_urls(expl, url):
    # pickle 파일에서 DataFrame 불러오기
    article_info_file_path = os.path.join(os.path.dirname(__file__), 'article_infos.pkl')
    with open(article_info_file_path, 'rb') as f:
        article_info_df = pickle.load(f)
    
    # 입력한 URL에 대한 해시태그 집합 추출
    input_hashtags = set(article_info_df.loc[article_info_df['url'] == url, 'hashtags'].iloc[0])

    # 게시글의 학습 여부에 따라 구분하여 추출
    similarity_scores = []

    urls = article_info_df['url']

    for url in urls:
        # URL에 해당하는 해시태그 집합 추출
        hashtags = set(article_info_df.loc[article_info_df['url'] == url, 'hashtags'].iloc[0])
        # 입력 URL과의 Jaccard 유사도 계산
        similarity = jaccard_similarity(input_hashtags, hashtags)
        # 유사도 점수를 저장
        similarity_scores.append((url, similarity))
    
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # article이 충분히 많다고 가정하고, expl의 K배수 범위에서 무작위로 뽑음
    sim_selected_url = sample(similarity_scores[2*expl:4*expl],int(expl // 2) + 1)

    random_url = sample(similarity_scores[4*expl:8*expl], expl-len(sim_selected_url))

    candidates_urls = sim_selected_url + random_url

    result = []

    for url, _ in candidates_urls:
        row = article_info_df.loc[article_info_df['url'] == url].iloc[0]
        result.append(row.to_dict())

    return result

def jaccard_similarity(set1, set2):
    # 두 집합의 Jaccard 유사도 계산
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0