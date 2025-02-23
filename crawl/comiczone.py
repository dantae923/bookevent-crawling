import requests
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_comiczone_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 코믹존 크롤링 시작")
    url = f"https://www.comiczone.co.kr/board/list.php?bdId=event&memNo=&noheader=&mypageFl=&searchField=subject&searchWord={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        items = soup.select('div.event_cont')

        for item in items:
            link_tag = item.select_one('a').get('href')
            link = "https://www.comiczone.co.kr/board/view.php?&bdId=event&sno=" + \
                link_tag.split(",")[1].strip() if link_tag else "#"
            title_tag = item.select_one('div.event_info_cont strong')
            title = title_tag.text.strip() if title_tag else "제목 없음"
            image_tag = item.select_one('div.board_img img')
            image = image_tag["src"] if image_tag else "이미지 없음"
            period_tag = item.select_one('div.board_event_day span')
            period = period_tag.text.strip() if period_tag else "기간 정보 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                data.append({
                    'site': '코믹존',
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
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 코믹존 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")