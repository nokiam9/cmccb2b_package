## 开发记录 2018-04 ##

- 修复pymongo的bug，解决启动时偶尔connect mongo失败的问题
- 修改`main.py`，将@`app.route()`修饰符方式改为`app.add_url_rule()`方式，并将所有页面函数隐藏到`views.py`
- 修改`pagination.html`，点击记录时打开新开窗口显示招标详情，且对未设置提醒的记录改变字体颜色
-
-
