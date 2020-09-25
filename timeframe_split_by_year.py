# -*- coding: utf-8 -*-
# @Time: 2020/9/22 18:02
# @Author: Rollbear
# @Filename: timeframe_split_by_year.py
# 按照时间片分割edgelist（每年一个时间片）

from tqdm import tqdm
import json

from functools import reduce  # 列表累加


def split_from_json(json_path, author_map_path, co_author_edgelist_path, skip_abnormal=True):
    """
    从json解析得到edgelist
    :param skip_abnormal: 是否跳过年份为异常值的数据
    :param json_path: json数据文件路径
    :param author_map_path: 作者id映射表的输出路径
    :param co_author_edgelist_path: 时间片输出目录
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

    # 处理time cluster为时间片
    # todo::性能优化
    time_frame = {}

    print("generating time frames...")
    for year in tqdm(time_cluster.keys()):
        # 某个时间点的时间片包含该时间以前的所有边
        time_frame[year] = reduce(
            lambda x, y: x + y,  # 列表拼接
            [time_cluster[y] for y in time_cluster.keys() if int(y) <= int(year)]
        )

    # 保存图的边（合著关系）
    print("generating edges...")
    for record_index, record_item in enumerate(time_frame.items()):
        print(f"{record_index}/{len(time_frame)}")
        edgelist = []
        with open(co_author_edgelist_path + str(record_item[0]) + ".edgelist", "w") as wf:
            for record in tqdm(record_item[1]):
                # 生成从一作到其他合著者的边，用空格作为两个节点的分隔符
                # for co_author in record["author"][1:]:
                #     edgelist.append(str(author_map[record["author"][0]]) +
                #                     " " +
                #                     str(author_map[co_author]) +
                #                     "\n")

                # 对合著者生成完全子图
                for author_index, cur_author in enumerate(record["author"]):
                    if author_index < len(record["author"])-1:  # 如果当前元素是列表的末位，就不用处理了
                        other_authors = record["author"][author_index+1:]
                        for other_author in other_authors:
                            edgelist.append(str(author_map[cur_author]) +
                                            " " +
                                            str(author_map[other_author]) +
                                            "\n")

            # 去掉最后一行末尾的换行符
            edgelist[-1] = edgelist[-1].rstrip()
            wf.writelines(edgelist)


if __name__ == '__main__':
    # 处理服务器上的数据
    working_dir = "./resource/co_author/"
    # proceedings和masterthesis类别是空的，这里不再处理
    avail_types = ["phdthesis",
                   # "article",
                   # "inproceedings",
                   "book",
                   "incollection",
                   "www"]
    for t in avail_types:
        print(f"--------------{t}----------------")
        json_data_input_path = f"./resource/{t}_co_author_data.json"
        dataset_dump_path = working_dir + t + "/"
        author_map_dump_path = working_dir + t + f"/{t}_author_map.json"
        # 生成时间片
        split_from_json(json_data_input_path,
                        author_map_dump_path,
                        dataset_dump_path)
