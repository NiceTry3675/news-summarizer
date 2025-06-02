# AI 뉴스 요약 에이전트

네이버 뉴스 API와 OpenAI/Anthropic AI 모델을 활용한 스마트 뉴스 요약 서비스입니다.

## 🚀 주요 기능

- **네이버 뉴스 검색**: 키워드를 통한 실시간 뉴스 검색
- **AI 요약**: OpenAI GPT 또는 Anthropic Claude를 사용한 뉴스 요약
- **직관적인 UI**: Streamlit 기반의 사용자 친화적 인터페이스
- **다양한 옵션**: 검색 개수, 정렬 기준 등 세부 설정 가능

## 📋 필요 요구사항

- Python 3.8 이상
- 네이버 개발자센터 API 키
- OpenAI 또는 Anthropic API 키

## 🛠️ 설치 방법

1. **프로젝트 클론**
   ```bash
   cd your-project-directory
   ```

2. **가상환경 생성 (권장)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 API 키 설정

### 1. 네이버 뉴스 API

1. [네이버 개발자센터](https://developers.naver.com/)에 접속
2. 로그인 후 '애플리케이션 등록' 클릭
3. 다음 정보로 애플리케이션 등록:
   - 애플리케이션 이름: AI 뉴스 요약 에이전트
   - 사용 API: 검색 <-이때 자신이 원하는 사이트를 한정지어 주세요. 예)뉴스를 원한다면 https://news.naver.com/
4. 등록 완료 후 Client ID와 Client Secret 복사
5. 귀찮으시면 이거 쓰세요 Client ID = HR1ViOWJh1QauFSYrqqH
Client Secret = 83RXfyuce_

### 2. AI 모델 API (택 1)

#### OpenAI API
1. [OpenAI 플랫폼](https://platform.openai.com/)에 가입
2. API Keys 메뉴에서 새 API 키 생성
3. 생성된 API 키 복사

#### Anthropic API
1. [Anthropic 콘솔](https://console.anthropic.com/)에 가입
2. API Keys 메뉴에서 새 API 키 생성
3. 생성된 API 키 복사

## 🚀 실행 방법

1. **애플리케이션 실행**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **웹 브라우저에서 접속**
   - 자동으로 브라우저가 열리며 앱에 접속됩니다
   - 수동 접속: http://localhost:8501

3. **API 키 설정**
   - 사이드바에서 네이버 API Client ID/Secret 입력
   - AI 모델 선택 (OpenAI 또는 Anthropic)
   - 선택한 AI 모델의 API 키 입력

4. **뉴스 검색 및 요약**
   - 메인 화면에서 검색 키워드 입력
   - 요약할 뉴스 개수와 정렬 기준 선택
   - '뉴스 검색 및 요약' 버튼 클릭

## 📱 사용 화면

### 메인 화면
- 검색어 입력 필드
- 뉴스 개수 슬라이더 (1~10개)
- 정렬 기준 선택 (정확도순/최신순)
- 검색 및 요약 버튼

### 사이드바
- 네이버 API 설정
- AI 모델 선택 및 API 키 입력
- API 키 발급 가이드 링크

### 결과 화면
- 검색된 뉴스 제목
- 출처 및 날짜 정보
- 원문 내용
- AI 생성 요약문
- 원문 링크

## 🔧 설정 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| 뉴스 개수 | 검색할 뉴스 기사 수 | 5개 |
| 정렬 기준 | 정확도순 또는 최신순 | 정확도순 |
| AI 모델 | OpenAI 또는 Anthropic | OpenAI |

## 🚨 주의사항

- **API 키 보안**: API 키는 개인정보이므로 타인과 공유하지 마세요
- **API 사용량**: AI 모델 API는 사용량에 따라 요금이 부과됩니다
- **속도**: 요약 생성에 몇 초의 시간이 소요될 수 있습니다
- **네트워크**: 인터넷 연결이 필요합니다

## 💡 사용 팁

1. **검색 키워드**: 구체적이고 명확한 키워드를 사용하세요
2. **뉴스 개수**: 너무 많은 수를 선택하면 시간이 오래 걸릴 수 있습니다
3. **AI 모델**: OpenAI는 빠르고 정확하며, Anthropic은 좀 더 자세한 요약을 제공합니다

## 🐛 문제 해결

### 일반적인 오류

1. **API 키 오류**
   - API 키가 올바른지 확인
   - API 키에 충분한 크레딧이 있는지 확인

2. **검색 결과 없음**
   - 다른 키워드로 시도
   - 네이버 API 설정 확인

3. **요약 생성 실패**
   - AI 모델 API 키 확인
   - 인터넷 연결 상태 확인

### 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 개별 설치
pip install streamlit openai anthropic requests
```

## 📞 지원

문제가 발생하거나 개선 사항이 있으시면 이슈를 등록하거나 gpt한테 물어보세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

© 2025 AI 뉴스 요약 에이전트 | 네이버 뉴스 API와 AI 기술 기반
