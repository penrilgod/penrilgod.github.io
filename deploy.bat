@echo off
echo 🚀 1. AI 에이전트 가동 및 새로운 블로그 글 자동 생성...

chcp 65001

py -3.12 generate.py

REM ✅ 수정: python 실행 실패 시 에러코드 확인 후 종료
if %errorlevel% neq 0 (
    echo ❌ 블로그 글 생성 실패! 빌드를 중단합니다.
    pause
    exit /b 1
)

echo 📦 2. Hugo 정적 웹사이트 빌드 중 (임시저장 및 미래 시간 강제 빌드 옵션 적용)...
:: -D 옵션: draft: true인 파일도 강제로 포함
:: -F 옵션: 미래 날짜(Future date)로 되어 있는 파일도 강제로 포함
hugo --cleanDestinationDir -D -F

if %errorlevel% neq 0 (
    echo ❌ Hugo 빌드 실패!
    pause
    exit /b 1
)


echo 📂 3. public 폴더 내 정적 파일들을 최상위로 이동 및 정렬...
xcopy /E /Y public\* .

echo 🌐 4. 깃허브 저장소로 진짜 웹사이트 파일 전송 (Push)...
git add .
git commit -m "Fix: Rebuild all draft and future posts: %date% %time%"
git push origin main

echo ✨ 배포가 완벽하게 완료되었습니다!
pause