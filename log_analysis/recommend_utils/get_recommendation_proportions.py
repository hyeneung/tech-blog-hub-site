import os
import pickle

from typing import List, Dict, Tuple, Any

def get_recommendation_proportions(N: int, url: str) -> Tuple[int, int, int, int]:    
    trained_data_file_path = os.path.join(os.path.dirname(__file__), 'trained_article_latent_matrix.pkl')
    with open(trained_data_file_path, 'rb') as f:
        trained_data_df = pickle.load(f)
    
    # 만약 trained_data_df['url']에 url이 있다면 flag를 1로, 그렇지 않으면 0으로 설정
    flag = 1 if url in trained_data_df['url'].values else 0

    if flag == 1: # CF 적용가능, CBF 구분하여 적용가능
        cf = int(0.35*N)
        trained_cbf = int(0.35*N)
        non_trained_cbf = int(0.2*N)
        expl = int(0.1*N)
    else: # 단순한 CF만 적용가능
        cf = 0
        trained_cbf = N
        non_trained_cbf = 0
        expl = 0
    
    return cf, trained_cbf, non_trained_cbf, expl