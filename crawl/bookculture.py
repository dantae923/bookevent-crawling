import requests
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_bookculture_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 북컬쳐 크롤링 시작")
    url = f"https://bookculture.co.kr/product/search.html?banner_action=&keyword={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        items = soup.select('div.box')

        for item in items:
            link_tag = item.select_one("a[href^='/product/detail.html']")
            link = "https://bookculture.co.kr/" + \
                link_tag["href"] if link_tag else "#"
            title_tag = item.select_one("p.name a span")
            title = title_tag.text.strip() if title_tag else "제목 없음"
            image_tag = item.select_one("div.box a img.thumb")
            image = image_tag["src"] if image_tag else "이미지 없음"

            # 행사 상품만 추려냄
            special_keywords = ["예약", "특전", "한정", "사은"]
            is_special = any(keyword in title for keyword in special_keywords)

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", "") and is_special:
                data.append({
                    'site': '북컬쳐',
                    'link': link,
                    'title': title,
                    'image': image
                })

        return data
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []
    finally:
        end_time = datetime.now()
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 북컬쳐 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")