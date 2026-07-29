import os
import datetime
import random
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import BaseTool  # 필요시
from litellm import completion  # LiteLLM 직접 사용 시
# CrewAI 의 LLM 설정 방식에 따라 imports 는 달라질 수 있음
from crewai import LLM  # CrewAI 최신 버전에 따라 다름

# 1. .env 파일 로드
load_dotenv()

# ✅ 수정 1: Google API 키를 환경변수에서 그대로 사용 (가짜 키 제거)
# .env 파일에 GOOGLE_API_KEY="your-real-key" 가 있어야 함
if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY 가 .env 파일에 설정되지 않았습니다.")

# ✅ 수정 2: 모델명에서 'latest' 제거 및 표준명 사용
# LiteLLM 에서는 보통 "gemini/gemini-1.5-flash" 형식을 사용
MODEL_NAME = "gemini/gemini-1.5-flash" 

# ✅ 수정 3: CrewAI 에서 LLM 객체를 명시적으로 생성 (안정성 향상)
# (버전에 따라 llm 인자에 문자열 또는 객체가 들어갑니다. 최신 CrewAI 기준)
# 예: from crewai import LLM
# llm = LLM(model=MODEL_NAME, api_key=os.getenv("GOOGLE_API_KEY"))
# 아래 코드는 문자열 전달을 유지하되, 모델명만 수정한 방식입니다.

# 8 가지 카테고리 리스트
CATEGORIES = [
    "[A] 최신 AI 툴/서비스 비교",
    "[B] 백엔드 & 클라우드 기술",
    "[C] 데이터 분석 & SQL",
    "[D] 프론트엔드 & 웹 개발",
    "[E] 개발자 생산성 툴 & Git",
    "[F] 보안 & 서버 관리",
    "[G] 데이터베이스 & ORM",
    "[H] 머신러닝 & 파이썬 기초"
]

# ✅ 수정 4: Python 에서 실제 무작위 선택 (LLM 에게 시키지 않음)
selected_category = random.choice(CATEGORIES)

# 2. 에이전트(Agent) 정의
researcher = Agent(
    role='테크 트렌드 분석가',
    goal='IT, AI, 최신 프로그래밍 기술 트렌드를 분석하여 블로그에 쓸 매력적인 주제를 선정한다.',
    backstory='당신은 글로벌 IT 기술 트렌드와 오픈소스 동향을 날카롭게 분석하는 10년 경력의 테크 분석가입니다.',
    llm=MODEL_NAME,  # 수정된 모델명 전달
    max_rpm=3,
    verbose=True
)

writer = Agent(
    role='시니어 소프트웨어 엔지니어 겸 라이터',
    goal='선정된 주제를 바탕으로 실무 관점의 깊이 있는 테크 블로그 글을 마크다운(Markdown) 형식으로 작성한다.',
    backstory='...',
    llm=MODEL_NAME,
    max_rpm=3,
    verbose=True
)

# 3. 오늘의 날짜와 저장 파일 경로 정의
current_time = datetime.datetime.now()
date_str = current_time.strftime("%Y-%m-%d")
time_str = current_time.strftime("%H%M")

# ✅ 수정 5: 경로를 상대 경로 또는 사용자 홈 디렉토리 기반으로 변경
# 예: ./content/posts 또는 ~/my-ai-blog/
base_dir = os.path.join(os.path.expanduser("~"), "my-ai-blog", "content", "posts")
file_name = f"{date_str}-{time_str}-ai-agent-blog.md"
target_path = os.path.join(base_dir, file_name)

# 4. 태스크(Task) 정의
# ✅ 수정 6: 태스크 설명에 실제 선택된 카테고리 전달
research_task = Task(
    description=f'''
1. 아래 8가지 테크 카테고리 중 **확정된 카테고리**: {selected_category}
2. 이 카테고리에 맞춰, 'CrewAI'나 'Agent'라는 단어를 제외한 완전히 새로운 트렌디한 IT/개발 주제 1개를 기획하라.
3. 기획한 주제는 구체적인 기술 명칭과 활용 사례가 포함되어야 하며, 기존에 작성된 주제와 절대로 중복되지 않아야 한다.
''',
    expected_output='CrewAI가 아닌, 선정된 카테고리에 맞는 신선하고 구체적인 IT/개발 주제 1개',
    agent=researcher
)

# write_task 는 동일하게 유지 (date_str 포맷 확인 필요)
write_task = Task(
    description=f'''
... (기존 내용 유지, 단 date 변수 사용)
'''.format(date=date_str),
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
try:
    result = blog_crew.kickoff()
    
    # 6. 마크다운 파일로 결과 자동 저장
    blog_content = str(result)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(blog_content)

    print(f"✨ 성공적으로 글이 작성되어 저장되었습니다! 경로: {target_path}")
except Exception as e:
    print(f"❌ 자동 블로그 생성 중 오류가 발생했습니다: {e}")
    # 에러 로그를 별도 파일로 저장하는 코드 추가 권장