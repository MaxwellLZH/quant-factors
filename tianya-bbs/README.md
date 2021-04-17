## 爬取天涯论坛股票板块的讨论帖信息

#### 数据来源
论坛地址：http://bbs.tianya.cn/list.jsp?item=stocks

#### 数据存储
数据用python自带的**shelve**库存储，分成三个文件：
- `article_list.db`: Key是包含页面URL，Value是页面里的文章meta信息（名称、link、阅读量等）。
- `article_tiny.db`: Key是文章的URL，Value包括文章的一些简单信息（作者等级、发布时间等），但不包含帖子具体文本。
- `article_full.db`: Key是文章的URL，Value包含帖子本身和所有回复的文本信息。
