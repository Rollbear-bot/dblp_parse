# -*- coding: utf-8 -*-
# @Time: 2020/9/23 14:31
# @Author: Rollbear
# @Filename: test_timeframe_split.py

from functools import reduce  # 累加函数
import unittest  # 单元测试模块
import json

from timeframe_split_by_year import split_from_json


class TestSplit(unittest.TestCase):
    def test_split(self):
        time_cluster = {}
        time_frame = {}

        # test data
        data_path = "test_res/www_co_author_data.json"
        with open(data_path, "r") as rf:
            data = json.load(rf)

        for record in data:
            # 按照时间划分文献
            # 注意year标签并不一定出现，此时考虑使用mdate字段的年份替代
            if "year" in record.keys():
                if record["year"] not in time_cluster.keys():
                    time_cluster[record["year"]] = [record]
                else:
                    time_cluster[record["year"]].append(record)
            elif "mdate" in record.keys():
                # 使用mdate中的年份代替year字段
                m_date_year = str(record["mdate"]).split("-")[0]  # mdate中的年份
                if m_date_year not in time_cluster.keys():
                    time_cluster[m_date_year] = [record]
                else:
                    time_cluster[m_date_year].append(record)

        for year in time_cluster.keys():
            # 某个时间点的时间片包含该时间以前的所有边
            time_frame[year] = reduce(
                lambda x, y: x + y,  # 列表拼接
                [time_cluster[y] for y in time_cluster.keys() if int(y) <= int(year)]
            )

        assert True

    def test_split_www(self):
        json_path = "./test_res/www_co_author_data.json"
        author_map_path = "./test_res/test_split/author_map.json"
        co_author_edgelist_path = "./test_res/test_split/"
        abnormal_log = "./test_res/test_split/abnormal_log.txt"
        split_from_json(json_path, author_map_path, co_author_edgelist_path, 1000, abnormal_log)

        # 检验生成的edgelist的准确性
        working_dir = "./test_res/test_split/"
        # 检测四个样本edgelist的长度
        with open(working_dir + "1998.edgelist") as e_lt_1998:
            # print(len(e_lt_1998.readlines()))
            assert len(e_lt_1998.readlines()) == 10  # 合著关系为完全子图时的边数
        with open(working_dir + "1999.edgelist") as e_lt_1999:
            # print(len(e_lt_1999.readlines()))
            assert len(e_lt_1999.readlines()) == 13
        with open(working_dir + "2019.edgelist") as e_lt_2019:
            # print(len(e_lt_2019.readlines()))
            assert len(e_lt_2019.readlines()) == 55568
        with open(working_dir + "2020.edgelist") as e_lt_2020:
            # print(len(e_lt_2020.readlines()))
            assert len(e_lt_2020.readlines()) == 70627

    # 本地机器上无法运行这个测试单元
    # def test_split_incollection(self):
    #     json_path = "./test_res/incollection_co_author_data.json"
    #     author_map_path = "./test_res/test_split_incollection/author_map.json"
    #     co_author_edgelist_path = "./test_res/test_split_incollection/"
    #     split_from_json(json_path, author_map_path, co_author_edgelist_path)

    # 谨慎运行这个测试单元
    def test_split_article(self):
        json_path = "./test_res/article_co_author_data.json"
        author_map_path = "./test_res/test_split_article/author_map.json"
        co_author_edgelist_path = "./test_res/test_split_article/"
        split_from_json(json_path, author_map_path, co_author_edgelist_path)


if __name__ == '__main__':
    unittest.main()
