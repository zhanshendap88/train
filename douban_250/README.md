对豆瓣网页小说内容爬取
=

描述
-
涉及内容：1000本小说链接里的"书名","作者","出版社"等内容<br>
反爬手段：UA<br>
线程进程：单进程单线程<br>
链接任务数：1000个<br>
时间：6-7秒一个<br>
耗费时间：1.5小时<br>
库：涉及re正则表达式，time，csv，random，requests<br>

流程
-
1.爬取小说页面，返回源代码，用re解析单页其中的20个小说，并加进度条显示直接爬取完毕，时长大概三分钟<br>
2.按照1000个链接的列表，遍历逐个爬取其中的内容，涉及内容有（耗时一个半小时）：<br>
"书名","作者","出版社","出品方","出版年","页数","定价","装帧","ISBN","丛书","译者","原作名","豆瓣评分","5星","4星","3星","2星","1星","评价人数","内容简介","作者简介","网站链接"<br>
3.将全部爬取的内容储存至csv文件<br>