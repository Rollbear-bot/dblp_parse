# -*- coding: utf-8 -*-
# @Time: 2020/9/22 18:02
# @Author: Rollbear
# @Filename: timeframe_split_by_year.py
# 按照时间片分割edgelist（每年一个时间片）

from tqdm import tqdm
import json
from functools import reduce  # 列表累加
import time
import datetime


def split_from_json(json_path, author_map_path, co_author_edgelist_path,
                    max_co_authors: int, abnormal_log_path,
                    skip_abnormal=True, with_timestamp=False,
                    segregating_str=" "):
    """
    从json解析得到edgelist
    :param skip_abnormal: 是否跳过年份为异常值的数据
    :param json_path: json数据文件路径
    :param author_map_path: 作者id映射表的输出路径
    :param co_author_edgelist_path: 时间片输出目录
    :param max_co_authors: 最大合著者限制（控制时间开销）
    :param abnormal_log_path: 异常数据信息输出路径
    :param with_timestamp: 是否生成带时间戳的时间片（tiles算法格式）
    :param segregating_str: edge中节点（或时间戳）的分隔字符，默认为空格
    :return: None
    """
    with open(json_path, "r") as rf:
        data = json.load(rf)
        # skip the empty files.
        if len(data) is 0:
            return

    time_cluster = {}  # 按照年份对文献分类，以便后续划分时间片

    author_map = {}
    author_count = 0  # 用于生成作者的id

    print("split data base on time...")
    for record in tqdm(data):
        # 按照时间划分文献
        # 注意year标签并不一定出现，此时考虑使用mdate字段的年份替代
        if "year" in record.keys():
            if record["year"] not in time_cluster.keys():
                # 识别年份为异常值的数据
                if skip_abnormal is False or len(record["year"]) == 4:
                    time_cluster[record["year"]] = [record]
            else:
                time_cluster[record["year"]].append(record)
        elif "mdate" in record.keys():
            # 使用mdate中的年份代替year字段
            m_date_year = str(record["mdate"]).split("-")[0]  # mdate中的年份
            if m_date_year not in time_cluster.keys():
                # 识别年份为异常的数据
                if skip_abnormal is False or len(m_date_year) == 4:
                    time_cluster[m_date_year] = [record]
            else:
                time_cluster[m_date_year].append(record)
        # 生成作者的id映射表
        for author in record["author"]:
            if author_map.get(author, -1) is -1:
                author_map[author] = author_count
                author_count += 1

    # 将作者名与id的映射关系储存到json
    with open(author_map_path, "w") as wf:
        json.dump(author_map, wf, indent=4)

    print("generating time frames...")

    years = sorted(list(time_cluster.keys()))  # 数据中的所有年份（或有效年份）
    if with_timestamp is True:
        # tiles算法格式的时间片只包含末位年份
        years = [years[-1]]

    for year in tqdm(years):
        # 处理time cluster为时间片
        # 某个时间点的时间片包含该时间以前的所有边
        cur_frame = reduce(
            lambda x, y: x + y,  # 列表拼接
            [time_cluster[y] for y in time_cluster.keys() if int(y) <= int(year)]
        )

        # 保存图的边（合著关系）
        with open(abnormal_log_path, "w") as ab_f:
            with open(co_author_edgelist_path + str(year) + ".edgelist", "w") as wf:
                for i, record in enumerate(tqdm(cur_frame)):

                    # 被注释的代码对合著关系生成星型状的边，已弃用
                    # 生成从一作到其他合著者的边，用空格作为两个节点的分隔符
                    # for co_author in record["author"][1:]:
                    #     edgelist.append(str(author_map[record["author"][0]]) +
                    #                     " " +
                    #                     str(author_map[co_author]) +
                    #                     "\n")

                    # 跳过合著者过高的记录，否则会导致时间开销过大
                    if len(record["author"]) > max_co_authors:
                        # 将合著者数量异常的记录信息输出到文件
                        ab_f.write(record["title"] + ";" + str(len(record["author"])) + "\n")
                        continue

                    # 对合著者生成完全子图
                    for author_index, cur_author in enumerate(record["author"]):
                        if author_index < len(record["author"]) - 1:  # 如果当前元素是列表的末位，就不用处理了
                            other_authors = record["author"][author_index + 1:]
                            for other_author_index, other_author in enumerate(other_authors):
                                # 边表直接写入文件，不保存在内存，防止爆内存
                                edge_str = str(author_map[cur_author]) + segregating_str + \
                                           str(author_map[other_author])

                                if with_timestamp is True:
                                    # 生成时间戳
                                    if "year" in record.keys():
                                        time_array = time.strptime(record["year"], "%Y")
                                    elif "mdate" in record.keys():
                                        time_array = time.strptime(record["mdate"], "%Y-%m-%d")
                                    time_stamp = time.mktime(time_array)
                                    edge_str += (segregating_str + str(time_stamp))

                                # 最后一行不加换行符
                                if not (i == len(cur_frame) - 1 and
                                        author_index == len(record["author"]) - 1 and
                                        other_author_index == len(other_authors) - 1):
                                    edge_str += "\n"
                                wf.write(edge_str)


if __name__ == '__main__':
    # 处理服务器上的数据
    # proceedings和masterthesis类别是空的，这里不再处理
    avail_types = ["phdthesis",
                   # "article",
                   # "inproceedings",
                   # "book",
                   # "incollection",
                   "www"]
    for t in avail_types:
        print(f"\n--------------{t}----------------")

        # working_dir = "./resource/co_author/"
        working_dir = "../datasets/frame_with_timestamp/"

        json_data_input_path = f"./resource/{t}_co_author_data.json"
        dataset_dump_path = working_dir + t + "/"
        author_map_dump_path = working_dir + t + f"/{t}_author_map.json"
        abnormal_log = working_dir + t + f"/{t}_abnormal_data_log.txt"

        # 生成时间片
        split_from_json(json_data_input_path,
                        author_map_dump_path,
                        dataset_dump_path,
                        max_co_authors=1000,
                        abnormal_log_path=abnormal_log,
                        skip_abnormal=True,
                        with_timestamp=True,
                        segregating_str="\t")
