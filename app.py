import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# 크롤링 함수

# yes24
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

# 교보문고
def crawl_kyobo_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 교보문고 크롤링 시작")
    url = f"https://event.kyobobook.co.kr/?search={search_query}"

    # Selenium WebDriver 최적화 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 (UI 없이 실행)
    # GPU 사용 안 함 (Windows 환경에서 필요)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # 보안 정책 비활성화 (Linux에서 필요)
    chrome_options.add_argument("--disable-extensions")  # 확장 프로그램 비활성화
    chrome_options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 방지
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")  # 자동화 탐지 방지

    # 불필요한 리소스 로드 차단 (이미지, CSS)
    prefs = {
        "profile.managed_default_content_settings.images": 2,  # 이미지 로드 안 함
        "profile.managed_default_content_settings.stylesheets": 2,  # CSS 로드 함
        "profile.managed_default_content_settings.cookies": 1,  # 쿠키 안 받음
        "profile.managed_default_content_settings.javascript": 1  # JavaScript 유지
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Selenium WebDriver 설정
    # ChromeDriver 경로
    base_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(base_dir, "drivers", "chromedriver.exe")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    try:
        # 1️⃣ 페이지가 완전히 로딩될 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        # 2️⃣ JavaScript 실행 완료를 위한 추가 대기
        time.sleep(3)

        # 3️⃣ 스크롤을 끝까지 내려서 동적 데이터 로드 강제 실행
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 스크롤 후 데이터 로딩 대기

        # 4️⃣ `event_link` 요소가 보일 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.event_link"))
        )

        # BeautifulSoup으로 HTML 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        items = soup.select('a.event_link')  # <a> 태그와 클래스 선택

        for item in items:
            link_tag = item.get('href', '#')
            link = f"https://event.kyobobook.co.kr{link_tag}" if link_tag.startswith(
                "/") else link_tag
            title_tag = item.select_one('div.event_name')
            title = title_tag.text.strip() if title_tag else "제목 없음"
            image_tag = item.select_one('img')
            image = image_tag['src'] if image_tag else "이미지 없음"
            period_tag = item.select_one('div.event_period')
            period = period_tag.text.strip() if period_tag else "기간 정보 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                data.append({
                    'site': '교보문고',
                    'link': link,
                    'title': title,
                    'image': image,
                    'period': period
                })

        return data
    except Exception as e:
        print(f"교보문고 크롤링 중 오류 발생: {e}")
        return []
    finally:
        driver.quit()  # 브라우저 닫기
        end_time = datetime.now()
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 교보문고 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")

# 알라딘
def crawl_aladin_event_details(search_query):
    start_time = datetime.now()
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] 알라딘 크롤링 시작")
    url = "https://www.aladin.co.kr/events/wevent_sub.aspx?CID=2551"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        items = soup.select('table#Table1 tr')

        for item in items:
            link_tag = item.select_one("a.ml")
            link = "https://www.aladin.co.kr" + \
                link_tag["href"] if link_tag else "#"
            title_tag = item.select_one('a.ml h3')
            title = title_tag.text.strip() if title_tag else "제목 없음"
            image_tag = item.select_one('img')
            image = image_tag["src"] if image_tag else "이미지 없음"
            period_tag = item.select_one('span.date')
            period = period_tag.text.strip() if period_tag else "기간 정보 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                data.append({
                    'site': '알라딘',
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
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 알라딘 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")

# 애니메이트
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

# 대원씨아이
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
        items = soup.select('div.name a')

        for item in items:
            link_tag = item.get('href', '#')
            link = f"https://dwcishop.co.kr/{link_tag}" if link_tag.startswith(
                "/") else link_tag
            title_tag = item.find_all("span")
            title = title_tag[-1].text.strip() if title_tag else "제목 없음"
            image_tag = item.select_one('img')
            image = image_tag["src"] if image_tag else "이미지 없음"
            period_tag = item.select_one('span.date')
            period = period_tag.text.strip() if period_tag else "기간 정보 없음"

            if title != '제목 없음' and search_query.replace(" ", "") in title.replace(" ", ""):
                data.append({
                    'site': '대원씨아이',
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
        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] 대원씨아이 크롤링 종료")
        print(f"실행 시간: {end_time - start_time}")


# 모든 사이트 크롤링
def crawl_all_events(search_query):
    yes24_data = crawl_yes24_event_details(search_query)
    kyobo_data = crawl_kyobo_event_details(search_query)
    aladin_data = crawl_aladin_event_details(search_query)
    animate_data = crawl_animate_event_details(search_query)
    return yes24_data + kyobo_data + aladin_data + animate_data

# 로그 파일 저장
def save_to_file(content, filename="C:/Users/Dantae/log_output.txt"):
    try:
        with open(filename, "a", encoding="utf-8") as file:  # "a" 모드는 파일에 내용을 추가
            file.write(content + "\n")
        print(f"내용이 '{filename}'에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")


# 검색 페이지
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        selected_sites = request.form.getlist('sites')

        events = []
        if "yes24" in selected_sites:
            events += crawl_yes24_event_details(search_query)
        if "kyobo" in selected_sites:
            events += crawl_kyobo_event_details(search_query)
        if "aladin" in selected_sites:
            events += crawl_aladin_event_details(search_query)
        if "animate" in selected_sites:
            events += crawl_animate_event_details(search_query)
        if "daewon" in selected_sites:
            events += crawl_daewon_event_details(search_query)

        return render_template('index.html', events=events, query=search_query)
    return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
