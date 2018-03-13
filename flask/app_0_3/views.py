# # -*- coding: utf-8 -*-

from flask import request, render_template, make_response
from flask.views import View, MethodView
from models import Todo


# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中


