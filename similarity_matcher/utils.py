#-*- coding:utf-8 -*-

import io
import os
import sys
import numpy as np
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')

def readFile(file_path):
    """读文件"""
    result = ""
    try:
        with io.open(file_path, "r", encoding="utf-8") as f:
            result = f.read()
    except Exception as e:
        print "读取文件异常！"
    return result

def initDict(path):
    """读文件转为字典"""
    result = readFile(path)
    if result:
        return eval(result)
    else:
        return {}

def words2Vec(tag_dict1=None, tag_dict2=None):
    """将字典转为词向量矩阵"""
    word_tf = []
    v1 = []
    v2 = []
    merged_tag = set(tag_dict1.keys()) | set(tag_dict2.keys())
    for i in merged_tag:
        if i in tag_dict1:
            v1.append(tag_dict1[i])
        else:
            v1.append(0)
        if i in tag_dict2:
            v2.append(tag_dict2[i])
        else:
            v2.append(0)
    word_tf.append(v1)
    word_tf.append(v2)
    return np.array(word_tf), list(merged_tag)

def cosineSimilarity(tfidf_vec):
    """计算两个向量之间的余弦相似度"""
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(tfidf_vec[0], tfidf_vec[1]):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        #return round(dot_product / ((normA ** 0.5) * (normB ** 0.5)) * 100, 2)
        return dot_product / ((normA ** 0.5) * (normB ** 0.5))

def getIdf(idf_path):
    """将idf文件读到字典中"""
    dic = {}
    with io.open(idf_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line:
                continue
            lines = line.strip().split("\t")
            if len(lines) == 2:
                dic[lines[0]] = float(lines[1])
            else:
                continue
    return dic

def getQuery(query_id, post_path):
    query = ""
    with io.open(post_path, "r", encoding="utf-8") as query_r:
        for line in query_r:
            temps = line.strip().split("##")
            if int(temps[0]) == query_id:
                query = temps[1]
    return query

def getCandidate(query_id, candidate_pairs, response_path):
    """读取候选项"""
    response = []
    id2candidate = {}
    candidate2id = {}
    candidate_ids = []
    for item in candidate_pairs[query_id]:
        candidate_ids.append(int(item.split(":")[1]))
    with io.open(response_path, "r", encoding="utf-8") as resp_r:
        for line in resp_r:
            temps = line.strip().split("##")
            if int(temps[0]) in candidate_ids:
                response.append(temps[1])
                id2candidate[int(temps[0])] = temps[1]
                if temps[1] not in candidate2id:
                    candidate2id[temps[1]] = int(temps[0])
    return response, id2candidate, candidate2id

def getTfIdf(words, root_data):
    """获取query和response的idf矩阵"""
    pidf_path = os.path.join(root_data, "data/vec/tieba_nlpcc.idf.query")
    ridf_path = os.path.join(root_data, "data/vec/tieba_nlpcc.idf.response")
    # post的idf值
    pidf_dict = getIdf(pidf_path)
    # response的idf值
    ridf_dict = getIdf(ridf_path)

    word_idf = []
    word_len = len(words)
    if word_len <= 0:
        return word_idf
    post_idf = []
    response_idf = []
    for item in words:
        try:
            post_idf.append(float(pidf_dict[item]))
        except:
            post_idf.append(float(1))
    for item in words:
        try:
            response_idf.append(float(ridf_dict[item]))
        except:
            response_idf.append(float(1))
    word_idf.append(post_idf)
    word_idf.append(response_idf)
    return word_idf


# def get_result(query, post):
#     result = {}
#     if not query or not post:
#         return result
#     for line in post:
#         corpus = []
#         corpus.append(query)
#         corpus.append(line)
#         # 01、构建词频矩阵，将文本中的词语转换成词频矩阵
#         vectorizer = CountVectorizer(min_df=1, max_df=1.0)
#         # 02、词频矩阵
#         word_tf = vectorizer.fit_transform(corpus).toarray()
#         # 03、获取词袋模型中的关键词
#         words = vectorizer.get_feature_names()
#         # 03、关键词矩阵
#         word_idf = np.array(get_tfidf(words))
#         # 04、TFIDF 矩阵
#         tfidf_vec = np.multiply(word_tf, word_idf)
#         # 05、获取相似度
#         value = cosine(tfidf_vec)
#         # 06、相似度大于一定的阈值才有效
#         if value >= 0.05:
#             result[line] = float(value)
#     # 对结果排序
#     result = sorted(result.items(), key=lambda x: x[1], reverse=True)
#     return result

if __name__ == "__main__":
    post = "祝 各位 2012 年 万事如意 ！ 万事如意 年"
    response = "祝 各位 朋友 2012 年 h"
    tag1 = dict(Counter(post.split()))
    tag2 = dict(Counter(response.split()))
    # for key,value in tag2.items():
    #     print key,value
    v1, v2 = words2Vec(tag1, tag2)
    words = list(set(tag1))
    print words