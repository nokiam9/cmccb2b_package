## Project for b2b.10086.cn ##

### 安装方式 ###
1. 在上层目录将全部文件打包`tar -cvf app.tar CMCCB2B`
2. scp到安装主机（已安装docker）并在安装点解包`tar -xvf app.tar`
3. 如果需要，调整user_data的目录设置，或迁移mongo DB数据
4. 启动预安装程序`sh prestart.sh`，并启动主程序`docker-compose up -d --build`
5. 浏览器远程访问`www.caogo.cn`

### 文件清单 ###
- `scrapy/`：后台爬虫应用，其中`app_?_?/`存放app各个版本(version: major+minor)
- `falsk/`：前台web应用，其中`app_?_?/`存放app各个版本 
- `mongo/`：公共数据库应用
- `crontab/`：后台定时任务调度，为scrapy提供服务
- `utils/`:系统维护的一些脚本，包括数据库迁移、数据检查等...
- `user_data`:用户数据，不需要安装，包括db、logs等，*注意：本目录改变时需要调整.yml配置文件*
- `prestart.sh`: 预启动程序，负责设置network并启动mongo，*注意：在启动docker-compose前，必须运行该程序*
- `docker-compose.yml`:主启动程序，自动加载scrapy，flask和crontab容器
- `.gitignore`：设置不需要上传Github的文件类型
