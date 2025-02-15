import requests
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_animate_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 애니메이트 크롤링 시작")
    url = f"https://www.animate-onlineshop.co.kr/goods/goods_search.php?keyword={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        items = soup.select('a[href^="../goods/goods_view.php?goodsNo="]')
        
        # 중복 데이터 삭제
        seen_links = set()

        for item in items:
            link_tag = item.get('href', '#')

            if link_tag in seen_links:
                continue

            seen_links.add(link_tag)
            link = "https://www.animate-onlineshop.co.kr" + link_tag[2:] if link_tag.startswith(
                "..") else "https://www.animate-onlineshop.co.kr" + link
            image_tag = item.select_one('img')
            image = image_tag.get('src') if image_tag else "이미지 없음"
            title = image_tag.get('alt') if image_tag else "제목 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                data.append({
                    'site': '애니메이트',
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
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 애니메이트 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")