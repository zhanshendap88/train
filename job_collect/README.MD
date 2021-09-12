对前程无忧网页内容爬取
=

描述
-
涉及内容：关于深圳本科数据分析工作岗位的爬取<br>
反爬手段：无<br>
线程进程：多线程<br>
链接任务数：300个<br>
时间：<br>
耗费时间：<br>
库：涉及xpath，time，csv，requests，selenium<br>

优化空间：
-
功能：<br>
1.建议可以根据搜索关键字定义到不同url<br>
2.建议可以根据网址爬取岗位内容<br>
<br>效率：<br>
1.减少代码量（重复内容封装一下）<br>
2.css选择器可以替代xpath<br>
3.可以用数据库储存和调用<br>
4.可以用scrapy<br>
5.可以尝试用抓包工具<br>

流程
-
1.生成2000页前程无忧岗位列表<br>
2.按照2000个链接的列表，用selenium逐个遍历爬取其中element的内容，涉及内容有：<br>
"jobhref","job","jobtime","salary","demand","benfit","company","companyherf","companyscale","companyindustry"<br>
3.引入异常处理，比如超时，以及页面内容空白的处理，引入多个线程爬取
4.将全部爬取的内容储存至xlsx文件<br>
