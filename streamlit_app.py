# streamlit_app.py
import streamlit as st
import requests
import urllib.request
import urllib.parse
import json
import time
from openai import OpenAI
from anthropic import Anthropic

# 페이지 설정
st.set_page_config(
    page_title="AI 뉴스 요약 에이전트",
    page_icon="📰",
    layout="wide"
)

# 앱 제목
st.title("AI 뉴스 요약 에이전트")
st.markdown("네이버 뉴스 API와 AI 모델을 활용한 스마트 뉴스 요약 서비스")
st.markdown("---")

# 사이드바에 API 설정 폼 추가
with st.sidebar:
    st.header("API 설정")
    
    # 네이버 API 설정
    st.subheader("네이버 뉴스 API")
    naver_client_id = st.text_input("Client ID", type="password", 
                                    help="네이버 개발자센터에서 발급받은 Client ID를 입력하세요")
    naver_client_secret = st.text_input("Client Secret", type="password",
                                       help="네이버 개발자센터에서 발급받은 Client Secret을 입력하세요")
    
    st.markdown("""
    👉 [네이버 개발자센터](https://developers.naver.com/)에서 API 키를 발급받으세요
    - 애플리케이션 등록 시 '검색' API 선택
    - 웹 서비스 URL은 로컬 테스트의 경우 http://localhost 입력
    """)
    
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

# 메인 화면
# 검색어 입력
keyword = st.text_input("검색할 뉴스 키워드를 입력하세요", placeholder="예: 인공지능, 기후변화, 경제")

# 검색 옵션 설정
col1, col2 = st.columns(2)
with col1:
    display_count = st.slider("요약할 뉴스 개수", min_value=1, max_value=10, value=5)
with col2:
    sort_option = st.selectbox("정렬 기준", ["정확도순", "최신순"], index=0)
    sort_value = "sim" if sort_option == "정확도순" else "date"

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
            return response_data.get('items', [])
        else:
            st.error(f"API 요청 실패: 응답 코드 {rescode}")
            return []
    except Exception as e:
        st.error(f"API 요청 중 오류 발생: {str(e)}")
        return []

def summarize_with_openai(news):
    """OpenAI API를 사용해 뉴스 기사 요약"""
    # 뉴스 정보 추출
    title = news.get('title', '').replace('<b>', '').replace('</b>', '')
    description = news.get('description', '').replace('<b>', '').replace('</b>', '')
    
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=openai_api_key)
    
    # 프롬프트 구성
    prompt = f"""다음 뉴스 기사를 3-4문장으로 요약해주세요. 핵심 정보만 간결하게 포함하세요.
    
    제목: {title}
    내용: {description}
    
    요약:"""
    
    # OpenAI API 호출
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 뉴스 요약 전문가입니다. 핵심 정보를 간결하고 정확하게 요약해주세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI API 요청 중 오류 발생: {str(e)}")
        return "요약을 생성할 수 없습니다."

def summarize_with_anthropic(news):
    """Anthropic API를 사용해 뉴스 기사 요약"""
    # 뉴스 정보 추출
    title = news.get('title', '').replace('<b>', '').replace('</b>', '')
    description = news.get('description', '').replace('<b>', '').replace('</b>', '')
    
    # Anthropic 클라이언트 초기화
    client = Anthropic(api_key=anthropic_api_key)
    
    # 프롬프트 구성
    prompt = f"""다음 뉴스 기사를 3-4문장으로 요약해주세요. 핵심 정보만 간결하게 포함하세요.
    
    제목: {title}
    내용: {description}
    
    요약:"""
    
    # Anthropic API 호출
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            system="당신은 뉴스 요약 전문가입니다. 핵심 정보를 간결하고 정확하게 요약해주세요.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    except Exception as e:
        st.error(f"Anthropic API 요청 중 오류 발생: {str(e)}")
        return "요약을 생성할 수 없습니다."

# 검색 및 요약 수행
if search_pressed:
    if not keyword:
        st.warning("검색어를 입력해주세요.")
    elif not naver_client_id or not naver_client_secret:
        st.error("네이버 API 설정이 필요합니다. 사이드바에서 Client ID와 Secret을 입력해주세요.")
    elif model_type == "OpenAI" and not openai_api_key:
        st.error("OpenAI API 키가 필요합니다. 사이드바에서 API 키를 입력해주세요.")
    elif model_type == "Anthropic" and not anthropic_api_key:
        st.error("Anthropic API 키가 필요합니다. 사이드바에서 API 키를 입력해주세요.")
    else:
        # 검색 진행
        with st.spinner('뉴스를 검색하고 요약 중입니다...'):
            # 네이버 뉴스 API 검색
            news_results = search_naver_news(keyword, display_count, sort_value)
            
            if not news_results:
                st.info("검색 결과가 없습니다. 다른 키워드로 시도해보세요.")
            else:
                st.success(f"{len(news_results)}개의 뉴스를 찾았습니다.")
                
                # 진행 상황 표시
                progress_bar = st.progress(0)
                summarized_news = []
                
                # 각 뉴스 요약
                for i, news in enumerate(news_results):
                    # 뉴스 요약
                    if model_type == "OpenAI":
                        summary = summarize_with_openai(news)
                    else:  # Anthropic
                        summary = summarize_with_anthropic(news)
                    
                    summarized_news.append({
                        "original": news,
                        "summary": summary
                    })
                    
                    # 진행 상황 업데이트
                    progress_bar.progress((i + 1) / len(news_results))
                    time.sleep(0.1)  # UI 업데이트를 위한 짧은 지연
                
                # 결과 표시
                for i, item in enumerate(summarized_news):
                    news = item["original"]
                    summary = item["summary"]
                    
                    with st.container():
                        st.subheader(f"{i+1}. {news['title'].replace('<b>', '').replace('</b>', '')}")
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.write(f"**출처:** {news.get('source', '정보 없음')}")
                            st.write(f"**날짜:** {news.get('pubDate', '정보 없음')[:10]}")
                        with col2:
                            st.write(f"**원문:** {news['description'].replace('<b>', '').replace('</b>', '')}")
                            st.write("**AI 요약:**")
                            st.info(summary)
                        
                        # 원문 링크
                        st.markdown(f"[원문 보기]({news['link']})")
                        st.divider()

# 앱 사용 방법 안내
with st.expander("📚 사용 방법"):
    st.markdown("""
    ### 네이버 뉴스 API 요약 에이전트 사용법
    
    1. 사이드바에서 **네이버 API 설정**과 **AI 모델 설정**을 완료합니다.
    2. 메인 화면에서 검색할 **뉴스 키워드**를 입력합니다.
    3. 요약할 뉴스 개수와 정렬 기준을 선택합니다.
    4. **뉴스 검색 및 요약** 버튼을 클릭합니다.
    5. 검색된 뉴스와 AI 모델이 생성한 요약을 확인합니다.
    
    ### API 키 발급 방법
    
    - **네이버 API**: [네이버 개발자센터](https://developers.naver.com/)에서 애플리케이션 등록 후 발급
    - **OpenAI API**: [OpenAI 플랫폼](https://platform.openai.com/api-keys)에서 계정 생성 후 API 키 발급
    - **Anthropic API**: [Anthropic 콘솔](https://console.anthropic.com/)에서 계정 생성 후 API 키 발급
    """)

# 푸터
st.markdown("---")
st.markdown("© 2025 AI 뉴스 요약 에이전트 | 네이버 뉴스 API와 AI 기술 기반")