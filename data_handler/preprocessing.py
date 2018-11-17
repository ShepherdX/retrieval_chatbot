#-*- coding:utf-8 -*-

import io
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Preprocessing(object):
    """预处理文件"""
    def __init__(self, root_path):
        self.root_path = root_path

    # 论文数据预处理
    def paperDataInit(self):
        # 候选集
        candidate_dic = {}
        # 标准结果
        standard_dic = {}
        data_path = os.path.join(self.root_path, "data/lihang_weibo/labeled.pair")
        query_list = os.path.join(self.root_path, "data/result/query_list")
        candidate_pairs = os.path.join(self.root_path, "data/result/candidate_pairs")
        standard_pairs = os.path.join(self.root_path, "data/result/standard_pairs")
        with io.open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line:
                    continue
                lines = line.strip().split(",")
                # 候选集
                if int(lines[1]) in candidate_dic:
                    candidate_dic[int(lines[1])].append(str(lines[1]) + ":" + str(lines[2]))
                else:
                    candidate_dic[int(lines[1])] = [str(lines[1]) + ":" + str(lines[2])]
                # 标准集
                if int(lines[0]) == 2:
                    if int(lines[1]) in standard_dic:
                        standard_dic[int(lines[1])].append(int(lines[2]))
                    else:
                        standard_dic[int(lines[1])] = [int(lines[2])]
        # 写文件
        with io.open(candidate_pairs, "w", encoding="utf-8") as can_w:
            can_w.write(str(candidate_dic).decode("utf-8"))
        with io.open(standard_pairs, "w", encoding="utf-8") as stand_w:
            stand_w.write(str(standard_dic).decode("utf-8"))
        with io.open(query_list, "w", encoding="utf-8") as que_w:
            for query_id in standard_dic.keys():
                que_w.write(str(query_id).decode("utf-8") + "\n")
        # 打印标准集的个数
        print "query的个数：", len(standard_dic.keys())

if __name__ == "__main__":
    pwd = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(pwd)
    prep = Preprocessing(root_path)
    prep.paperDataInit()
    pass


