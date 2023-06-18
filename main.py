from flask import Flask, request, jsonify, render_template
from libs.storages import Storages

storage = Storages()

app = Flask(__name__)

def get_search_data(is_rss=False):
    return storage.search(dict(
        title=request.args.get('title'),
        author=request.args.get('author'),
        size=request.args.get('size'),
    ), is_rss=is_rss)

@app.route('/search', methods=['GET'])
def search():
    return jsonify(get_search_data())

@app.route("/rss")
def rss():
    data = get_search_data(is_rss=True)
    return render_template("rss.xml", data=data)

@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id: str):
    return jsonify(storage.get_item(item_id=item_id))

@app.route('/submit', methods=['POST'])
def store():
    data = storage.add({**request.json, 'user_agent': request.headers.get('User-Agent')})
    return jsonify(data.to_json()), 201

