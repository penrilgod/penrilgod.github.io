import os
import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# 1. .env 파일 로드
load_dotenv()

# OpenAI 에러 우회용 더미 키
os.environ["OPENAI_API_KEY"] = "fake-key-to-bypass-crewai-validation"

# 무료 한도가 적용되는 기본 모델명 지정
MODEL_NAME = "gemini/gemini-1.5-flash-latest"

# 2. 에이전트(Agent) 정의 (max_rpm을 3으로 제한하여 429 차단 우회)
researcher = Agent(
    role='테크 트렌드 분석가',
    goal='IT, AI, 최신 프로그래밍 기술 트렌드를 분석하여 블로그에 쓸 매력적인 주제를 선정한다.',
    backstory='당신은 글로벌 IT 기술 트렌드와 오픈소스 동향을 날카롭게 분석하는 10년 경력의 테크 분석가입니다. 대중적이면서도 영양가 있는 기술 키워드를 찾아내는 데 탁월합니다.',
    llm=MODEL_NAME,
    max_rpm=3,  # ◀ 초당 호출 제한을 피하기 위해 분당 3회만 호출하도록 제한
    verbose=True
)

writer = Agent(
    role='시니어 소프트웨어 엔지니어 겸 라이터',
    goal='선정된 주제를 바탕으로 실무 관점의 깊이 있는 테크 블로그 글을 마크다운(Markdown) 형식으로 작성한다.',
    backstory='''당신은 20년 경력의 베테랑 데이터 엔지니어이자 시니어 개발자입니다. 
    단순한 개념 나열이 아닌, 반드시 실제 구동 가능한 파이썬(Python) 또는 C# 코드 블록을 포함하여 실무 예시를 깊이 있게 풀어냅니다.
    구글 SEO(검색엔진최적화)에 완벽히 부합하도록 서론, 본론(3가지 핵심 구조), 결론으로 명확히 나누어 작성하며, 독자에게 신뢰감을 주는 전문적인 어조를 사용합니다.''',
    llm=MODEL_NAME,
    max_rpm=3,  # ◀ 초당 호출 제한을 피하기 위해 분당 3회만 호출하도록 제한
    verbose=True
)

# 3. 오늘의 날짜와 저장 파일 경로 정의
current_time = datetime.datetime.now()
date_str = current_time.strftime("%Y-%m-%d")
time_str = current_time.strftime("%H%M")
file_name = f"{date_str}-{time_str}-ai-agent-blog.md"
target_path = f"C:\\Users\\ersgo\\my-ai-blog\\content\\posts\\{file_name}"

# 4. 태스크(Task) 정의
research_task = Task(
    description='''
1. 아래 8가지 테크 카테고리 중 하나를 **무작위(Random)**로 선택하라:
   - [A] 최신 AI 툴/서비스 비교 (예: Claude 3.5, Cursor, Perplexity, Midjourney 등)
   - [B] 백엔드 & 클라우드 기술 (예: Docker, FastApi, AWS, Kubernetes, Serverless 등)
   - [C] 데이터 분석 & SQL (예: Pandas, BigQuery, 데이터 시각화 팁 등)
   - [D] 프론트엔드 & 웹 개발 (예: Next.js, React, Tailwind CSS 성능 최적화 등)
   - [E] 개발자 생산성 툴 & Git (예: VSCode 확장프로그램, Git CLI 팁, 업무 자동화 등)
   - [F] 보안 & 서버 관리 (예: API Key 보안, Linux 필수 명령어, SSH 등)
   - [G] 데이터베이스 & ORM (예: PostgreSQL 성능 튜닝, Redis 캐싱 등)
   - [H] 머신러닝 & 파이썬 기초 (예: Scikit-learn, 파이썬 문법 꿀팁 등)

2. 위에서 선택한 카테고리에 맞춰, **'CrewAI'나 'Agent'라는 단어를 제외한** 완전히 새로운 트렌디한 IT/개발 주제 1개를 기획하라.
3. 기획한 주제는 구체적인 기술 명칭과 활용 사례가 포함되어야 하며, 기존에 작성된 주제와 절대로 중복되지 않아야 한다.
''',
    expected_output='CrewAI가 아닌, 8가지 테크 카테고리 중 무작위로 선정된 신선하고 구체적인 IT/개발 주제 1개',
    agent=researcher
)

write_task = Task(
description='''테크 분석가가 선정한 주제를 바탕으로 완벽한 Hugo 마크다운(.md) 포맷의 블로그 글을 작성하라.

반드시 다음 조건을 엄격히 충족해야 한다:

1. [Front Matter] 글의 서두에는 아래 양식의 Hugo 메타데이터를 반드시 포함할 것. (draft는 반드시 false)
---
title: "여기에 AI가 정한 매력적인 제목 입력"
date: {date}
draft: false
---

2. [콘텐츠 유형 다변화] 매번 똑같은 패턴을 피하기 위해, 주제에 맞춰 아래 4가지 유형 중 가장 적합한 방식을 선택하여 작성할 것:
   - [실전 가이드] 초보자/실무자를 위한 단계별 Step-by-Step 튜토리얼
   - [비교 분석] 2~3가지 핵심 기술/도구의 장단점 및 특징 비교
   - [개념 정리] 복잡한 IT/AI 기술 개념을 쉬운 비유와 함께 구조화한 설명
   - [트렌드/뉴스] 최신 기술 동향 분석 및 실제 적용 전망

3. [구성 및 가독성]
   - Front Matter 바로 밑 본문 시작 지점에 반드시 '📌 오늘 글의 3줄 요약' 코너를 배치할 것.
   - 구글 검색(SEO) 및 애드센스 평가에 유리하도록 소제목(##, ###)과 불렛 포인트(*)를 명확히 활용할 것.
   - 단순 이론 나열에 그치지 않고, 글 후반부에 '💡 실무 적용 팁' 단락을 반드시 포함할 것.

4. [실전 코드 및 톤앤매너]
   - 본문에는 반드시 구동 가능한 실제 파이썬(Python) 코드 예시(코드 블록 ```python ... ```)를 1개 이상 포함할 것.
   - 어조는 전문적이고 신뢰감 있는 10년 차 시니어 엔지니어의 톤앤매너를 유지할 것.'''.format(date=date_str),
    expected_output='Hugo Front Matter, 3줄 요약, 다채로운 목차, 실전 파이썬 코드가 포함된 완벽한 기술 마크다운 텍스트',
    agent=writer
)

# 5. 크루(Crew) 결성 및 실행
blog_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

print("🚀 제미나이 에이전트 가동을 시작합니다. 글을 생성 중입니다...")
result = blog_crew.kickoff()

# 6. 마크다운 파일로 결과 자동 저장
blog_content = str(result)
os.makedirs(os.path.dirname(target_path), exist_ok=True)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(blog_content)

print(f"✨ 성공적으로 글이 작성되어 저장되었습니다! 경로: {target_path}")