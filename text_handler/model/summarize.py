from openai import OpenAI


class SummarizeModule:
    def summarize(self, text: str) -> str:
        """
        주어진 text를 요약한 결과를 반환합니다.
        """
        prompt = f"""\
당신은 블로그 글 요약기입니다.
예시와 같이 글에 대한 한 줄 요약과 목차를 한국어로 제시하면 됩니다.
목차는 한 줄씩만 출력하며 세부적인 내용은 제외해야 합니다.
원문을 그대로 제시하면 안 됩니다.

{{example-start}}
요약: NLB의 TCP idle timeout 설정 기능을 소개하는 글입니다.
목차:
    1. TCP 연결 설정의 이해
    2. NLB의 TCP 연결 처리
    3. TCP 유휴 제한 시간을 변경할 때 고려사항
    4. AWS APIs/CLI 를 사용하여 TCP 유휴 제한 시간을 설정하는 단계
    5. AWS 관리 콘솔을 사용하여 TCP 유휴 제한 시간을 설정하는 단계
    6. 모니터링
{{example-end}}

Article:
{text}

Summarized text:
"""

        api_key = ''
        model = OpenAI(api_key=api_key)

        response = model.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        ).choices[0].message.content

        # post-processing
        lines = response.split('\n')
        if '' in lines:
            lines.remove('')
        one_line = lines.pop(0)[4:].strip()
        if len(lines) >= 1:
            lines.pop(0)
        index = []
        for line in lines:
            try:
                index.append(line.strip().split('.')[1].strip())
            except:
                continue
        
        summarized_text = one_line + '\n\n목차:\n' + '\n'.join([f'{i + 1}. {item}' for i, item in enumerate(index)])

        return summarized_text