import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import insert_event  # ✅ 공통 DB 함수 불러오기

def crawl_animate_event_details(search_query, filter_special=True, exclude_soldout=True):
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
        items = soup.select('div.item_cont')
        
        # 중복 데이터 삭제
        seen_links = set()

        for item in items:
            # 🔹 품절 여부 확인
            is_soldout = item.select_one("img[src*='soldout_icon']") is not None
            if exclude_soldout and is_soldout:
               continue  # 품절 상품 제외 옵션이 True면 건너뛰기

            # 🔹 특전 상품 필터링
            special_icon = item.select_one("div.item_icon_box img")
            special_text = special_icon.get("alt", "") + special_icon.get("title", "") if special_icon else ""
            special_keywords = ["예약", "특전", "한정"]

            # # 🔹 상품 아이콘의 alt 또는 title 속성에서 특전 여부 확인
            is_special = any(keyword in special_text for keyword in special_keywords)

            if filter_special and not is_special:
                continue  # 특전 상품만 가져오는 옵션이 True면, 특전이 없는 상품은 제외

            link_tag = item.select_one("div.item_tit_box a")

            if link_tag in seen_links:
                continue

            seen_links.add(link_tag)
            link = link_tag.get("href", "#") if link_tag else "#"
            link = "https://www.animate-onlineshop.co.kr" + link[2:] if link.startswith(
                "..") else "https://www.animate-onlineshop.co.kr" + link
            title_tag = item.select_one("div.item_tit_box a strong.item_name")
            title = title_tag.text.strip() if title_tag else "제목 없음"
            image_tag = item.select_one("div.item_photo_box a img")
            image = image_tag["src"] if image_tag else "이미지 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                insert_event('애니메이트', title, link, image, '')  # ✅ DB 저장
                # data.append({
                #     'site': '애니메이트',
                #     'link': link,
                #     'title': title,
                #     'image': image
                # })
        
        #return data
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []
    finally:
        end_time = datetime.now()
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 애니메이트 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")