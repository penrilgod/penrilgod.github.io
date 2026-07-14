import os
import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# 1. .env 파일 로드
load_dotenv()

# OpenAI 에러 우회용 더미 키
os.environ["OPENAI_API_KEY"] = "fake-key-to-bypass-crewai-validation"

# 무료 한도가 적용되는 기본 모델명 지정
MODEL_NAME = "gemini/gemini-3.5-flash"

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
file_name = f"{date_str}-ai-agent-blog.md"
target_path = os.path.join("content", "posts", file_name)

# 4. 태스크(Task) 정의
research_task = Task(
    description='현재 개발자들에게 가장 유용하고 트렌디한 "Python을 활용한 업무 자동화 및 AI 연동 기술" 중 하나를 선정하여 핵심 개념과 선정 이유를 정리하라.',
    expected_output='블로그 글의 주제가 될 핵심 키워드와 기술적 유용성이 정리된 분석 리포트',
    agent=researcher
)

write_task = Task(
    description='''테크 분석가가 선정한 주제를 바탕으로 완벽한 Hugo 마크다운(.md) 포맷의 블로그 글을 작성하라.
    반드시 다음 조건을 충족해야 한다:
    1. 글의 서두에는 아래 양식의 Hugo Front Matter(메타데이터)가 들어가야 한다. (draft는 반드시 false여야 함)
       ---
       title: "여기에 AI가 정한 매력적인 제목 입력"
       date: {date}
       draft: false
       ---
    2. 본문에는 반드시 구동 가능한 실제 Python 코드 예시(코드 블록)가 포함되어야 한다.
    3. 구글 검색(SEO)에 유리하도록 소제목(##, ###)을 명확히 나누어 가독성 있게 작성하라.
    4. 어조는 전문적이고 신뢰감 있는 시니어 엔지니어의 톤앤매너를 유지하라.'''.format(date=date_str),
    expected_output='Hugo Front Matter를 포함하여 작성된 고품질의 기술 마크다운 텍스트',
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