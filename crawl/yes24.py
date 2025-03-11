import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import insert_event  # ✅ 공통 DB 함수 불러오기

# ✅ 1️⃣ 예스24 크롤링 함수 (DB 저장 포함)
def crawl_yes24_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 예스24 크롤링 시작")
    url = f"https://event.yes24.com/main?pageNumber=1&pageSize=30&rank=Y&query={search_query}&sortTp=03"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        items = soup.select('a[onclick^="setEWCode(\'007_001\')"]')

        for item in items:
            link_tag = item.get('href', '#')
            link = f"https://event.yes24.com{link_tag}" if link_tag.startswith(
                "/") else link_tag
            title_tag = item.select_one('span.txt_tit')
            title = title_tag.text.strip() if title_tag else "제목 없음"
            image_tag = item.select_one('img')
            image = image_tag.get(
                'data-original', image_tag['src']) if image_tag else "이미지 없음"
            period_tag = item.select_one('span.txt_etc')
            period = period_tag.text.strip() if period_tag else "기간 정보 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                insert_event('예스24', title, link, image, period)  # ✅ DB 저장

            # if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
            #     data.append({
            #         'site': '예스24',
            #         'link': link,
            #         'title': title,
            #         'image': image,
            #         'period': period
            #     })

        # return data
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []
    finally:
        end_time = datetime.now()
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 예스24 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")