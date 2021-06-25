from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'D:\Desktop\大二下期文件\数据新闻\实验工具\stanford-corenlp-full-2018-10-05', lang='zh')


f = open("综合实验中文.txt", encoding='utf-8')   #设置文件对象
s = f.read()     #将txt文件的所有内容读入到字符串str中
f.close()   #将文件关闭

#分词
token = nlp.word_tokenize(s)
print('\n分词:')
print(' '.join(token))

#词性标注
postag = nlp.pos_tag(s)
print('\n词性标注(POS):')
print('|'.join([','.join(i) for i in postag]))

#找到不重复名词短语
wordlist = set()#无序
wordcount = []
for j in postag:
    if (j[1][0] == 'N') and j[1] != 'PU':
        wordlist.add(j[0])
print("\n词汇有(不包含重复部分)：\n", wordlist)
print("\n")


new_wordlist = set()
print("词汇及其频率（只考虑频率大与1的词语）：")
#计算各个词出现频率（只考虑频率大与1的词语）
for word in wordlist:
    word_cnt = token.count(word)
    if word_cnt > 1:
        wordcount.append(word)
        new_wordlist.add(word)
        print('(', word, ' 频率:', word_cnt, ')', end = '')

#找到词汇链
print("\n得到词汇链如下：")
wordnum = 1
max_np = {}
for word in new_wordlist:
    num = 0
    max_np[wordnum] = 0
    print('\n', wordnum, word)
    for k in range(len(postag) - 1):
        flag = 0
        if postag[k][0] == word:
            if postag[k + 1][1][0] == 'N':
                if postag[k + 2][1][0] == 'N':
                    if postag[k + 3][1][0] == 'N':
                        if postag[k + 4][1][0] == 'N':
                            if postag[k + 5][1][0] == 'N':
                                print("-%s%s%s%s%s%s"%(postag[k][0], postag[k + 1][0], postag[k + 2][0], postag[k + 3][0], postag[k + 4][0],postag[k + 5][0]), num, ' ', end='')
                                max_np[wordnum] = 6
                            else:
                                print("-%s%s%s%s%s"%(postag[k][0], postag[k + 1][0], postag[k + 2][0], postag[k + 3][0],postag[k + 4][0]), num, ' ', end='')
                                max_np[wordnum] = max(max_np[wordnum], 5)
                        else:
                            print("-%s%s%s%s"%(postag[k][0], postag[k + 1][0], postag[k + 2][0], postag[k + 3][0]), num, ' ', end='')
                            max_np[wordnum] = max(max_np[wordnum], 4)
                    else:
                        print("-%s%s%s"%(postag[k][0],postag[k + 1][0], postag[k + 2][0]), num, ' ', end = '')
                        max_np[wordnum] = max(max_np[wordnum], 3)
                else:
                    print("-%s%s"%(postag[k][0], postag[k + 1][0]), num, ' ', end = '')
                    max_np[wordnum] = max(max_np[wordnum], 2)
            else:
                print('-', postag[k][0], num, ' ', end ='')
                max_np[wordnum] = max(max_np[wordnum], 1)

        num = num + 1
    wordnum = wordnum + 1

print("\n")
print("各词汇链中最长的np长度为:", max_np)
print("最长NP存在于第 %d 条链, 最长的np长度为：%d " %(max(max_np, key = max_np.get), max_np[max(max_np, key = max_np.get)]))


#找到最长np

'''
#命名实体识别
ner = nlp.ner(s)
print(ner)
print('\n命名实体识别:')
print('|'.join([','.join(i) for i in ner]))
'''
'''
#句法分析
parse = nlp.parse(s)
print('\n句法分析:')
print(parse)
'''
'''
#依存关系分析
dependencyParse = nlp.dependency_parse(s)
print('\n依存关系分析:')
for i, begin, end in dependencyParse:
    print(i, '-'.join([str(begin), token[begin-1]]), '-'.join([str(end),token[end-1]]))
'''
nlp.close()#有了它进程就不会占用空间出不来了哭
