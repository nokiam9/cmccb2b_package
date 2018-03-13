# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from models import Todo

# Mongoengine的调用隐藏在models.py中，数据库设置也在其中，并通过db暴露服务
from models import db

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config.from_pyfile(filename='settings.py')  # 配置文件在settings.py

db.init_app(app)    # 此处连接flask和mongoengine，注意db设置在app.config中，必须提前定义


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pagination')
def pageview():
    page_num = request.args.get('page_id', default=1, type=int)
    todos_page = Todo.objects.paginate(page=page_num, per_page=8)
    return render_template('pagination.html', todos_page=todos_page)


@app.route('/hello')
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=80)





