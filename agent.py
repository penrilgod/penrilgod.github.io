import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from langchain_google_genai import ChatGoogleGenerativeAI

# .env 파일로부터 API 키 로드
load_dotenv()

# 1. LangChain을 통해 구글 제미나이 핵심 통신 객체 생성 (v1 안정형)
raw_gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# 2. CrewAI의 데이터 검증기(Pydantic)가 정상 수용할 수 있도록 LLM 전용 래퍼로 감싸줍니다.
gemini_llm = LLM(
    model="gemini/gemini-1.5-pro",  # CrewAI 표준 매칭명
    custom_llm=raw_gemini           # 실제 통신은 위의 안정적인 LangChain 객체가 대행
)

# 3. 트렌드 분석 에이전트
researcher = Agent(
    role='테크 트렌드 분석가',
    goal='IT, AI, 최신 프로그래밍 기술 트렌드를 분석하여 블로그에 쓸 매력적인 주제를 선정한다.',
    backstory='당신은 글로벌 IT 기술 트렌드와 오픈소스 동향을 날카롭게 분석하는 10년 경력의 테크 분석가입니다. 대중적이면서도 영양가 있는 기술 키워드를 찾아내는 데 탁월합니다.',
    llm=gemini_llm,
    verbose=True
)

# 4. 시니어 테크 라이터 (글작가)
writer = Agent(
    role='시니어 소프트웨어 엔지니어 겸 라이터',
    goal='선정된 주제를 바탕으로 실무 관점의 깊이 있는 테크 블로그 글을 마크다운(Markdown) 형식으로 작성한다.',
    backstory='''당신은 20년 경력의 베테랑 데이터 엔지니어이자 시니어 개발자입니다. 
    단순한 개념 나열이 아닌, 반드시 실제 구동 가능한 파이썬(Python) 또는 C# 코드 블록을 포함하여 실무 예시를 깊이 있게 풀어냅니다.
    구글 SEO(검색엔진최적화)에 완벽히 부합하도록 서론, 본론(3가지 핵심 구조), 결론으로 명확히 나누어 작성하며, 독자에게 신뢰감을 주는 전문적인 어조를 사용합니다.''',
    llm=gemini_llm,
    verbose=True
)