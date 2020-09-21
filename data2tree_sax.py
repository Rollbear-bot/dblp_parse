# -*- coding: utf-8 -*-
# @Time: 2020/9/17 16:07
# @Author: Rollbear
# @Filename: data2tree_sax.py

from xml import sax
import json

from tqdm import tqdm

# 全局变量
DATA_LT = []
CUR_COUNT = 0  # 当前种类文献计数器
TOTAL_COUNT = 0  # 所有文献的计数器
THESIS_TYPE = None  # 当前解析的文献种类


class TestHandler(sax.ContentHandler):
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self._content = ""
        self._tag = ""

        # 共同作者计数器
        self.author_count = 0

        # 使用一个dict来存储一个meta data
        self.cluster = {}

    def startElement(self, name, attrs):
        """
        # 遇到<tag>标签时候会执行的方法，
        这里的name，attrs不用自己传值的（这里其实是重写）
        :param name:
        :param attrs:
        :return:
        """
        self._tag = name
        if name == THESIS_TYPE:
            # if name == "phdthesis":
            # 初始化作者计数器
            self.author_count = 0
            # 初始化存储字典
            self.cluster = {}

            # mdate和key是meta-tag
            mdate = attrs["mdate"] if "mdate" in attrs else None
            key = attrs["key"] if "key" in attrs else None

            self.cluster["mdate"] = mdate
            self.cluster["key"] = key

            global CUR_COUNT
            CUR_COUNT += 1  # 计数器自加

        if name == "phdthesis" or \
                "article" or \
                "inproceedings" or \
                "proceedings" or \
                "book" or \
                "incollection" or \
                "mastersthesis" or \
                "www":
            global TOTAL_COUNT
            TOTAL_COUNT += 1  # 全局计数器自加

    def endElement(self, name):
        """
        # 遇到</tag>执行的方法，name不用自己传值（重写）
        :param name:
        :return:
        """
        if name == "dblp":
            print("=========dblp=========")

        elif name == THESIS_TYPE:  # thesis end: collecting end
            if "author" in self.cluster and \
                    len(self.cluster["author"]) >= 2:
                # 仅当文献作者大于一个才储存该样本（研究合著关系图）
                global DATA_LT  # 使用全局变量声明
                DATA_LT.append(self.cluster)

        elif name == "author":
            self.author_count += 1  # 计数器自加
            # author可能有多个
            if "author" in self.cluster:
                self.cluster["author"].append(self._content)
            else:
                self.cluster["author"] = [self._content]
        elif name == "title":
            self.cluster["title"] = self._content
        elif name == "year":
            self.cluster["year"] = self._content
        elif name == "school":
            self.cluster["school"] = self._content

        # --------------------------------
        # 先考虑与共同作者有关的字段，忽略其他信息

        # elif name == "pages":
        #     print("pages: " + self._content)
        # elif name == "isbn":
        #     print("isbn: " + self._content)
        # elif name == "ee":
        #     print("ee: " + self._content)
        else:
            pass

    def characters(self, content):  # 获取标签内容
        self._content = content


def data2json(json_dump_path, obj):
    """将解析得到数据转化为json文件"""
    with open(json_dump_path, "w") as wf:
        json.dump(obj, wf, indent=4)


def process(file_path: str):
    handler = TestHandler()  # 自定义类实例化成对象
    sax.parse(file_path, handler)  # 解析xml文件

    print("该类别文献记录数：", CUR_COUNT)
    print("所有文献记录数：", TOTAL_COUNT)

    # 生成json存储路径
    json_dump_path = f"./resource/{THESIS_TYPE}_co_author_data.json"
    data2json(json_dump_path, DATA_LT)


def main():
    test_file_path = "../dblp-2020-09-01.xml"

    thesis_types = ["phdthesis",
                    "article",
                    "inproceedings",
                    "proceedings",
                    "book",
                    "incollection",
                    "mastersthesis",
                    "www"]
    for t in tqdm(thesis_types):
        global THESIS_TYPE, DATA_LT, CUR_COUNT, TOTAL_COUNT  # 绑定到全局变量
        THESIS_TYPE = t  # 设置本轮迭代的文献类型

        process(test_file_path)  # 按照设置的类别解析数据

        # 重新初始化变量
        DATA_LT = []  # 每轮迭代后，清空数据表中的数据
        THESIS_TYPE = None
        CUR_COUNT = 0
        TOTAL_COUNT = 0

    # json_dump_path = "./resource/co_author_data_total.json"
    #
    # handler = TestHandler()  # 自定义类实例化成对象
    # sax.parse(test_file_path, handler)  # 解析xml文件
    #
    # print("phd文献记录数：", PHD_COUNT)
    # print("所有文献记录数：", TOTAL_COUNT)
    #
    # data2json(json_dump_path, DATA_LT)


if __name__ == '__main__':
    main()
