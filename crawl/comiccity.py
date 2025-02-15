import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
        items = soup.select('div.box')

        for item in items:
            link_tag = item.select_one('p.name a')
            link = link_tag.get('href', '#')
            title = link_tag.text.strip() if link_tag else "제목 없음"
            image_tag = item.select_one('div.prdimg img')
            image = image_tag["src"] if image_tag else "이미지 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", "") and '특전' in title.replace(" ", ""):
                data.append({
                    'site': '코믹시티',
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
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 코믹시티 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")