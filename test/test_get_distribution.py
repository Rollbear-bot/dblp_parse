# -*- coding: utf-8 -*-
# @Time: 2020/10/1 23:58
# @Author: Rollbear
# @Filename: test_get_distribution.py

from unittest import TestCase
import unittest

from get_distribution import get_degree_distribution
from get_distribution import get_num_coauthor_distribution

import os


class TestGetDistribution(TestCase):
    def test_get_degree_distribution(self):
        """测试度分布的统计"""
        get_degree_distribution(time_frame_path="./test_res/test_split/2020.edgelist",
                                csv_dump_path="./test_res/test_degree_distribution.csv",
                                segregate_str=" ")

    def test_get_num_coauthor_distribution(self):
        get_num_coauthor_distribution(json_path="./test_res/www_co_author_data.json",
                                      csv_dump_path="./test_res/test_num_coauthor_distribution.csv")

    def test_find_last_frame(self):

        working_dir = "./test_res/test_split/"
        edgelist_paths = []
        for path in os.listdir(working_dir):
            if path.endswith(".edgelist") and len(path.split(".edgelist")[0]) == 4:
                edgelist_paths.append(path)
        edgelist_paths.sort()
        last_frame_path = working_dir + edgelist_paths[-1]
        assert last_frame_path == working_dir + "2020.edgelist"


if __name__ == '__main__':
    unittest.main()
