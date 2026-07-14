@echo off
echo 🚀 1. AI 에이전트 가동 및 새로운 블로그 글 자동 생성...
python generate.py

echo 📦 2. Hugo 정적 웹사이트 빌드 중...
hugo --cleanDestinationDir

echo 📂 3. public 폴더 내 정적 파일들을 최상위로 이동 및 정렬...
xcopy /E /Y public\* .

echo 🌐 4. 깃허브 저장소로 진짜 웹사이트 파일 전송 (Push)...
git add .
git commit -m "Fix: Deploy static HTML files to root: %date% %time%"
git push origin main

echo ✨ 배포가 완벽하게 완료되었습니다!
pause