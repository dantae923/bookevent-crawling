import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import insert_event  # ✅ 공통 DB 함수 불러오기

def crawl_comiccity_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 코믹시티 크롤링 시작")
    url = f"https://www.comicct.com/shop/search_result.php?search_str={search_query}&x=0&y=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        items = soup.select('div[class="box"]')

        for item in items:
            link_title_tag = item.select_one('p.name a')
            link = link_title_tag.get('href', '#')
            title = link_title_tag.text.strip() if link_title_tag else "제목 없음"
            image_tag = item.select_one('div.prdimg img')
            image = image_tag["src"] if image_tag else "이미지 없음"

            # 행사 상품만 추려냄
            special_keywords = ["예약", "특전", "한정"]
            is_special = any(keyword in title for keyword in special_keywords)

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", "") and is_special:
                insert_event('코믹시티', title, link, image, '')  # ✅ DB 저장
                # data.append({
                #     'site': '코믹시티',
                #     'link': link,
                #     'title': title,
                #     'image': image
                # })

        return data
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []
    finally:
        end_time = datetime.now()
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 코믹시티 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")