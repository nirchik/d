from flask import Flask,request, redirect, url_for, render_template_string
from datetime import datetime

app = Flask(__name__)

bookmarks = []
next_id = 1

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Bookmark Manager</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto; }
    form { display: flex; gap: 8px; margin-bottom: 20px; }
    input { padding: 8px; flex: 1; }
    button { padding: 8px 12px; }
    .item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
    .meta { color: #666; font-size: 12px; }
  </style>
</head>
<body>
  <h1>Bookmark Manager</h1>
  <form method="post" action="{{ url_for('add') }}">
    <input name="title" placeholder="Title" required>
    <input name="url" placeholder="https://example.com" required>
    <button type="submit">Add</button>
  </form>
  {% if bookmarks %}
    {% for b in bookmarks %}
      <div class="item">
        <div>
          <div><a href="{{ b['url'] }}" target="_blank" rel="noopener">{{ b['title'] }}</a></div>
          <div class="meta">{{ b['url'] }} · {{ b['created_at'] }}</div>
        </div>
        <form method="post" action="{{ url_for('delete', bookmark_id=b['id']) }}">
          <button type="submit">Delete</button>
        </form>
      </div>
    {% endfor %}
  {% else %}
    <p>No bookmarks yet.</p>
  {% endif %}
</body>
</html>
"""
@app.route('/',methods=['GET'])
def index():
    return render_template_string(TEMPLATE,bookmarks=bookmarks)

@app.route('/add',methods=['POST'])
def add():
    global next_id
    title = request.form['title']
    url = request.form['url']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%5')
    bookmarks.append({'id': next_id,'title':title,'url':url,'created_at':created_at})
    next_id += 1
    return redirect(url_for('index'))

@app.route('/delete/<int:bookmark_id>', methods = ['POST'])
def delete(bookmark_id):
    global bookmarks
    bookmarks = [b for b in bookmarks if b['id'] != bookmark_id]
    return redirect(url_for('index'))