import codecs
import jieba.analyse
import re

"""
获取每个post的关键词和其对应的TFIDF值
"""

# 去掉只包含非汉字的对话
zhmodel = re.compile(u'[\u4e00-\u9fa5]')
# 检查非中文
#zhmodel = re.compile(u'[^\u4e00-\u9fa5]')

def getTFIDF(input_dir="data/post-comment", output_dir="data/trainData.txt"):
    with codecs.open(output_dir, "w", "utf-8") as w:
        with codecs.open(input_dir, "r", "utf-8") as f:
            for line in f:
                try:
                    newstr = line.strip().split("\t")
                    lines = newstr[1].split()
                    tag = jieba.analyse.extract_tags(lines[0], withWeight=True, topK=20)
                    tag_dict = {i[0]: i[1] for i in tag}
                    w.write(str(tag_dict) + "\t" + newstr[1] + "\n")
                except Exception as e:
                    match = zhmodel.search(line)
                    if match:
                        lines = line.strip().split()
                        tag = jieba.analyse.extract_tags(lines[0], withWeight=True, topK=20)
                        tag_dict = {i[0]: i[1] for i in tag}
                        w.write(str(tag_dict) + "\t" + line.strip() + "\n")
                    else:
                        print(line.strip())

if __name__ == "__main__":
    getTFIDF()
