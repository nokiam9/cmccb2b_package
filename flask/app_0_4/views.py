# # -*- coding: utf-8 -*-

from flask import request, render_template
from models import Todo


# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中
def index():
    return render_template('index.html', rec_count=Todo.objects.count())


def pageview():
    page_num = request.args.get('page_id', default=1, type=int)
    # pipeline = [{
    #     '$sort': {
    #         'published_date': -1,
    #         'crawled_time': -1
    #     }
    # }]
    # cursor = Todo.objects.aggregate(*pipeline, allowDiskUse=True)
    # todos_page = cursor.paginate(page=page_num, per_page=10)  ＃ error！
    todos_page = Todo.objects.order_by("-published_date", "-crawled_time").paginate(page=page_num, per_page=10)
    return render_template('pagination.html', todos_page=todos_page)


def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"