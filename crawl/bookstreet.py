import requests
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_bookstreet_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 북스트릿 크롤링 시작")
    url = f"https://smartstore.naver.com/bookst/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        data = []
        items = soup.select('a[onclick^="setEWCode"]')

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
                data.append({
                    'site': '예스24',
                    'link': link,
                    'title': title,
                    'image': image,
                    'period': period
                })

        return data
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []
    finally:
        end_time = datetime.now()
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 예스24 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")