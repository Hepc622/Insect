import requests
import json
import codecs

from bs4 import BeautifulSoup

from com.hneb.insect.db import DB


class Insect:
    # 网站url
    __url = ''
    # 获取数据库操作对象
    __db = DB()
    # 记录那些是被爬过的网页
    __file = None

    def __init__(self):
        self.__url = "https://333av.vip"

    # 循环a标签，返回字典数组
    def get_arr(self, arr):
        arrs = []
        for tag in arr:  # 获取li下的所有a标签
            if tag.has_attr('href'):  # 如果该标签包含指定属性就返回True
                obj = {'title': '', 'url': ''}
                obj['url'] = tag.get("href")
                obj['title'] = tag.get('title')
                arrs.append(obj)
        return arrs

    # 获取指定url的body的html代码
    def get_html(self, url):
        res = requests.get(url)
        res.encoding = "utf-8"
        bts = BeautifulSoup(res.text, "html.parser")
        return bts.body

    # 获取不同类型的电影url
    def get_type_url(self, html):
        return self.get_arr(html.select('div[class="navmenu dy"] ul li a[href]'))

    # 判断下一页的url
    def get_page_url(self, html):
        a = html.select("#pages a[class=pagegbk]")
        for tag in a:
            if tag.has_attr('class') and tag.contents[0] == '下一页':
                return self.__url + tag.get('href')
        return ""

    # 组拼一个页面的数据
    def piece_page_data(self, arr, types):
        self.__file = codecs.open(filename="c://movie.txt", mode='a+', encoding='utf-8')
        sql = "insert into	movies VALUES (null,?,?,?,?,?)"
        for detail in arr:
            if self.is_read(detail['url']):
                detail_html = self.get_html(self.__url + detail['url'])
                link = detail_html.select('li[class=thunder] a')
                if len(link) > 0:
                    link = link[0]
                    m_type = types
                    m_name = detail['title']
                    m_img = detail_html.select('.pic img')[0]['src']
                    m_url = link.get('href')
                    m_role = ''
                    self.__db.insert(sql, m_type, m_name, m_url, m_img, m_role)
                    self.__file.write(detail['url'] + ",")
        # 关闭文件
        self.__file.close()

    # 获取电影的具体url
    def get_movie_url(self, html):
        return self.get_arr(html.select('ul[class=mlist] li a[class=p]'))

    # 查看记录中是否有当前的url
    def is_read(self, url):
        # 将游标移至第一行
        self.__file.seek(0)
        record = self.__file.read(-1)
        if record.find(url) != -1:
            return False
        else:
            return True

    # 主方法
    def main(self):
        # 获取首页html
        index = self.get_html(self.__url)
        #     获取电影页面的标题和url
        movie_index = self.get_type_url(index)

        for movie in movie_index:
            index = movie['url'].find("index.html")
            if index == -1:
                url = movie['url']
                while url != "":
                    movie_details=None
                    #   获取当类型页面的数据
                    if url.find("http") != -1:
                        movie_details = self.get_html(url)
                    else:
                        movie_details = self.get_html(self.__url + url)
                    #   返回
                    arr = self.get_movie_url(movie_details)
                    #     获取电影详细url
                    self.piece_page_data(arr, movie['title'])

                    #     判断该类型的是否有下一页，有的话继续循环
                    url = self.get_page_url(movie_details)
                    # 添加到当前的类型下面去


if __name__ == '__main__':
    Insect().main()
