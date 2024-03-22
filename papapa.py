from lxml import etree
import time
from selenium import webdriver
import pandas as pd
 
#保存电影名和演员信息
title = list()
actor = list()
#加载浏览器驱动
chrome_driver = "E:\ChromeDownload\chromedriver-win64\chromedriver-win64\chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver)
# 设置想要爬取的导演或演员的 数据('徐峥'前加u，目的是保证汉字编码是utf-8)
director = u'吴镇宇'
# 爬取数据的url地址
base_url = 'https://movie.douban.com/subject_search?search_text=' + director + '&cat=1002&start='
 
# 爬取指定页面的数据
def download(request_url):
    driver.get(request_url)
    # 停顿1秒钟
    time.sleep(1)
    # 获得整个文档的HTML
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    # 解析html文档
    html = etree.HTML(html)
    # 拿到的是电影名称列表
    movie_lists = html.xpath(
        "/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']")
    # 拿到的是演员名称列表
    name_lists = html.xpath(
        "/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='meta abstract_2']")
    # 获取返回的数据个数
    num = len(movie_lists)
 
    if num > 15:  # 第一页会有16条数据(第一条数据是导演介绍，因为定位电影名称和演员名称的标签顺序表和导演介绍的标签顺序表一样)
        # 不要导演介绍，所以第一条数据需要去掉
        movie_lists = movie_lists[1:]
        name_lists = name_lists[1:]
    for (movie, name_list) in zip(movie_lists, name_lists):
        # 会存在数据为空的情况(真的有空值，第七页第四条数据，name_list为空值)
        if name_list.text is None:
            # 结束当前迭代，并执行下一次迭代(演员为空的那一条数据舍弃，最终有99条数据)
            continue
        # 添加电影名到集合中
        title.append(movie.text)
        # 添加演员信息到集合中
        actor.append(name_list.text.replace(" ", ""))
    print('OK')  # 代表这页数据下载成功
    if num >= 15:
        # 数据个数>=15，说明这一页数据满了，可能还有下一页，所以返回True，告知程序可以继续下一页去下载数据
        # 继续下一页
        return True
    else:
        # 如果这一页数据小于15，说明后面没有数据了，所以返回False，告知程序没有下一页了
        # 没有下一页
        return False
 
# 开始的ID为0，每页增加15(因为url地址后面的数字，当切换到下一页时会增加15，第一页start=0)
start = 0
while start < 10000:  # 以此来控制获取电影的数量
    # 字符串拼接来得到下一页的url
    request_url = base_url + str(start)
    # 下载数据，并返回是否有下一页(download方法会有返回值True、False)
    flag = download(request_url)
    if flag:
        start = start + 15
    else:
        break
# 存储电影名称和演员信息
dfData = {
        '电影名称' : title,
        '主演' : actor,
    }
fwrite = pd.DataFrame(dfData)
# 保存信息到Excel文件中
fwrite.to_excel("./吴镇宇.xlsx",index=False)
# 关闭selenium
driver.quit()