import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def segTool(inputfile, outputfile):
    with open(outputfile, "w", encoding="utf-8") as w:
        with open(inputfile, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                line = "".join(line.strip().split())
                res = jieba.cut_for_search(line)
                res = " ".join(res)
                w.write(res+"\n")

def get_tfidf(filename, outputfile):
    # 00、读取文件,一行就是一个文档，将所有文档输出到一个list中
    corpus = []
    for line in open(filename, 'r', encoding="utf-8").readlines():
        corpus.append(line.strip())

    # 01、构建词频矩阵，将文本中的词语转换成词频矩阵
    vectorizer = CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b')
    vectorizer.fit(corpus)
    # a[i][j]:表示j词在第i个文本中的词频
    X = vectorizer.transform(corpus)
    # 03、获取词袋模型中的关键词
    bag_of_words = vectorizer.get_feature_names()
    # 02、构建TFIDF权值
    transformer = TfidfTransformer()
    # 计算tfidf值
    transformer.fit(X.toarray())

    dic = {}
    for idx, word in enumerate(bag_of_words):
        print("{}\t{}".format(word, transformer.idf_[idx]))
        dic[word] = transformer.idf_[idx]
    with open(outputfile, "w", encoding="utf-8") as w:
        w.write(str(dic))


if __name__ == "__main__":
    # segTool("data/TFIDF/post-comment.txt", "data/TFIDF/trainningSet.txt")
    get_tfidf("data/TFIDF/trainningSet.txt", "data/TFIDF/tfidf.txt")