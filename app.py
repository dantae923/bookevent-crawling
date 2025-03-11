#from crawl import crawl_all_events
from flask import Flask, render_template, request
from database import init_db, get_events  # ✅ DB 초기화 & 조회 함수
from crawl import crawl_yes24_event_details

app = Flask(__name__)

# ✅ 서버 실행 시 DB 초기화 & 크롤링 자동 실행
init_db()
print("📢 초기 크롤링 실행 중...")
crawl_yes24_event_details("카구라바치")  # 기본 검색어 크롤링
print("✅ 초기 크롤링 완료! 데이터 저장됨.")

# ✅ 메인 페이지 (DB에서 데이터 가져와서 표시)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        events = get_events()  # ✅ DB에서 검색 결과 가져오기
    else:
        search_query = "카구라바치"  # 기본 검색어
        events = get_events()  # ✅ DB에서 기본 검색 데이터 가져오기
    
    return render_template('index.html', events=events, query=search_query)
# def home():
#     if request.method == 'POST':
#         search_query = request.form.get('search_query', '').strip()
#         selected_sites = request.form.getlist('sites')
#         events = crawl_all_events(search_query, selected_sites)

#         return render_template('index.html', events=events, query=search_query)
    
#     return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
