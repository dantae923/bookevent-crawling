import os
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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