from typing import List, Dict, Any
from opensearch.article_analyze import get_related_urls_json

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
    recommended_urls_by_hashtags = get_related_urls_json(url)

    return recommended_urls_by_hashtags