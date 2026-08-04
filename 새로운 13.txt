import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"🔑 로드된 API Key (앞 6자리): {api_key[:6] if api_key else '키 없음'}***")

# 사용 가능한 모델 목록 조회
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    with urllib.request.urlopen(url) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("\n✅ API Key 인증 성공! 사용 가능한 모델 목록:")
        for m in res.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                print(f" - {m['name']}")
except urllib.error.HTTPError as e:
    print(f"\n❌ API 호출 실패 ({e.code}): {e.read().decode('utf-8')}")
except Exception as e:
    print(f"\n❌ 기타 오류 발생: {e}")