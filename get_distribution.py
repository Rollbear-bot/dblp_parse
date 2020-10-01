# -*- coding: utf-8 -*-
# @Time: 2020/10/1 17:46
# @Author: Rollbear
# @Filename: get_distribution.py

import csv
import json
from tqdm import tqdm
import os


def get_degree_distribution(time_frame_path: str, csv_dump_path: str, segregate_str=" "):
    degree = {}  # 度分布（每节点）

    with open(time_frame_path, "r") as frame:
        for edge in frame:
            node_a, node_b = edge.rstrip().split(segregate_str)
            degree[node_a] = degree.get(node_a, 0) + 1
            degree[node_b] = degree.get(node_b, 0) + 1

    with open(csv_dump_path, "w", newline="") as csv_file:
        rows = [(key, value) for key, value in degree.items()]
        writer = csv.writer(csv_file)
        writer.writerow(("node_id", "degree"))
        writer.writerows(rows)


def get_num_coauthor_distribution(json_path: str, csv_dump_path: str):
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
        rows = [(record["key"], len(record["author"])) for record in data]
        with open(csv_dump_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(("key", "num_of_author"))  # headers
            writer.writerows(rows)


if __name__ == '__main__':
    avail_types = ["phdthesis",
                   "article",
                   "inproceedings",
                   "book",
                   "incollection",
                   "www"]
    for t in tqdm(avail_types):
        print(f"\n--------------{t}----------------")
        json_data_input_path = f"./resource/{t}_co_author_data.json"

        working_dir = "./resource/co_author/" + t + "/"
        degree_dis = working_dir + "degree_distribution.csv"
        num_coauthor_dis = working_dir + "num_coauthor_distribution.csv"

        edgelist_paths = []
        for path in os.listdir(working_dir):
            if path.endswith(".edgelist") and len(path.split(".edgelist")[0]) == 4:
                edgelist_paths.append(path)
        edgelist_paths.sort()
        last_frame_path = working_dir + edgelist_paths[-1]

        get_degree_distribution(time_frame_path=last_frame_path,
                                csv_dump_path=degree_dis,
                                segregate_str=" ")
        get_num_coauthor_distribution(json_path=json_data_input_path,
                                      csv_dump_path=num_coauthor_dis)
