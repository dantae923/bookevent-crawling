from crawl import crawl_all_events
from flask import Flask, render_template, request


app = Flask(__name__)


# 검색 페이지
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        selected_sites = request.form.getlist('sites')
        events = crawl_all_events(search_query, selected_sites)

        return render_template('index.html', events=events, query=search_query)
    
    return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
