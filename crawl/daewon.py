import requests
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_daewon_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 대원씨아이 크롤링 시작")
    url = "https://dwcishop.co.kr/product/list.html?cate_no=450"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        items = soup.select('div.prdImg a')

        for item in items:
            link_tag = item.get('href', '#')
            link = f"https://dwcishop.co.kr/{link_tag}" if link_tag.startswith(
                "/") else link_tag
            title_image_tag = item.select_one('img')
            title = title_image_tag["alt"] if title_image_tag else "제목 없음"
            image = title_image_tag["src"] if title_image_tag else "이미지 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                data.append({
                    'site': '대원씨아이',
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
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 대원씨아이 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")