# streamlit_app.py
import streamlit as st
import requests
import urllib.request
import urllib.parse
import json
import time
from datetime import datetime
from openai import OpenAI
from anthropic import Anthropic

# 페이지 설정
st.set_page_config(
    page_title="AI 뉴스 요약 에이전트",
    page_icon="📰",
    layout="wide"
)

# 세션 상태 초기화
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []

# 앱 제목
st.title("AI 뉴스 요약 에이전트")
st.markdown("네이버 뉴스 API와 NewsAPI를 활용한 스마트 뉴스 요약 서비스")
st.markdown("---")

# 사이드바에 API 설정 폼 추가
with st.sidebar:
    st.header("API 설정")
    
    # 뉴스 소스 선택
    st.subheader("뉴스 소스 선택")
    news_source = st.radio("사용할 뉴스 API", ["네이버 뉴스", "NewsAPI"])
    
    # 네이버 API 설정
    if news_source == "네이버 뉴스":
        st.subheader("네이버 뉴스 API")
        naver_client_id = st.text_input("Naver Client ID", type="password", 
                                        help="네이버 개발자센터에서 발급받은 Client ID를 입력하세요")
        naver_client_secret = st.text_input("Naver Client Secret", type="password",
                                           help="네이버 개발자센터에서 발급받은 Client Secret을 입력하세요")
        
        st.markdown("""
        👉 [네이버 개발자센터](https://developers.naver.com/)에서 API 키를 발급받으세요
        - 애플리케이션 등록 시 '검색' API 선택
        - 웹 서비스 URL은 로컬 테스트의 경우 http://localhost 입력
        """)
        newsapi_key = None
        newsapi_language = "ko"
    else:
        naver_client_id = None
        naver_client_secret = None
    
    # NewsAPI 설정
    if news_source == "NewsAPI":
        st.subheader("NewsAPI")
        newsapi_key = st.text_input("NewsAPI Key", type="password",
                                   help="NewsAPI에서 발급받은 API 키를 입력하세요")
        
        # NewsAPI 설정 옵션
        newsapi_language = st.selectbox("언어 설정", 
                                      ["ko", "en", "zh", "ja"], 
                                      index=0,
                                      help="ko=한국어, en=영어, zh=중국어, ja=일본어")
        
        st.markdown("""
        👉 [NewsAPI](https://newsapi.org/)에서 무료 API 키를 발급받으세요
        - 무료 계정: 하루 1,000회 요청 제한
        - 개발용으로 충분한 할당량 제공
        """)
    else:
        newsapi_key = None
        newsapi_language = "ko"
    
    # AI 모델 설정
    st.subheader("AI 모델 API")
    model_type = st.radio("사용할 AI 모델", ["OpenAI", "Anthropic"])
    
    if model_type == "OpenAI":
        openai_api_key = st.text_input("OpenAI API Key", type="password",
                                       help="OpenAI API 키를 입력하세요")
        st.markdown("[OpenAI API 키 발급받기](https://platform.openai.com/api-keys)")
        ai_model = "gpt-4o-mini"
    else:
        anthropic_api_key = st.text_input("Anthropic API Key", type="password",
                                         help="Anthropic API 키를 입력하세요")
        st.markdown("[Anthropic API 키 발급받기](https://console.anthropic.com/)")
        ai_model = "claude-3-haiku-20240307"
    
    # 북마크 표시
    st.markdown("---")
    st.subheader("📑 저장된 뉴스")
    if st.session_state.bookmarks:
        for i, bookmark in enumerate(st.session_state.bookmarks):
            with st.expander(f"📌 {bookmark['title'][:30]}..."):
                st.write(f"**요약:** {bookmark['summary']}")
                st.write(f"**출처:** {bookmark['source']}")
                if st.button(f"삭제", key=f"delete_{i}"):
                    st.session_state.bookmarks.pop(i)
                    st.rerun()
    else:
        st.write("저장된 뉴스가 없습니다.")

# 메인 화면
# 검색어 입력
keyword = st.text_input("검색할 뉴스 키워드를 입력하세요", placeholder="예: 인공지능, 기후변화, 경제")

# 검색 옵션 설정
col1, col2, col3 = st.columns(3)
with col1:
    display_count = st.slider("요약할 뉴스 개수", min_value=1, max_value=10, value=5)
with col2:
    sort_option = st.selectbox("정렬 기준", ["정확도순", "최신순"], index=0)
    sort_value = "sim" if sort_option == "정확도순" else "date"
with col3:
    summary_length = st.selectbox("요약 길이", ["짧게", "보통", "자세히"], index=1)

# 분석 옵션
col4, col5 = st.columns(2)
with col4:
    enable_sentiment = st.checkbox("감정 분석 포함", value=True)
