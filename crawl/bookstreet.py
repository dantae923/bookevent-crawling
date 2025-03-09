import requests
from bs4 import BeautifulSoup

def search_google_naver_smartstore(query):
    """구글 검색을 이용해 네이버 스마트스토어 크롤링"""
    google_url = f"https://www.google.com/search?q={query}+site:smartstore.naver.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    response = requests.get(google_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.select(".tF2Cxc")
        
        data = []
        for result in search_results:
            title = result.select_one("h3").text
            link = result.select_one("a")["href"]
            data.append({"title": title, "link": link})

        return data
    else:
        print("구글 검색 크롤링 실패")
        return []

# 테스트 실행
results = search_google_naver_smartstore("카구라바치")
for idx, item in enumerate(results, 1):
    print(f"{idx}. {item['title']} - {item['link']}")
