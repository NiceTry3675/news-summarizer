# AI 뉴스 요약 에이전트

네이버 뉴스 API, NewsAPI와 OpenAI/Anthropic AI 모델을 활용한 스마트 뉴스 요약 서비스입니다.

## 🚀 주요 기능

### 📰 뉴스 검색
- **네이버 뉴스**: 한국 뉴스 중심의 정확한 검색
- **NewsAPI**: 전 세계 뉴스, 다양한 언어 지원
- **실시간 검색**: 키워드를 통한 최신 뉴스 검색

### 🤖 AI 분석
- **스마트 요약**: OpenAI GPT 또는 Anthropic Claude를 사용한 뉴스 요약
- **요약 길이 조절**: 짧게/보통/자세히 중 선택 가능
- **감정 분석**: 뉴스의 긍정/부정/중립 감정 자동 분석
- **키워드 추출**: 중요 키워드 자동 추출 및 태그 표시

### 📑 개인화 기능
- **뉴스 북마크**: 관심 있는 뉴스 저장 및 관리
- **직관적인 UI**: Streamlit 기반의 사용자 친화적 인터페이스
- **다양한 옵션**: 검색 개수, 정렬 기준, 언어 설정 등

## 📋 필요 요구사항

- Python 3.8 이상
- 네이버 개발자센터 API 키 (선택사항)
- NewsAPI 키 (선택사항)
- OpenAI 또는 Anthropic API 키

## 🛠️ 설치 방법

