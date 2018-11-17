#-*- coding:utf-8 -*-

import io
import os
import sys
from similarity_matcher.sim_matcher import SimMatcher

reload(sys)
sys.setdefaultencoding('utf-8')

def read_query():
    while True:
        query = input("请输入问题：").strip()
        yield query

def getQuery(query_path):
    query_list = []
    with io.open(query_path, "r", encoding="utf-8") as f:
        for line in f:
            query_list.append(int(line))
    return query_list

def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    query_path = os.path.join(root_path, "data/result/query_list")
    predict_path = os.path.join(root_path, "data/result/predict")
    query_list = getQuery(query_path)
    SM = SimMatcher()
    SM.similarityMatcher(query_list, predict_path, root_path)

if __name__ == "__main__":
    main()


"""
netease-cloud-music
"""