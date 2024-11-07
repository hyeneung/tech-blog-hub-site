# FewShotExample에 사용될 예시 모음.
# 특성 상 hashtags.py의 make_prompt 계열 함수 내의 example = ...에 하단 리스트를 그대로 대입하여도 문제없음
# 분리한 이유는 FewShot이 함수 내에서 지나치게 길어지면 가독성 문제가 생겨서 분리한 것일뿐.


# make_prompt_for_intro_blocks에 사용되는 examples (List[Dict]):
# [ { Title, Intro Content(서문), 최초 Subtitle, 최초 Subtile의 Content, 예시 keywords }, ... ]
intro_examples = [
{
"title": """이미지 분류 모델 개발, 아직도 데이터만 기다려?""",
"intro_content": """이번 글에서는 Zero-shot 분류를 사용하여 가공한 선분류 데이터셋을 통해 모델 개발 기간을 단축한 방법을 중점으로 소개하겠습니다""",
"subtitle": """이미지 분류 모델 선정""",
"subtitle_content": """많은 모델들 중에서도 CVPR 2022에서 공개된 ConvNext[1]라는 순수 컨볼루션 신경망(Convnet) 모델을 선정했습니다.""",
"keywords": "Image Classification, Zero-shot, ConvNext"
},
{
"title": """Web을 위한 gRPC Stub과 Runtime 생성하기 - Feat. Buf & kubernetes""",
"intro_content": """gRPC는 마이크로서비스간 호출에 많이 사용되는 통신 프로토콜로,
개발자 생산성 향상 및 빠른 통신 속도를 지원하여 많은 어플리케이션에서 사용하고 있습니다.""",
"subtitle": """점점 늘어나는 유지비용""",
"subtitle_content": """하지만 점점 프론트엔드 어플리케이션이 많아지고 마이크로 서비스와 각 서비스의 메시지가 늘어나면서 아래와 같은 문제점들이 생겼습니다.""",
"keywords": "gRPC, kubernetes, microservice"
},
]


# make_prompt_for_unit_block에 사용되는 examples (List[Dict]):
# [ { Subtitle, Content, 예시 keywords }, ... ]
body_examples = [
{
"subtitle": """Next.js 어플리케이션에서 사용 및 효과""",
"content": """별도의 API 코드 작성 없이 편리하게 마이크로서비스를 호출할 수 있었습니다. 또한 SSR에서 방화벽을 거치지 않게 되어 인프라 부하가 감소되었습니다.""",
"keywords": "Next.js, Microservice, SSR"
},
{
"subtitle": """ChatGPT와 협업하며 겪은 시행착오""",
"content": """프롬프트로는 완벽한 맥락 전달이 어렵고 AI의 할루시네이션 현상이 발생하여 스크립트 작성 작업시간이 늘어났습니다.""",
"keywords": "ChatGPT, prompt, hallucination"
},
]


# make_prompt_for_category에 사용되는 examples (List[Dict]):
# [ { 추출된 keywords, active상태 category 후보군, 최종 category 예시}, ... ]
candidates_examples = [
{
"candidates": """image classification, data augmentation, model performance, preprocessing, vision system, deep learning""",
"keywords": "Computer Vision, Model Optimization, Deep Learning"
},
{
"candidates": """code test, algorithm, problem solving, data structure, dynamic programming, greedy algorithm, graph theory""",
"keywords": "algorithm, code test"
}
]


# make_prompt_for_category에 사용되는 examples (List[Dict]):
# [ { 추출된 keywords, active상태 category 후보군, 최종 category 예시}, ... ]
category_examples = [
{
"keywords": """Data Analysis, Statistics, Big Data, Anomaly Detection, Supervised Learning""",
"active_category":"""Frontend, DataScience, Security, AI""",
"final_category": "DataScience, AI"
},
{
"keywords": """System Design, Agile Development, Code Review, Version Control""",
"active_category":"""Mobile, SoftwareEngineering, Infra""",
"final_category": "SoftwareEngineering"
}
]


# make_prompt_for_postproces에 사용되는 examples (List[Dict]):
# [ { 추출된 keywords, 중복이 제거된 예시 hashtags }, ... ]
postprocess_examples = [
{
"keywords": """DL, Deep Learning, AI, Artificial Intelligence, ML, Machine Learning""",
"hashtags": "Deep Learning, AI, Machine Learning"
},
{
"keywords": """Threads, Thread, Function, Functions, Multi-Task, Multitasking""",
"hashtags": "Thread, Function, Multi-Task"
}
]