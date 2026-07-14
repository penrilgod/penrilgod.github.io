@echo off
echo 🚀 1. AI 에이전트 가동 및 새로운 블로그 글 자동 생성...
python generate.py

echo 📦 2. Hugo 정적 웹사이트 빌드 중...
hugo --cleanDestinationDir

echo 🌐 3. 깃허브 저장소로 최신 글 자동 푸시(Push)...
git add .
git commit -m "Auto-deployed by AI Agent: %date% %time%"
git push origin main

echo ✨ 배포가 완벽하게 완료되었습니다!
pause