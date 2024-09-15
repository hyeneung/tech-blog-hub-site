# utils/preprocess.py

def get_preprocessed_text(url: str) -> str:
    """
    주어진 URL에서 HTML 파일을 읽어들인 후 텍스트를 전처리하여 반환합니다.
    
    Parameters:
    url (str): HTML 파일을 가져올 URL
    
    Returns:
    str: 전처리된 텍스트
    """
    # 실제 전처리 로직 구현
    preprocessed_text = "요약되지않은글이라긺" * 200 # 대충 2천자라 가정함
    return preprocessed_text