import sqlite3
import os

# ✅ DB 파일 경로
DB_PATH = os.path.join(os.getcwd(), "events.db")

# ✅ 1️⃣ 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT,
        title TEXT,
        link TEXT,
        image TEXT,
        period TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# ✅ 2️⃣ 데이터 삽입 함수 (중복 방지)
def insert_event(site, title, link, image, period):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM events WHERE site=? AND title=? AND link=?", (site, title, link))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute("INSERT INTO events (site, title, link, image, period) VALUES (?, ?, ?, ?, ?)", 
                       (site, title, link, image, period))
        conn.commit()

    conn.close()

# ✅ 3️⃣ 검색어에 따른 데이터 조회 함수
def get_events(search_query="카구라바치"):
    """ 검색어가 포함된 데이터를 DB에서 가져옴 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT site, title, link, image, period FROM events WHERE title LIKE ? ORDER BY created_at DESC",
                   (f"%{search_query}%",))
    results = cursor.fetchall()
    
    conn.close()
    return [{"site": row[0], "title": row[1], "link": row[2], "image": row[3], "period": row[4]} for row in results]
