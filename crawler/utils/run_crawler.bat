@echo off
REM ============================================
REM 커뮤니티 크롤러 - 15분 간격 로테이션 스케줄러
REM ============================================
REM 
REM 사용법:
REM 1. 이 파일을 crawler 폴더에 저장
REM 2. Windows 작업 스케줄러에서 8개 작업 생성
REM 3. 각 작업마다 다른 사이트와 시작 시간 설정
REM
REM ============================================

REM Python 경로 설정 (필요시 수정)
set PYTHON=python

REM 크롤러 디렉토리
cd /d "%~dp0"

REM 사이트 이름 (인자로 받음)
set SITE=%1

REM 로그 파일
set LOGDIR=logs
if not exist %LOGDIR% mkdir %LOGDIR%
set LOGFILE=%LOGDIR%\crawler_%SITE%_%date:~0,4%%date:~5,2%%date:~8,2%.log

REM 크롤링 실행
echo [%date% %time%] Starting crawler for %SITE% >> %LOGFILE%
%PYTHON% main.py --site %SITE% >> %LOGFILE% 2>&1
echo [%date% %time%] Finished crawler for %SITE% >> %LOGFILE%
echo. >> %LOGFILE%
