#-*- coding:utf-8 -*-

import io
import os
import sys
import numpy as np
from utils import *

reload(sys)
sys.setdefaultencoding('utf-8')


class Word2VecRespMatcher(object):
    """根据词向量计算相似度"""

    def vector2Dict(self, vectors_path):
        """将词向量转为字典"""
        with io.open(vectors_path, "r", encoding="utf-8") as read:
            vector_dic = {}
            for line in read:
                lines = line.strip().split()
                vector_dic[line[0]] = [float(i) for i in lines[1:]]
        return vector_dic

    def word2Vec(self, querys, responses, vector_dic):
        """用word2vec计算词向量"""
        v1 = [[0]*200]
        v2 = [[0]*200]
        for item in querys:
            if item in vector_dic:
                v1.append(vector_dic[item])
        for item in responses:
            if item in vector_dic:
                v2.append(vector_dic[item])
        vec1 = np.true_divide(np.sum(v1, axis=0), len(querys))
        vec2 = np.true_divide(np.sum(v2, axis=0), len(responses))
        return vec1, vec2

    def getResult(self, query, response, vector_dic):
        result = {}
        if not query or not response:
            return result
        for line in response:
            querys = query.strip().split()
            lines = line.strip().split()
            vec1, vec2 = self.word2Vec(querys, lines, vector_dic)
            vec = []
            vec.append(vec1.tolist())
            vec.append(vec2.tolist())
            vec_score = cosineSimilarity(vec)
            result[line] = float(vec_score)
        # # 对结果排序
        # result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        # 返回结果
        return result

    def q2rWord2VecScore(self, query_id, root_path):
        response_path = os.path.join(root_path, "data/lihang_weibo/response.index")
        candidate_path = os.path.join(root_path, "data/result/candidate_pairs")
        post_path = os.path.join(root_path, "data/lihang_weibo/post.index")
        vectors_path = os.path.join(root_path, "data/vec/tieba_nlpcc.vectors.txt")

        candidate_pairs = initDict(candidate_path)
        response, id2candidate, candidate2id = getCandidate(query_id, candidate_pairs, response_path)
        query = getQuery(query_id, post_path)
        vector_dic = self.vector2Dict(vectors_path)
        result = self.getResult(query, response, vector_dic)
        result_list = []
        for key, value in result.items():
            result_list.append((candidate2id[key], value))
        return result_list

if __name__ == "__main__":
    pwd = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(pwd)
    vec_q2r = Word2VecRespMatcher()
    query_id = 10270
    result_list = vec_q2r.q2rWord2VecScore(query_id, root_path)
    print result_list

