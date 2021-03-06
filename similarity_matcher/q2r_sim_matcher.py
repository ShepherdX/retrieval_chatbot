#-*- coding:utf-8 -*-

import io
import os
import sys
import numpy as np
from utils import *
from sklearn.feature_extraction.text import CountVectorizer

reload(sys)
sys.setdefaultencoding('utf-8')


class ResponseTfIdfMatcher(object):
    """基于query和response的TfIdf的相似度计算"""
    def getResult(self, query, response, root_path):
        result = {}
        if not query or not response:
            return result

        for line in response:
            query_dict = dict(Counter(query.split()))
            response_dict = dict(Counter(line.split()))
            # 02、词频矩阵和关键词
            word_tf, words = words2Vec(query_dict, response_dict)
            # 03、关键词矩阵
            word_idf = np.array(getTfIdf(words, root_path))
            # 04、TFIDF 矩阵
            tfidf_vec = np.multiply(word_tf, word_idf)
            # 05、获取相似度
            value = cosineSimilarity(tfidf_vec)
            # 06、相似度大于一定的阈值才有效
            # if value >= 0.0:
            result[line] = float(value)
        # # 对结果排序
        # result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return result

    def q2rTfIdfScore(self, query_id, root_path):
        post_path = os.path.join(root_path, "data/lihang_weibo/post.index")
        response_path = os.path.join(root_path, "data/lihang_weibo/response.index")
        candidate_path = os.path.join(os.path.join(root_path, "data/result/candidate_pairs"))
        # 候选集
        candidate_pairs = initDict(candidate_path)
        response, id2candidate, candidate2id = getCandidate(query_id, candidate_pairs, response_path)
        query = getQuery(query_id, post_path)
        result = self.getResult(query, response, root_path)
        result_list = []
        for key, value in result.items():
            result_list.append((candidate2id[key], value))
        return result_list
