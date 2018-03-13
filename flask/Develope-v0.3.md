## Docker web v0.3 from flask ###

[基础镜像：集成了flask、uwsgi、nginx](https://github.com/tiangolo/uwsgi-nginx-flask-docker)

### 基本结构 ###
- `main.py`：app的主入口，负责启动app并设置url路径和对应的函数
- `settings.py`：新增，用于保存flask所需要的配置，包含mongo等
- `models.py`：存在所有的数据定义，注意MongoDB的引擎设置也在其中
- `uwsgi.ini`：uwsgi配置文件，用于连接Nginx和Flask
- `requirements.txt`：定义Flask所需要的第三方类库，
在创建container时自动安装
- `static/`：存放所有静态文件的目录，这也是flask唯一存放静态文件的目录
    >- `bootstrap/`:bootstrap v4.0的库文件，包含css和js
    >- `imags/`:自定义的图像文件
    >- `js/`:自定义的js脚本
- `templates/`: 存放所有html模版的目录，基于jinja2
- `views.py`：被取消，存放所有web页面的函数，由于docker整合uwsgi时要求必须使用@app.route修饰符，不能使用app.add_route_rule方法

### 遗留任务 ###
- *为什么，mongo连接的初始化经常失败？*
- app修饰符的定义方式，导致main.py非常臃肿，需要想办法拆分到views.py中去
- 列表点击条目时，新开窗口展示招标文档
- 列表按published_date, crawled_time排序，显示最新的招标信息；尚未发送提醒的条目显示告警颜色
- 列表的title显示记录总数，最新爬取的记录数量
- nav增加按钮，直接打开scrapyd：6800的监控窗口

------

### AJAX调用的开发步骤 ###
- 在index.html模版中引入jquery, `<script type=text/javascript src="/static/js/jquery-3.2.1.min.js"></script>`
- 在index.html模版中预留位置，例如`<div class="table-responsive" id="searchResult">`，
有个小技巧，html中有个不可见的input，保存了当前page_id, 而且每次刷新局部页面时，都将序号暂存在该字段
- 在index.html模版中，编写自定义的js函数，实现ajax方法，基本方法是通过url调用http，将结果数据填充到预留位置
```javascript
    function doSearchByPage(pageNo) {
        var url = "/pagination?page_id=" + pageNo;
        document.getElementsByName('currentPage')[0].value = pageNo;

        // 开始使用AJAX的POST方法从url中读取数据，并装入searchResult的元素
        $.ajax({
            type: "GET",
            url: url,
            cache: false
        }).done(function (responseData) {
            $("#searchResult").html(responseData);
        }).fail(function (responseData) {
            alert("error! url=" + url)
        });
    };

    function gotoPage(pageNo) {
        document.getElementsByName('currentPage')[0].value = pageNo
        doSearchByPage(pageNo);
    }
``` 
- 在index.html模版中定义， frame加载完成后，调用自定义js函数第一次打开页面
```javascript
    $(document).ready(
        function () {
            doSearchByPage(1);
        }
    )
```
- 在flask中定义静态url的路由，并构造函数生成局部的html，注意静态url也可以传递参数，形如 `0.0.0.0:3000/pagination?page_id=1`，参数的数值可以通过request.args.get方法获得，
```python
@app.route('/pagination)
def pageview():
    page_num = request.args.get('page_id', default=1, type=int)
    todos_page = Todo.objects.paginate(page=page_num, per_page=8)
    return render_template('pagination.html', todos_page=todos_page)
```
- 在构造函数的模版pagination.html中，直接将翻页按钮的click事件定义为doSearchByPage()，就可以完成局部页面刷新
- todos_page是基于todo的page类，其中`.items`保存了记录内容，`.iter_pages()`提供了可用页面列表