1. **프로젝트 클론**
   ```bash
   git clone https://github.com/your-username/news-summarizer.git
   cd news-summarizer
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

### 1. 뉴스 API (택 1 또는 둘 다)

#### 네이버 뉴스 API
1. [네이버 개발자센터](https://developers.naver.com/)에 접속
2. 로그인 후 '애플리케이션 등록' 클릭
3. 다음 정보로 애플리케이션 등록:
   - 애플리케이션 이름: AI 뉴스 요약 에이전트
   - 사용 API: 검색
   - 웹 서비스 URL: http://localhost (로컬 테스트용)
4. 등록 완료 후 Client ID와 Client Secret 복사
5. 귀찮으시면 이거 쓰세요 Client ID = HR1ViOWJh1QauFSYrqqH
Client Secret = 83RXfyuce_

#### NewsAPI
1. [NewsAPI](https://newsapi.org/)에 접속
2. 무료 계정 생성 (하루 1,000회 요청 제한)
3. API 키 복사

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
   - 사이드바에서 뉴스 소스 선택 (네이버 뉴스 또는 NewsAPI)
   - 선택한 뉴스 API의 키 입력
   - AI 모델 선택 (OpenAI 또는 Anthropic)
   - 선택한 AI 모델의 API 키 입력

4. **뉴스 검색 및 분석**
   - 메인 화면에서 검색 키워드 입력
   - 요약할 뉴스 개수, 정렬 기준, 요약 길이 선택
   - 감정 분석 및 키워드 추출 옵션 선택
   - '뉴스 검색 및 요약' 버튼 클릭

## 📱 사용 화면

### 메인 화면
- **검색 설정**: 키워드 입력, 뉴스 개수 (1~10개), 정렬 기준
- **분석 옵션**: 요약 길이 (짧게/보통/자세히), 감정 분석, 키워드 추출
- **검색 버튼**: 뉴스 검색 및 AI 분석 실행

### 사이드바
- **뉴스 소스 선택**: 네이버 뉴스 또는 NewsAPI
- **API 설정**: 선택한 뉴스 API 및 AI 모델 키 입력
- **저장된 뉴스**: 북마크한 뉴스 목록 및 관리
- **API 키 발급 가이드**: 각 서비스별 가이드 링크

### 결과 화면
- **뉴스 정보**: 제목, 출처, 날짜, API 소스
- **AI 분석 결과**:
  - 📝 요약문 (길이별 맞춤 요약)
  - 😊 감정 분석 (긍정/부정/중립 + 이유)
  - 🔑 주요 키워드 (태그 형태 표시)
- **상호작용**: 원문 링크, 북마크 저장 버튼

## 🔧 설정 옵션

| 카테고리 | 옵션 | 설명 | 기본값 |
|----------|------|------|--------|
| **뉴스 검색** | 뉴스 소스 | 네이버 뉴스 또는 NewsAPI | 네이버 뉴스 |
| | 뉴스 개수 | 검색할 뉴스 기사 수 | 5개 |
| | 정렬 기준 | 정확도순 또는 최신순 | 정확도순 |
| | 언어 설정 | NewsAPI 언어 (ko/en/zh/ja) | 한국어 |
| **AI 분석** | AI 모델 | OpenAI 또는 Anthropic | OpenAI |
| | 요약 길이 | 짧게/보통/자세히 | 보통 |
| | 감정 분석 | 활성화/비활성화 | 활성화 |
| | 키워드 추출 | 활성화/비활성화 | 활성화 |

## ✨ 새로운 기능 상세

### 🎯 요약 길이 조절
- **짧게**: 1-2문장으로 핵심만 간단히
- **보통**: 3-4문장으로 균형잡힌 요약
- **자세히**: 5-6문장으로 배경정보 포함

### 😊 감정 분석
- 뉴스의 전체적인 톤 분석
- 긍정/부정/중립 분류 + 분석 이유 제공
- 이모지와 색상으로 직관적 표시

### 🔑 키워드 추출
- AI가 자동으로 중요 키워드 5개 추출
- 태그 형태로 깔끔하게 표시
- 뉴스 주제를 한눈에 파악 가능

### 📑 뉴스 북마크
- 관심 있는 뉴스를 "📑 저장" 버튼으로 북마크
- 사이드바에서 저장된 뉴스 목록 확인
- 요약, 출처 정보와 함께 저장
- 불필요한 북마크 삭제 가능

## 🌍 뉴스 소스별 특징

### 네이버 뉴스
- ✅ 한국 뉴스 중심
- ✅ 높은 검색 정확도
- ✅ 실시간 업데이트
- ✅ 무료 사용

### NewsAPI
- ✅ 전 세계 뉴스 커버리지
- ✅ 다양한 언어 지원
- ✅ 국제 뉴스 소스
- ⚠️ 무료 계정 하루 1,000회 제한

## 🚨 주의사항

- **API 키 보안**: API 키는 개인정보이므로 타인과 공유하지 마세요
- **API 사용량**: AI 모델 API는 사용량에 따라 요금이 부과됩니다
- **NewsAPI 제한**: 무료 계정은 하루 1,000회 요청 제한이 있습니다
- **속도**: 분석 기능이 많을수록 처리 시간이 길어질 수 있습니다
- **네트워크**: 인터넷 연결이 필요합니다

## 💡 사용 팁

1. **검색 키워드**: 구체적이고 명확한 키워드를 사용하세요
2. **뉴스 개수**: 너무 많은 수를 선택하면 시간이 오래 걸릴 수 있습니다
3. **AI 모델**: 
   - OpenAI: 빠르고 정확한 분석
   - Anthropic: 더 자세하고 신중한 분석
4. **요약 길이**: 용도에 맞게 선택
   - 빠른 확인: 짧게
   - 일반적 사용: 보통
   - 상세 분석: 자세히
5. **북마크 활용**: 중요한 뉴스는 저장해서 나중에 다시 확인

## 🐛 문제 해결

### 일반적인 오류

1. **API 키 오류**
   - API 키가 올바른지 확인
   - API 키에 충분한 크레딧이 있는지 확인

2. **검색 결과 없음**
   - 다른 키워드로 시도
   - 뉴스 API 설정 확인
   - 언어 설정 확인 (NewsAPI)

3. **분석 생성 실패**
   - AI 모델 API 키 확인
   - 인터넷 연결 상태 확인
   - API 사용량 한도 확인

4. **북마크 저장 안됨**
   - 페이지 새로고침 후 다시 시도
   - 브라우저 쿠키/캐시 확인

### 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 개별 설치
pip install streamlit openai anthropic requests

# 특정 버전 설치 (호환성 문제 시)
pip install streamlit==1.28.0
```

### 성능 최적화
```bash
# 메모리 사용량 최적화
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200

# 캐시 클리어
streamlit cache clear
```

## 📊 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python
- **뉴스 API**: 네이버 뉴스 API, NewsAPI
- **AI 모델**: OpenAI GPT-4o-mini, Anthropic Claude-3-Haiku
- **주요 라이브러리**: requests, json, datetime

## 🔄 업데이트 내역

### v2.0.0 (2025-01-XX)
- ✨ NewsAPI 지원 추가
- ✨ 감정 분석 기능 추가
- ✨ 키워드 추출 기능 추가
- ✨ 뉴스 북마크 기능 추가
- ✨ 요약 길이 조절 기능 추가
- 🎨 UI/UX 개선
- 📱 반응형 레이아웃 적용

### v1.0.0 (2025-01-XX)
- 🎉 초기 버전 출시
- 📰 네이버 뉴스 API 연동
- 🤖 OpenAI/Anthropic AI 요약 기능
- 🖥️ Streamlit 웹 인터페이스

## 📞 지원

문제가 발생하거나 개선 사항이 있으시면:
- GitHub Issues에 등록
- 개발자에게 문의
- AI 어시스턴트에게 질문

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

---

© 2025 AI 뉴스 요약 에이전트 | 네이버 뉴스 API, NewsAPI와 AI 기술 기반
