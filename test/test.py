#-*- coding:utf-8 -*-

import os
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


pwd = os.path.dirname(os.path.abspath(__file__))
father_path = os.path.dirname(pwd)
data_path = os.path.join(father_path, "data/lihang_weibo")
vec_path = os.path.join(father_path, "data/vec")
newdata_path = os.path.join(father_path, "data/result")

reload(sys)
sys.setdefaultencoding('utf-8')

def get_result(query, response):
    result = {}
    if not query or not response:
        return result
    print "query: ", query
    print "response: ", response[0]

    for line in response:
        corpus = []
        corpus.append(query.decode("utf-8"))
        corpus.append(line.decode("utf-8"))

        # 01、构建词频矩阵，将文本中的词语转换成词频矩阵
        vectorizer = CountVectorizer(min_df=0, max_df=1.0)
        # 02、词频矩阵
        word_tf = vectorizer.fit_transform(corpus).toarray()
        # 03、获取词袋模型中的关键词
        words = vectorizer.get_feature_names()
        print words
        for w in words:
            print w.encode("utf-8")
        # 03、关键词矩阵
        word_idf = np.array(get_tfidf(words))
        # 04、TFIDF 矩阵
        tfidf_vec = np.multiply(word_tf, word_idf)
        # 05、获取相似度
        value = cosine_similarity(tfidf_vec)
        # 06、相似度大于一定的阈值才有效
        if value > 0:
            result[line] = float(value)
    # 对结果排序
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    for item in result:
        print item[0].encode("utf-8"), item[1]
    return result

if __name__ == "__main__":
    global ridf_dict, pidf_dict, candidate_pairs
    pidf_dict = get_idf(os.path.join(vec_path, "tieba_nlpcc.idf.query"))
    ridf_dict = get_idf(os.path.join(vec_path, "tieba_nlpcc.idf.response"))
    query = "祝 各位 朋友 2012 年 万事如意 ！"
    response = ["祝 各位 朋友 2012 年 十 有 七八 事 如意 ！ 看 我 数学 文化 学得 好 吧 …"]
    get_result(query, response)

