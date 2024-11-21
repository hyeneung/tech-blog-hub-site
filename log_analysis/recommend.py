from typing import List, Dict, Tuple, Any

from bigquery.user_log_analyze import latent_recommended_urls
from opensearch.article_analyze import hashtags_recommended_urls
from exploratory_recommended_urls import exploratory_recommended_urls

def get_recommend_articles_by_url(url: str) -> List[Dict[str, Any]]:
    """
    사용자가 방문한 기술 블로그 게시글 URL을 받아 추천할 게시글들을 반환하는 함수입니다.

    Parameters:
    url (str): 사용자가 방문한 게시글의 URL입니다.
    
    Returns: 추천할 게시글들 정보
        [
            {
                "title": "Understanding Backend Architecture",
                "pubDate": "2023-11-06",
                "companyName": "someCompany1",
                "url": "https://techinsights.com/backend-architecture",
                "summarizedText": "This article explores the fundamentals of backend architecture...",
                "hashtags": ["Backend", "Architecture", "Tech"]
            },
            {
                "title": "Infrastructure as Code: Best Practices",
                "pubDate": "2023-11-05",
                "companyName": "someCompany2",
                "url": "https://devopsweekly.com/infrastructure-as-code",
                "summarizedText": "Learn how to manage your infrastructure through code...",
                "hashtags": ["Infra", "DevOps", "Automation"]
            }, 
            ...
        ]
    """
    # bigquery 폴더의 사용자 로그 기반 추천 모듈 이용
    # opensearch 폴더의 컨텐츠 기반 추천 모듈 이용
    
    # 추천게시글 시스템 별 할당할 게시글 수 결정
    N = 10 # 기준값
    cf = int(0.36*N)
    stored_cbf = int(0.36*N)
    new_cbf = int(0.18*N)
    expl = N - cf - stored_cbf - new_cbf
    
    # 초기화
    recommended_urls = []

    # 사용자 패턴에 대하여 학습된 잠재요인 기반 유사한 게시글 추천 (Item-Based filtering, CF)
    recommended_urls.append(latent_recommended_urls(cf, url))

    # 해시태그 기반 DB 내 저장된 게시글 추천 (Content-Based filtering, CBF)
    recommended_urls.append(hashtags_recommended_urls(stored_cbf, url, "stored_posts"))

    # 해시태그 기반 DB 외의 추가된 게시글 추천 (Content-Based filtering, CBF)
    recommended_urls.append(hashtags_recommended_urls(new_cbf, url, "new_posts"))

    # 기타 탐색적(보완적) 방법으로 게시글 추천 (사용자 관심사 확장 유도)
    recommended_urls.append(exploratory_recommended_urls(expl, url))

    # list flatten, 필요한 정보만 반환
    recommended_urls = [item for sublist in recommended_urls for item in sublist]
    
    # 중복 URL 제거
    seen_urls = set()  # 중복 체크를 위한 집합 생성
    unique_recommended_urls = []  # 중복이 제거된 결과 리스트

    for item in recommended_urls:
        current_url = item['url']
        if current_url not in seen_urls:
            seen_urls.add(current_url)
            unique_recommended_urls.append(item)

    return unique_recommended_urls