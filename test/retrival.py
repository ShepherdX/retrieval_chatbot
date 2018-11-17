import codecs
import jieba
import jieba.analyse

def words2vec(tag1=None, tag_dict2=None,):
    v1 = []
    v2 = []
    tag_dict1 = {i[0]: i[1] for i in tag1}
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

# # 获取post中关键词的TFIDF值
# def getTFIDF(input_dir, output_dir):
#     with open(output_dir, "w", encoding="utf-8") as w:
#         with open(input_dir, "r", encoding="utf-8") as f:
#             for line in f:
#                 lines = line.strip().split()
#                 tag = jieba.analyse.extract_tags(lines[0], withWeight=True, topK=20)
#                 tag_dict = {i[0]: i[1] for i in tag}
#                 w.write(str(tag_dict) + "\t" + line)

def readQuery():
    while True:
        query = input("问：").strip()
        yield query

def retrival(query):
    dic = {}
    tag1 = jieba.analyse.extract_tags(query, withWeight=True, topK=20)
    with codecs.open("data/trainData.txt", "r", "utf-8") as f:
        for line in f:
            if not line:
                continue
            lines = line.strip().split("\t")
            if lines[0].strip() == "{}":
                continue
            #print(lines[0].strip())
            #print(type(lines[0].strip()))
            tag2 = eval(lines[0].strip())
            value = cosine(tag1, tag2)
            if value > 0:
                # print("检索结果：", line, value)
                # dic[" ".join(line.split()[1:])] = float(value)
                dic[lines[1].strip()] = float(value)
    print(dic)
    return dic

def main():
    for query in readQuery():
        print(query)
        dic = retrival(query)
        new_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        n = 20
        if len(new_dic) < 20:
            n = len(new_dic)
        for i in range(n):
            print(new_dic[i])

if __name__ == "__main__":
    main()