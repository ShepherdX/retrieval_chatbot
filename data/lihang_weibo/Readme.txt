Readme for conversation_data_v1.1
{jizongcheng, Lu.Zhengdong, HangLi.HL}@huawei.com
Huawei Noah's Ark Lab
2014-01-21

This version of dataset (with some minor modifications listed below) is prefered over the previous one.
We have get permission from Sina to release this dataset only for research purpose. 


-------------------------------------------------
Some main differences from conversation_data_v1.0
-------------------------------------------------
1. In v1.0, we leave only the Chinese characters in "post.index" and "response.index" by dropping English words, numbers and punctuations, etc., while
   in v1.1, we retain the dropped English words, numbers and punctuations with the Chinese characters for better reading and understanding for human.

2. In v1.0, original post-responses pairs are split into two files "original_trn.pair" and "orignal_tst.pair" for training and testing the semantic match model used in section 3.1 of paper [1], while
   in v1.1, we combine them into one single file "original.pair" for simplification.

3. In v1.0, there are some duplicate post-response pairs, while
   in v1.1, we remove the duplicate post-response pairs.


--------------------
Files in this folder
--------------------
This folder contains five files:
    1. post.index       contains post_id with its contents
    2. response.index   contains response_id with its contents
    3. original.pair    original post-response pairs
    4. labeled.pair     labeled post-response pairs
    5. Readme           readme of this dataset

"post.index" and "response.index" save the content of the posts and responses.
    1. Format for post.index
        post_id##word1 word2 word3..
        For example: 0##祝 各位 朋友 2012 年 万事如意 ！

    2. Format for response.index
        response_id##word1 word2 word3..
        For example: 0##祝 汤 教授 新年 快乐

    NOTE that the content is given after Chinese word segmentation.

"original.pair" and "labeled.pair" save the original post-response pairs and the labeled post-response pairs, all saved in their IDs.
    3. Format for original.pair
        post_id:response_id1,response_id2,...
        where post_id and response_idx are respectively the post and response index. For example:
            0:0,1,2,3,4,5,6,7,10,12,13,24,25,29,32,36,359,455,640,679

    4. Format for labeled.pair
        label,post_id,response_id
        where label=2, if the pair is considered appropriate, and 1 otherwise. For example:
            ...
            1,10270,272666
            1,10270,126721
            2,10270,126728
            1,10270,126754
            ...

    NOTE that 1) the labeling is only on a small subset of the 38,016 posts, and 
              2) for each seleted (query) post, the labeled responses are not originally given to it.
                 
                 You can get original post_id for response_id from file "original.pair".
                 For example, the original post_id for response_id 272666 is 19109.


--------------------------
Statistics of this dataset
--------------------------
Retrieval_Repository
    #posts              38,016
    #responses          618,104
    #original_pairs     618,104
Labeled_Data
    #posts              422
    #responses          12,402
    #labeled_pairs      12,402


---------------
Please cite the following paper if you publish any result on this data set. Reference paper:
---------------
[1] Hao Wang, Zhengdong Lu, Hang Li, Enhong Chen.
    A Dataset for Research on Short-Text Conversation,
    In Proceedings of Empirical Methods in Natural Language Processing (EMNLP), 935-945, 2013.


