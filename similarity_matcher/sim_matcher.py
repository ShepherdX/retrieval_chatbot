#-*- coding:utf-8 -*-

import io
import sys
from w2v_q2r_matcher import Word2VecRespMatcher
from q2p_sim_matcher import PostTfIdfMatcher
from q2r_sim_matcher import ResponseTfIdfMatcher

reload(sys)
sys.setdefaultencoding('utf-8')

class SimMatcher(object):
    """相似度计算"""

    def merge2Dict(self, dic, lis, weight):
        """将列表乘上权重后合并到字典中"""
        for item in lis:
            if item[0] in dic:
                dic[item[0]] += float(item[1])*weight
            else:
                dic[item[0]] = float(item[1])*weight
        return dic

    def similarityMatcher(self, query_list, predict_path, root_path, flag=None):
        VecQ2R = Word2VecRespMatcher()
        Q2P = PostTfIdfMatcher()
        Q2R = ResponseTfIdfMatcher()
        """计算相似度"""
        weight_post_tfidf = 0.6
        weight_response_tfidf = 0.1
        weight_response_w2v = 0.3
        predict = {}
        for i, query_id in enumerate(query_list):
            print("Running the %d sentences! " % (i + 1))
            if flag == 1:
                result_list = Q2R.q2rTfIdfScore(query_id, root_path)
            elif flag == 2:
                result_list = Q2P.q2pTfIdfScore(query_id, root_path)
            elif flag == 3:
                result_list = VecQ2R.q2rWord2VecScore(query_id, root_path)
            else:
                # 返回结果 result_list：列表形式，列表中存储的元组（response_id, 相似度值）
                q2r_res = Q2R.q2rTfIdfScore(query_id, root_path)
                q2p_res = Q2P.q2pTfIdfScore(query_id, root_path)
                vec_q2r_res = VecQ2R.q2rWord2VecScore(query_id, root_path)
                dic = {}
                dic = self.merge2Dict(dic, q2r_res, weight_response_tfidf)
                dic = self.merge2Dict(dic, q2p_res, weight_post_tfidf)
                dic = self.merge2Dict(dic, vec_q2r_res, weight_response_w2v)
                # 对结果排序
                result_list = sorted(dic.items(), key=lambda x: x[1], reverse=True)

            length = 30
            if len(result_list) >= length:
                predict[query_id] = result_list[:length]
            else:
                predict[query_id] = result_list
            if i >= 20:
                break

        with io.open(predict_path, "w", encoding="utf-8") as w:
            w.write(str(predict).decode("utf-8"))

