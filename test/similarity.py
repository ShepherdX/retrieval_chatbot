import jieba
import jieba.analyse


def words2vec(words1=None, words2=None):
    v1 = []
    v2 = []
    tag1 = jieba.analyse.extract_tags(words1, withWeight=True, topK=20)
    tag2 = jieba.analyse.extract_tags(words2, withWeight=True, topK=20)
    # print("tag1", tag1)
    # print("tag2", tag2)
    tag_dict1 = {i[0]: i[1] for i in tag1}
    tag_dict2 = {i[0]: i[1] for i in tag2}
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
    # print("merg", merged_tag)
    # print(v1, v2)
    return v1, v2


def cosine_similarity(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        #return round(dot_product / ((normA ** 0.5) * (normB ** 0.5)) * 100, 2)
        return dot_product / ((normA ** 0.5) * (normB ** 0.5))


def cosine(str1, str2):
    vec1, vec2 = words2vec(str1, str2)
    return cosine_similarity(vec1, vec2)

if __name__ == "__main__":
    # print(cosine('老骨头3', '你以为你还年轻么3'))
    words = "嗯嗯老实在家呆着吧5"
    tag = jieba.analyse.extract_tags(words, withWeight=True, topK=20)
    print(tag)