with col5:
    enable_keywords = st.checkbox("키워드 추출 포함", value=True)

# 검색 버튼
search_pressed = st.button("뉴스 검색 및 요약", type="primary")

# 뉴스 검색 및 요약 함수
def search_naver_news(keyword, display=5, sort='sim'):
    """네이버 뉴스 API를 사용해 뉴스 검색"""
    encText = urllib.parse.quote(keyword)
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}&sort={sort}"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)
    
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        
        if rescode == 200:
            response_body = response.read()
            response_data = json.loads(response_body.decode('utf-8'))
            items = response_data.get('items', [])
            
            # 네이버 API 결과를 표준 형태로 변환
            standardized_items = []
            for item in items:
                standardized_items.append({
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'url': item.get('link', ''),
                    'source': item.get('source', '네이버 뉴스'),
                    'publishedAt': item.get('pubDate', ''),
                    'api_source': 'naver'
                })
            
            return standardized_items
        else:
            st.error(f"네이버 API 요청 실패: 응답 코드 {rescode}")
            return []
    except Exception as e:
        st.error(f"네이버 API 요청 중 오류 발생: {str(e)}")
        return []

def search_newsapi(keyword, page_size=5, sort_by='relevancy', language='ko'):
    """NewsAPI를 사용해 뉴스 검색"""
    url = "https://newsapi.org/v2/everything"
    
    params = {
        'q': keyword,
        'pageSize': page_size,
        'sortBy': 'relevancy' if sort_by == 'sim' else 'publishedAt',
        'language': language,
        'apiKey': newsapi_key
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            # NewsAPI 결과를 표준 형태로 변환
            standardized_articles = []
            for article in articles:
                standardized_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'NewsAPI'),
                    'publishedAt': article.get('publishedAt', ''),
                    'api_source': 'newsapi'
                })
            
            return standardized_articles
        else:
            st.error(f"NewsAPI 요청 실패: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"NewsAPI 요청 중 오류 발생: {str(e)}")
        return []

def get_summary_prompt(title, description, length):
    """요약 길이에 따른 프롬프트 생성"""
    if length == "짧게":
        return f"""다음 뉴스 기사를 1-2문장으로 핵심만 간단히 요약해주세요.
        
        제목: {title}
        내용: {description}
        
        요약:"""
    elif length == "보통":
        return f"""다음 뉴스 기사를 3-4문장으로 요약해주세요. 핵심 정보만 간결하게 포함하세요.
        
        제목: {title}
        내용: {description}
        
        요약:"""
    else:  # 자세히
        return f"""다음 뉴스 기사를 5-6문장으로 자세히 요약해주세요. 배경 정보와 세부 내용을 포함하세요.
        
        제목: {title}
        내용: {description}
        
        요약:"""

def analyze_with_openai(news, length, include_sentiment=False, include_keywords=False):
    """OpenAI API를 사용해 뉴스 기사 분석"""
    title = news.get('title', '').replace('<b>', '').replace('</b>', '')
    description = news.get('description', '').replace('<b>', '').replace('</b>', '')
    
    client = OpenAI(api_key=openai_api_key)
    
    # 기본 요약 프롬프트
    summary_prompt = get_summary_prompt(title, description, length)
    
    try:
        # 요약 생성
        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 뉴스 요약 전문가입니다. 핵심 정보를 간결하고 정확하게 요약해주세요."},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        summary = summary_response.choices[0].message.content.strip()
        
        result = {"summary": summary}
        
        # 감정 분석
        if include_sentiment:
            sentiment_prompt = f"""다음 뉴스의 전체적인 감정을 분석해주세요. '긍정', '부정', '중립' 중 하나로 답하고, 한 줄로 이유를 설명해주세요.
            
            제목: {title}
            내용: {description}"""
            
            sentiment_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 텍스트 감정 분석 전문가입니다."},
                    {"role": "user", "content": sentiment_prompt}
                ],
                temperature=0.1,
                max_tokens=100
            )
            result["sentiment"] = sentiment_response.choices[0].message.content.strip()
        
        # 키워드 추출
        if include_keywords:
            keywords_prompt = f"""다음 뉴스에서 가장 중요한 키워드 5개를 추출해주세요. 쉼표로 구분해서 나열해주세요.
            
            제목: {title}
            내용: {description}"""
            
            keywords_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 키워드 추출 전문가입니다."},
                    {"role": "user", "content": keywords_prompt}
                ],
                temperature=0.1,
                max_tokens=100
            )
            result["keywords"] = keywords_response.choices[0].message.content.strip()
        
        return result
    except Exception as e:
        st.error(f"OpenAI API 요청 중 오류 발생: {str(e)}")
        return {"summary": "분석을 생성할 수 없습니다."}

