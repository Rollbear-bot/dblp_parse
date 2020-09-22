# -*- coding: utf-8 -*-
# @Time: 2020/9/18 7:44
# @Author: Rollbear
# @Filename: parse_json.py

import json
import csv
import pandas as pd
from tqdm import tqdm


def parse_json(json_path, author_map_path, co_author_edgelist_path):
    # json_path = "resource/co_author/phdthesis/co_author_data.json"
    # author_map_path = "resource/co_author/phdthesis/author_map.json"
    # co_author_edgelist_path = "resource/co_author/phdthesis/co_author.edgelist"

    with open(json_path, "r") as rf:
        data = json.load(rf)
       
       # skip the empty files.
        if len(data) is 0:
            return

    author_map = {}
    author_count = 0
    for record in data:
        for author in record["author"]:
            if author_map.get(author, -1) is -1:
                author_map[author] = author_count
                author_count += 1
            else:
                pass

    # 将作者名与id的映射关系储存到json
    with open(author_map_path, "w") as wf:
        json.dump(author_map, wf, indent=4)

    # 保存图的边（合著关系）
    edgelist = []
    with open(co_author_edgelist_path, "w") as wf:
        for record in data:
            # 生成从一作到其他合著者的边
            for co_author in record["author"][1:]:
                edgelist.append(str(author_map[record["author"][0]]) +
                                ", " +
                                str(author_map[co_author]) +
                                "\n")
        # 去掉最后一行末尾的换行符
        edgelist[-1] = edgelist[-1].rstrip()
        wf.writelines(edgelist)


if __name__ == '__main__':
    working_dir = "./resource/co_author/"

    types = ["phdthesis",
             "article",
             "inproceedings",
             "proceedings",
             "book",
             "incollection",
             "mastersthesis",
             "www"]
    for t in tqdm(types):
        json_path = f"./resource/{t}_co_author_data.json"
        author_map_path = working_dir + t + f"/{t}_author_map.json"
        co_author_edgelist_path = working_dir + t + f"/{t}_co_author.edgelist"
        parse_json(json_path, author_map_path, co_author_edgelist_path)
