# -*- coding: utf-8 -*-
# @Time: 2020/9/21 12:06
# @Author: Rollbear
# @Filename: data_analysis.py

import os
import csv
from tqdm import tqdm


def _dataset_description(e_lt_path: str):
    """
    获取某个时间片的统计信息
    :param e_lt_path: 时间片的文件路径
    :return: 二元组，(节点数, 边数)
    """
    with open(e_lt_path) as rf:
        data = [row.rstrip().split(" ") for row in rf.readlines()]
        num_of_edges = len(data)
        nodes = set(node for edge in data for node in edge)
        num_of_nodes = len(nodes)

    return num_of_nodes, num_of_edges


def dataset_description(working_dir: str, skip_abnormal_edgelist=True):
    """
    获取一个数据集（含若干时间片）的描述性信息
    :param working_dir: 数据集目录，末尾应带上"/"
    :param skip_abnormal_edgelist: 是否舍弃年份不为四位数的异常数据
    :return: list of tuple(year, num of nodes, num of edges)
    """
    data_info = []

    for path in os.listdir(working_dir):
        if path.endswith(".edgelist"):
            if skip_abnormal_edgelist and len(path.split(".")[0]) == 4:
                # 跳过异常数据的情况
                num_n, num_e = _dataset_description(working_dir + path)
                data_info.append((path.split(".")[0], num_n, num_e))
            else:
                num_n, num_e = _dataset_description(working_dir + path)
                data_info.append((path.split(".")[0], num_n, num_e))

    data_info.sort(key=lambda item: int(item[0]))
    return data_info


if __name__ == '__main__':
    avail_types = ["phdthesis",
                   "article",
                   "inproceedings",
                   "book",
                   "incollection",
                   "www"]
    for t in tqdm(avail_types):
        wd = "./resource/co_author/" + t + "/"
        # 不跳过异常数据
        info = dataset_description(wd, skip_abnormal_edgelist=False)

        # 将描述性数据写入数据集目录
        with open(wd + "dataset_description.csv", "w", newline="") as wf:
            writer = csv.writer(wf)
            writer.writerow(("YEAR", "NODES", "EDGES"))
            writer.writerows(info)
