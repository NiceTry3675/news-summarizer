# 간단한 뉴스 요약 예제 실행하기
# 실제 환경에서는 API 키가 필요하지만, 예제로 코드가 어떻게 동작하는지 보여드리겠습니다.

import json
import re
from datetime import datetime

# 샘플 뉴스 데이터
sample_news = {
    "title": "<b>인공지능</b> 기술 발전으로 새로운 일자리 창출된다",
    "link": "https://example.com/news1",
    "description": "최신 <b>인공지능</b> 기술의 발전이 기존 일자리를 대체하는 것이 아니라 새로운 형태의 직업을 만들어내고 있다는 연구 결과가 발표됐다. 전문가들은 AI 트레이너, 데이터 분석가 등의 직업이 급부상할 것으로 전망했다.",
    "pubDate": "Mon, 15 Jan 2024 10:30:00 +0900",
    "source": "테크뉴스"
}

# HTML 태그 제거 함수
def remove_html_tags(text):
    return re.sub(r'<.*?>', '', text)

# 요약 함수 - 실제로는 OpenAI/Anthropic API를 호출하지만 여기서는 간단히 시뮬레이션
def simulate_ai_summary(news, model_type="openai"):
    # 입력 데이터 정리
    title = remove_html_tags(news["title"])
    description = remove_html_tags(news["description"])
    
    # 모델 유형에 따라 다른 요약 스타일 시뮬레이션
    if model_type == "openai":
        return f"OpenAI 모델 요약: {title}. {description[:100]}... (이하 생략)"
    else:  # anthropic
        return f"Claude 모델 요약: {title}. {description[:80]}... (이하 생략)"

# 뉴스 정보 가공 및 표시
def process_news(news_item, model_type="openai"):
    # 데이터 정리
    title = remove_html_tags(news_item["title"])
    description = remove_html_tags(news_item["description"])
    
    # pubDate 포맷 변환
    try:
        pub_date = datetime.strptime(news_item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
        formatted_date = pub_date.strftime("%Y-%m-%d %H:%M")
    except:
        formatted_date = news_item["pubDate"]
    
    # 요약 생성
    summary = simulate_ai_summary(news_item, model_type)
    
    # 결과 반환
    return {
        "title": title,
        "description": description,
        "link": news_item["link"],
        "pubDate": formatted_date,
        "source": news_item.get("source", "알 수 없음"),
        "summary": summary
    }

# 샘플 뉴스 처리 예제
print("=== 네이버 뉴스 API + AI 요약 예제 ===\n")

# OpenAI 모델 시뮬레이션
print("[OpenAI 모델 사용 시]")
processed_news_openai = process_news(sample_news, "openai")
print(json.dumps(processed_news_openai, indent=2, ensure_ascii=False))
print()

# Anthropic 모델 시뮬레이션
print("[Anthropic 모델 사용 시]")
processed_news_anthropic = process_news(sample_news, "anthropic")
print(json.dumps(processed_news_anthropic, indent=2, ensure_ascii=False))

# 실제 애플리케이션 흐름 설명
print("\n=== 실제 애플리케이션 실행 흐름 ===")
print("1. 사용자가 검색어 입력")
print("2. 네이버 뉴스 API로 뉴스 검색")
print("3. 검색된 뉴스 데이터 전처리")
print("4. 선택된 AI 모델(OpenAI/Anthropic)로 뉴스 요약")
print("5. 요약 결과를 사용자에게 표시")
print("\n* 실제 실행을 위해서는 네이버 API 키와 OpenAI/Anthropic API 키가 필요합니다.")