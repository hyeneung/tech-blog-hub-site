import re
from typing import List, Tuple

# 주로 전처리된 텍스트를 2차 가공하는 함수와 관련된 utility 클래스, HashtaggingModule을 보조
class TextProcessingUtils:
    def __init__(self):
        pass

    def make_blocks_from_preprocessed_text(self, text: str) -> List[List[Tuple[str, str]]]:
        """
        주어진 텍스트를 제목, 서문, 소제목 및 내용을 기준으로 파싱하여 블록(List[Tuple[str, str]) 단위로 반환합니다.
        반복되는 소제목은 하나의 블록으로 묶고, 고립된 소제목은 무시합니다.
            
        Parameters:
            text (str): get_preprocessed_text에 의해 전처리된 텍스트.
            
        Returns:
            blocks (list): 파싱된 블록 리스트. 각 블록은 [('Type', '내용')] 형식의 튜플을 요소로 가지며, 예시는 다음과 같습니다:
                [
                    [('Title', 'Sample Article Title'), ('Intro', 'This is the introductory text.')],
                    [('Subtitle', 'First Subtitle'), ('Content', 'This is the first content.')],
                    [('Subtitle', 'Second Subtitle / Third Subtitle'), ('Content', 'Combined content of second and third.')],
                    ...
                ]
        """
        blocks = []

        # Title 추출
        title_match = re.search(r'Title:\s*(.*)', text)
        if title_match:
            title_content = title_match.group(1).strip()
            blocks.append([("Title", title_content)])
        else:
            blocks.append([("Title", "")])

        # 서문 추출
        intro_match = re.search(r'Intro:\s*(.*)', text)
        intro_content = intro_match.group(1).strip() if intro_match else ''
        blocks[-1].append(("Intro", intro_content))  # Title 블록에 Intro 추가

        # Subtitle과 Content 블록 생성
        subtitles_contents = re.split(r'Subtitle:\s*', text)[1:]  # 첫 번째 Subtitle 이후로 분리
        temp_block = []  # 임시 블록을 저장하기 위한 변수
        pending_subtitles = []  # 반복되는 subtitle을 임시 저장하는 리스트

        for segment in subtitles_contents:
            # Subtitle 추출
            subtitle, *content = segment.split('\n', 1)
            subtitle = subtitle.strip()
            
            # Content가 있는 경우
            if content and content[0].strip():
                # 대기 중인 subtitle들을 하나의 블록으로 묶어 추가
                if len(pending_subtitles) > 1:
                    blocks.append(pending_subtitles)  # 여러 subtitle을 하나의 블록으로 추가
                    pending_subtitles = []  # 초기화
                elif len(pending_subtitles) == 1:  # 고립된 subtitle은 무시
                    pending_subtitles = []

                # Subtitle + Content 블록 생성
                temp_block = [("Subtitle", subtitle), ("Content", content[0].strip())]
                blocks.append(temp_block)  # 완전한 블록을 blocks 리스트에 추가
                temp_block = []  # temp_block 초기화
            else:
                # Content가 없는 경우 pending_subtitles에 추가
                pending_subtitles.append(("Subtitle", subtitle))

        # 마지막에 남은 pending_subtitles가 둘 이상인 경우 추가
        if len(pending_subtitles) > 1:
            blocks.append(pending_subtitles)

        return blocks
    
    def make_merged_block_list(self, org_list: List[List[Tuple[str, str]]]) -> List[List[Tuple[str, str]]]:
        """
        주어진 org_list에서 Content 길이가 threshold보다 작으면 이웃 블록과 합병하여 반환하는 함수입니다.
        모든 블록의 Content 길이를 체크하고, 이웃 블록의 Content와 합쳐 threshold 이상이 되도록 합병합니다.
        (단, org_list에 Intro 블럭은 제외되어야 합니다.)

        Parameters:
        org_list (List[List[Tuple[str, str]]]): 초기 블록 리스트

        Returns:
        contents_blocks (List[List[Tuple[str, str]]]): 합병이 완료된 블록 리스트
        """
        content_blocks = org_list  # 모든 블록을 content_blocks로 처리
        MERGE_THRESHOLD = 100 # block내 Content의 글자 수가 MERGE_THESHOLD 이하일 경우 다른 문단과 합병 시도

        while True:
            merged = False  # 루프 내에서 합병이 이루어졌는지 확인하는 플래그
            new_blocks = []

            # 블록을 2개씩 짝지어 합병을 진행
            i = 0
            while i < len(content_blocks) - 1:
                current_block = content_blocks[i]
                next_block = content_blocks[i + 1]

                # 현재 블록과 다음 블록의 Content 길이 체크
                current_content = current_block[1][1]
                next_content = next_block[1][1]

                # 빈 content는 제외하고 합산된 길이만을 사용해 합병 조건을 확인
                combined_content_length = len(current_content) + len(next_content)
                if combined_content_length < MERGE_THRESHOLD:
                    # Subtitle과 Content 합병
                    merged_subtitle = current_block[0][1] + " , " + next_block[0][1]
                    
                    # 빈 문자열이 아닌 Content만 합치기
                    merged_content = "\n".join([c for c in [current_content, next_content] if c])

                    new_blocks.append([("Subtitle", merged_subtitle), ("Content", merged_content)])
                    merged = True
                    i += 2  # 두 블록을 하나로 합병했으므로 다음 블록은 건너뜀
                else:
                    new_blocks.append(current_block)
                    i += 1

            # 홀수일 경우 마지막 블록 추가
            if i < len(content_blocks):
                new_blocks.append(content_blocks[i])

            if not merged:  # 합병이 일어나지 않았을 때 루프 종료
                break

            content_blocks = new_blocks  # 새롭게 합병된 블록 리스트를 content_blocks에 할당

        # 최종 결과 반환
        return content_blocks

    def to_camel_case(self, word_list: List[str]) -> List[str]:
        """
        리스트 내 문자열에 대해 두 단어 이상인 경우 CamelCase로 변환하는 함수입니다.
        (단순히 각 단어의 첫 글자만 대문자로 치환한 뒤 한 단어로 합칩니다.)
        
        Parameters:
        word_list (List[str]): 변환할 문자열이 포함된 리스트
        
        Returns:
        result (List[str]): CamelCase로 변환된 문자열 리스트
        """
        result = []
        for word in word_list:
            words = word.split()
            # 두 단어 이상일 경우 각 단어의 첫 글자만 대문자로 치환하여 연결
            if len(words) > 1:
                camel_case_word = ''.join(w[0].upper() + w[1:] for w in words)
                result.append(camel_case_word)
            else:
                word_ = word[0].upper() + word[1:]
                result.append(word_)  # 한 단어는 첫글자를 대문자로 바꿔서 추가

        return result