def analyze_with_anthropic(news, length, include_sentiment=False, include_keywords=False):
    """Anthropic API를 사용해 뉴스 기사 분석"""
    title = news.get('title', '').replace('<b>', '').replace('</b>', '')
    description = news.get('description', '').replace('<b>', '').replace('</b>', '')
    
    client = Anthropic(api_key=anthropic_api_key)
    
    try:
        # 분석 요청을 하나의 프롬프트로 통합
        analysis_parts = []
        analysis_parts.append(get_summary_prompt(title, description, length))
        
        if include_sentiment:
            analysis_parts.append("\n\n추가로, 이 뉴스의 감정을 '긍정', '부정', '중립' 중 하나로 분석하고 이유를 한 줄로 설명해주세요.")
        
        if include_keywords:
            analysis_parts.append("\n\n또한, 이 뉴스에서 가장 중요한 키워드 5개를 쉼표로 구분해서 추출해주세요.")
        
        combined_prompt = "".join(analysis_parts)
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=400,
            system="당신은 뉴스 분석 전문가입니다. 요약, 감정 분석, 키워드 추출을 정확하게 수행해주세요.",
            messages=[
                {"role": "user", "content": combined_prompt}
            ]
        )
        
        full_response = response.content[0].text.strip()
        
        # 응답을 파싱해서 구분
        result = {"summary": full_response}
        
        # 간단한 파싱 (실제로는 더 정교한 파싱이 필요할 수 있음)
        if include_sentiment and include_keywords:
            lines = full_response.split('\n')
            if len(lines) >= 3:
                result["summary"] = lines[0]
                result["sentiment"] = lines[-2] if '감정' in lines[-2] or '긍정' in lines[-2] or '부정' in lines[-2] or '중립' in lines[-2] else "분석 실패"
                result["keywords"] = lines[-1] if ',' in lines[-1] else "추출 실패"
        
        return result
    except Exception as e:
        st.error(f"Anthropic API 요청 중 오류 발생: {str(e)}")
        return {"summary": "분석을 생성할 수 없습니다."}

# 검색 및 요약 수행
if search_pressed:
    if not keyword:
        st.warning("검색어를 입력해주세요.")
    elif model_type == "OpenAI" and not openai_api_key:
        st.error("OpenAI API 키가 필요합니다. 사이드바에서 API 키를 입력해주세요.")
    elif model_type == "Anthropic" and not anthropic_api_key:
        st.error("Anthropic API 키가 필요합니다. 사이드바에서 API 키를 입력해주세요.")
    else:
        # API 키 유효성 검사
        api_configured = False
        
        if news_source == "네이버 뉴스":
            if naver_client_id and naver_client_secret:
                api_configured = True
            else:
                st.error("네이버 API 설정이 필요합니다. 사이드바에서 Client ID와 Secret을 입력해주세요.")
        elif news_source == "NewsAPI":
            if newsapi_key:
                api_configured = True
            else:
                st.error("NewsAPI 키가 필요합니다. 사이드바에서 API 키를 입력해주세요.")
        
        if api_configured:
            # 검색 진행
            with st.spinner('뉴스를 검색하고 분석 중입니다...'):
                # 선택된 API로 뉴스 검색
                if news_source == "네이버 뉴스":
                    news_results = search_naver_news(keyword, display_count, sort_value)
                else:  # NewsAPI
                    news_results = search_newsapi(keyword, display_count, sort_value, newsapi_language)
                
                if not news_results:
                    st.info("검색 결과가 없습니다. 다른 키워드로 시도해보세요.")
                else:
                    st.success(f"{len(news_results)}개의 뉴스를 찾았습니다.")
                    
                    # 진행 상황 표시
                    progress_bar = st.progress(0)
                    analyzed_news = []
                    
                    # 각 뉴스 분석
                    for i, news in enumerate(news_results):
                        # 뉴스 분석
                        if model_type == "OpenAI":
                            analysis = analyze_with_openai(news, summary_length, enable_sentiment, enable_keywords)
                        else:  # Anthropic
                            analysis = analyze_with_anthropic(news, summary_length, enable_sentiment, enable_keywords)
                        
                        analyzed_news.append({
                            "original": news,
                            "analysis": analysis
                        })
                        
                        # 진행 상황 업데이트
                        progress_bar.progress((i + 1) / len(news_results))
                        time.sleep(0.1)  # UI 업데이트를 위한 짧은 지연
                    
                    # 결과 표시
                    for i, item in enumerate(analyzed_news):
                        news = item["original"]
                        analysis = item["analysis"]
                        
                        with st.container():
                            st.subheader(f"{i+1}. {news['title'].replace('<b>', '').replace('</b>', '')}")
                            
                            # 뉴스 정보 및 분석 결과
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.write(f"**출처:** {news.get('source', '정보 없음')}")
                                # 날짜 형식 처리
                                published_date = news.get('publishedAt', '정보 없음')
                                if published_date != '정보 없음':
                                    if news.get('api_source') == 'newsapi':
                                        try:
                                            parsed_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                                            formatted_date = parsed_date.strftime('%Y-%m-%d')
                                        except:
                                            formatted_date = published_date[:10]
                                    else:
                                        formatted_date = published_date[:10]
                                else:
                                    formatted_date = '정보 없음'
                                st.write(f"**날짜:** {formatted_date}")
                                st.write(f"**API:** {news.get('api_source', '').upper()}")
                                
                                # 북마크 버튼
                                if st.button(f"📑 저장", key=f"bookmark_{i}"):
                                    bookmark_data = {
                                        "title": news['title'].replace('<b>', '').replace('</b>', ''),
                                        "summary": analysis.get('summary', ''),
                                        "source": news.get('source', ''),
                                        "url": news['url']
                                    }
                                    st.session_state.bookmarks.append(bookmark_data)
                                    st.success("뉴스가 저장되었습니다!")
                                    time.sleep(1)
                                    st.rerun()
                            
                            with col2:
                                st.write(f"**원문:** {news['description'].replace('<b>', '').replace('</b>', '')}")
                                st.write("**AI 요약:**")
                                st.info(analysis.get('summary', '요약 없음'))
                                
                                # 감정 분석 결과
                                if enable_sentiment and 'sentiment' in analysis:
                                    st.write("**감정 분석:**")
                                    sentiment = analysis['sentiment']
                                    if '긍정' in sentiment:
                                        st.success(f"😊 {sentiment}")
                                    elif '부정' in sentiment:
                                        st.error(f"😔 {sentiment}")
                                    else:
                                        st.info(f"😐 {sentiment}")
                                
                                # 키워드 추출 결과
                                if enable_keywords and 'keywords' in analysis:
                                    st.write("**주요 키워드:**")
                                    keywords = analysis['keywords'].split(',')
                                    keyword_tags = []
                                    for kw in keywords[:5]:  # 최대 5개만 표시
                                        keyword_tags.append(f"`{kw.strip()}`")
                                    st.markdown(" ".join(keyword_tags))
                            
                            # 원문 링크
                            st.markdown(f"[원문 보기]({news['url']})")
                            st.divider()

