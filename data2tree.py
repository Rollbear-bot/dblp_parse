# -*- coding: utf-8 -*-
# @Time: 2020/9/16 15:10
# @Author: Rollbear
# @Filename: data2tree.py

# import xml
import xml.sax
# from xml.sax import make_parser

# import xml.etree.ElementTree as ET

# c语言实现版本
import xml.etree.cElementTree as ET


def main():
    # 待解析的xml文件的存储路径
    xml_path = "../dblp-2020-09-01.xml"
    tmp_path = "./tmp.xml"

    with open(xml_path, "r") as rf:
        xml_str = rf.read()
        # 构造小数据集
        tmp = xml_str[:1000-167-14] + "</dblp>"

        with open(tmp_path, "w") as wf:
            wf.write(tmp)

    print("len of whole string", len(xml_str))
    print("len of mini dataset", len(tmp))

    # 直接从字符串解析
    root = ET.fromstring(tmp)

    # 查看解析内容
    for child in root:
        print(child.tag, child.attrib)
        for c in child:
            print(c.tag, c.attrib)

if __name__ == '__main__':
    main()
