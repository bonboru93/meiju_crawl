# meiju_crawl
美剧剧本爬虫

## app.py
总入口  

## renren.py
爬人人美剧页面，得到中英文名、图片、描述  

## springfield.py
首先根据英文名猜测springfield网上的对应url地址，处理引号、the、年份猜测。  
由于google翻译api收费，使用调用google翻译网页版的googletrans库做翻译，注意合并语句一次请求。  

## baidu_meiju.py
使用百度【美剧大全】入口，得到中文名。  
使用百度站内搜索在豆瓣站内搜索中文名，得到英文名、评分、imdb地址。      
爬imdb得评分，英文描述。  
TODO：豆瓣过多请求封ip。  
