# API 설정 가이드

## 1. 네이버 뉴스 API 설정

### 1.1 네이버 개발자센터 회원가입 및 애플리케이션 등록

1. [네이버 개발자센터](https://developers.naver.com/) 접속
2. 네이버 계정으로 로그인
3. 우측 상단 "Application" > "애플리케이션 등록" 클릭
4. 애플리케이션 정보 입력:
   - **애플리케이션 이름**: 뉴스요약봇 (원하는 이름 입력)
   - **사용 API**: `검색` 체크
   - **비로그인 오픈 API 서비스 환경**: `WEB 설정` 선택
   - **웹 서비스 URL**: `http://localhost:5000` (로컬 테스트용)
5. "등록하기" 클릭
6. Client ID와 Client Secret 확인 및 안전한 곳에 저장

### 1.2 사용량 제한
- 하루 호출 한도: 25,000회 (무료)
- 한 번에 검색 가능한 뉴스 개수: 최대 100개
- 시작 위치: 최대 1000개

## 2. OpenAI API 설정

### 2.1 계정 생성 및 API 키 발급

1. [OpenAI Platform](https://platform.openai.com/) 접속
2. 계정 생성 또는 로그인
3. 휴대폰 번호 인증 (필수)
4. "API keys" 페이지로 이동
5. "Create new secret key" 클릭
6. API 키 이름 입력 후 생성
7. 생성된 API 키를 안전한 곳에 저장 (한 번만 표시됨)

### 2.2 요금 정보 (2024년 기준)
- GPT-4o-mini 모델: 입력 $0.15/1M 토큰, 출력 $0.60/1M 토큰
- 신규 가입 시 $5 무료 크레딧 제공 (3개월간 유효)
- 결제 정보 등록 후 사용량에 따라 과금

## 3. Anthropic API 설정

### 3.1 계정 생성 및 API 키 발급

1. [Anthropic Console](https://console.anthropic.com/) 접속
2. 계정 생성 또는 로그인
3. "API Keys" 섹션으로 이동
4. "Create Key" 클릭
5. API 키 이름 입력 후 생성
6. 생성된 API 키를 안전한 곳에 저장

### 3.2 요금 정보 (2024년 기준)
- Claude 3 Haiku: 입력 $0.25/1M 토큰, 출력 $1.25/1M 토큰
- 신규 가입 시 $5 무료 크레딧 제공

## 4. 환경 설정

### 4.1 Python 환경 설정

```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 필요한 패키지 설치
pip install flask streamlit openai anthropic requests
```

### 4.2 환경변수 설정

#### Windows (PowerShell)
```powershell
$env:NAVER_CLIENT_ID="your_client_id"
$env:NAVER_CLIENT_SECRET="your_client_secret"
$env:OPENAI_API_KEY="your_openai_key"
$env:ANTHROPIC_API_KEY="your_anthropic_key"
```

#### macOS/Linux (Bash)
```bash
export NAVER_CLIENT_ID="your_client_id"
export NAVER_CLIENT_SECRET="your_client_secret"
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
```

#### .env 파일 사용 (권장)
```bash
# .env 파일 생성
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### 4.3 .env 파일을 위한 추가 패키지 설치
```bash
pip install python-dotenv
```

### 4.4 코드에서 .env 파일 로드
```python
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경변수 읽기
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
```

## 5. 실행 방법

### 5.1 Flask 애플리케이션 실행

```bash
# Flask 앱 실행
python app.py

# 또는 Flask 명령어 사용
export FLASK_APP=app.py  # Linux/macOS
set FLASK_APP=app.py     # Windows
flask run
```

웹 브라우저에서 `http://localhost:5000` 접속

### 5.2 Streamlit 애플리케이션 실행

```bash
# Streamlit 앱 실행
streamlit run streamlit_app.py
```

자동으로 웹 브라우저가 열리며 `http://localhost:8501` 주소로 접속됨

## 6. 보안 및 모범 사례

### 6.1 API 키 보안
- API 키를 코드에 직접 작성하지 마세요
- 환경변수나 .env 파일을 사용하세요
- .env 파일을 .gitignore에 추가하여 버전 관리에서 제외하세요
- API 키 사용량을 정기적으로 모니터링하세요

### 6.2 사용량 관리
- 네이버 API: 일일 한도 25,000회 초과 시 429 에러 발생
- OpenAI/Anthropic: 과도한 사용 시 요금 폭탄 위험
- 적절한 에러 처리 및 재시도 로직 구현

### 6.3 .gitignore 예시
```gitignore
# 환경변수 파일
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Python 가상환경
venv/
env/
ENV/

# 캐시 파일
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE 설정 파일
.vscode/
.idea/
```

## 7. 문제 해결

### 7.1 네이버 API 관련 오류
- **401 Unauthorized**: Client ID/Secret 확인
- **429 Too Many Requests**: 일일 한도 초과, 다음날 재시도
- **400 Bad Request**: 검색어 인코딩 확인

### 7.2 OpenAI API 관련 오류
- **401 Unauthorized**: API 키 확인
- **429 Rate Limit**: 요청 빈도 조절
- **400 Bad Request**: 요청 형식 확인

### 7.3 Anthropic API 관련 오류
- **401 Unauthorized**: API 키 확인
- **429 Rate Limit**: 요청 빈도 조절
- **400 Bad Request**: 메시지 형식 확인

### 7.4 일반적인 문제
- **모듈 import 오류**: 패키지 재설치 확인
- **포트 충돌**: 다른 포트 번호 사용
- **방화벽 차단**: 로컬 서버 접근 허용 설정

이 가이드를 따라하면 네이버 뉴스 API와 AI 모델을 활용한 뉴스 요약 에이전트를 성공적으로 구축할 수 있습니다.