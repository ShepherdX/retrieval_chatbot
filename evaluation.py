#-*- coding:utf-8 -*-

import io
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class EvaluationTool(object):
    """评测工具"""
    def __init__(self, root_path):
        self.root_path = root_path

    def getDict(self, path):
        with io.open(path, "r", encoding="utf-8") as f:
            dic = eval(f.read())
        return dic

    # 计算平均均值准确率
    def claMap(self, standard, predict):
        # standard 标准答案的集合， predict 预测答案的集合
        # 形式： {query_id:[候选列表]}
        # 返回相关文档个数
        average_precision = 0
        # 遍历标准结果
        for key in standard.keys():
            precision = 0
            index = 0
            found = 0
            # 遍历预测结果
            if key not in predict.keys():
                continue
            for doc in predict[key]:
                doc = int(doc[0])
                index += 1
                # 检查是否匹配
                if doc in standard[key]:
                    found += 1
                precision += float(found) / index
            if len(predict[key]) == 0:
                continue
            average_precision += float(precision)/len(predict[key])
        map1 = float(average_precision)/len(standard.keys())
        return map1

    # 计算P@1值
    def calP1(self, standard, predict):
        count = 0
        # 遍历标准结果
        for key in standard.keys():
            # 检查是否匹配
            if key not in predict.keys() or len(predict[key]) == 0:
                continue
            if predict[key][0][0] in standard[key]:
                count += 1
        p1 = float(float(count)/len(standard.keys()))
        return p1

    # 评测工具
    def evalTool(self):
        standard_path = os.path.join(root_path, "data/result/standard_pairs")
        predict_dir = os.path.join(root_path, "data/result/predict")
        # 标准答案
        standard = self.getDict(standard_path)
        # 预测结果
        predict = self.getDict(predict_dir)

        # 评测结果
        map1 = self.claMap(standard, predict)
        p1 = self.calP1(standard, predict)
        # 打印结果
        print "****************************"
        print("map: ", map1)
        print("p@1: ", p1)
        print "*****************************"

if __name__ == "__main__":
    root_path = os.path.dirname(os.path.abspath(__file__))
    eval_tool = EvaluationTool(root_path)
    eval_tool.evalTool()


