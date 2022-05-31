from flask import Flask, render_template, request
from flask_cors import CORS
from model import get_posts, create_post

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('content')
        create_post(name, content)

    all_posts = get_posts()

    return render_template('index.html', all_posts = all_posts)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
