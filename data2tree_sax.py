# -*- coding: utf-8 -*-
# @Time: 2020/9/17 16:07
# @Author: Rollbear
# @Filename: data2tree_sax.py

from xml import sax


class TestHandler(sax.ContentHandler):
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self._content = ""
        self._tag = ""

        #         self.phdthesis = ""
        #         self.author = ""
        #         self.title = ""
        #         self.year = ""
        #         self.school = ""
        #         self.pages = ""
        #         self.isbn = ""
        #         self.ee = ""

    def startElement(self, name, attrs):
        """
        # 遇到<tag>标签时候会执行的方法，这里的name，attrs不用自己传值的（这里其实是重写）
        :param name:
        :param attrs:
        :return:
        """
        self._tag = name
        if name == "dblp":
            print("=========dblp=========")
        # if self._tag == "book":
        #     print("BOOK: " + attrs["category"])
        #     print("--------------------------")

    def endElement(self, name):
        """
        # 遇到</tag>执行的方法，name不用自己传值（重写）
        :param name:
        :return:
        """
        if name == "dblp":
            print("=========dblp=========")
        elif name == "phdthesis":
            print("phdthesis: " + self._content)
        elif name == "author":
            print("author: " + self._content)
        elif name == "title":
            print("title: " + self._content)
        elif name == "year":
            print("year: " + self._content)
        elif name == "school":
            print("school: " + self._content)
        elif name == "pages":
            print("pages: " + self._content)
        elif name == "isbn":
            print("isbn: " + self._content)
        elif name == "ee":
            print("ee: " + self._content)
        else:
            pass

    def characters(self, content):  # 获取标签内容
        self._content = content


def main():
    test_file_path = "./resource/test2.xml"

    handler = TestHandler()  # 自定义类实例化成对象
    sax.parse(test_file_path, handler)  # 解析xml文件


if __name__ == '__main__':
    main()