# 앱 사용 방법 안내
with st.expander("📚 사용 방법"):
    st.markdown("""
    ### 뉴스 API 요약 에이전트 사용법
    
    1. 사이드바에서 **뉴스 소스 선택** (네이버 뉴스 또는 NewsAPI)
    2. 선택한 뉴스 소스의 **API 설정**과 **AI 모델 설정**을 완료합니다.
    3. 메인 화면에서 검색할 **뉴스 키워드**를 입력합니다.
    4. 요약할 뉴스 개수, 정렬 기준, **요약 길이**를 선택합니다.
    5. **감정 분석**과 **키워드 추출** 옵션을 선택합니다.
    6. **뉴스 검색 및 요약** 버튼을 클릭합니다.
    7. 검색된 뉴스와 AI 분석 결과를 확인합니다.
    8. 관심 있는 뉴스는 **📑 저장** 버튼으로 북마크할 수 있습니다.
    
    ### 새로운 기능
    
    - **🎯 요약 길이 조절**: 짧게/보통/자세히 중 선택
    - **😊 감정 분석**: 뉴스의 긍정/부정/중립 감정 자동 분석
    - **🔑 키워드 추출**: 중요 키워드 자동 추출 및 태그 표시
    - **📑 뉴스 북마크**: 관심 있는 뉴스 저장 및 관리
    
    ### API 키 발급 방법
    
    - **네이버 API**: [네이버 개발자센터](https://developers.naver.com/)에서 애플리케이션 등록 후 발급
    - **NewsAPI**: [NewsAPI](https://newsapi.org/)에서 무료 계정 생성 후 API 키 발급
    - **OpenAI API**: [OpenAI 플랫폼](https://platform.openai.com/api-keys)에서 계정 생성 후 API 키 발급
    - **Anthropic API**: [Anthropic 콘솔](https://console.anthropic.com/)에서 계정 생성 후 API 키 발급
    
    ### 뉴스 소스별 특징
    
    - **네이버 뉴스**: 한국 뉴스 중심, 높은 검색 정확도
    - **NewsAPI**: 전 세계 뉴스, 다양한 언어 지원, 무료 계정 하루 1,000회 제한
    """)

# 푸터
st.markdown("---")
st.markdown("© 2025 AI 뉴스 요약 에이전트 | 네이버 뉴스 API, NewsAPI와 AI 기술 기반")