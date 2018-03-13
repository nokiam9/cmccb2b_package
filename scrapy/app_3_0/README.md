## Docker scrapy v3.0 from scrapy ##

### 概述 ###
- 在v2的基础上，集成了[scrapyd](http://scrapyd.readthedocs.io/en/stable/)以支持docker启动方式,
并通过crontab容器定时调用
- 启动方式：`docker-compose up -d`，关闭方式: `docker-compose down `
- 需要指定volume以安装`/app/logs`，注意防止文件过多溢出
- 注意：*ECS安装时，需要将`settings.py`的mongo地址从开发模式的`localhost`修改为`mongo`*

### 改进说明 ###
- 更新`scrapyd.cfg`, 配置scrapyd deploy的访问端口
- 新增配置文件`scrapyd.conf`，可以监视scrapyd的运行状态和日志，
使用方法：浏览器打开`0.0.0.0:6800`
- 新增配置文件`requirements.txt`,这是pip的标准安装方式
- 更新`docker-compose.yml`, 增加版本号arg带入dockerfile，
自动引入新版本的app


### 经验之谈 ###
- scrapyd的远程调用采用curl方式，以json方式访问并返回执行状态

### 遗留问题 ###
- scrapyd client基本没使用，现有版本还非常简陋
- scrapyd的logs数据量很大，curl方式启动没办法设置logger的level
