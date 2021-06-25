from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'D:\Desktop\大二下期文件\数据新闻\实验工具\stanford-corenlp-full-2018-10-05', lang='zh')


f = open("data.txt", encoding='utf-8')   #设置文件对象
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
print("\n")

#找到词汇链
print("得到词汇链如下：")
np_list = {{}}
wordnum = 1
max_np = {}
str = "->"
for word in new_wordlist:
    num = 0
    max_np[wordnum] = 0
    print('\n', wordnum, word)
    for k in range(len(postag) - 1):
        flag = 0
        if postag[k][0] == word:
            if postag[k + 1][1][0] == 'N':
                np_list[wordnum].append(str)
                np_list[wordnum].append(postag[k + 1])
                if postag[k + 2][1][0] == 'N':
                    np_list[wordnum].append(str)
                    np_list[wordnum].append(postag[k + 2])
                    if postag[k + 3][1][0] == 'N':
                        print('-', postag[k], postag[k + 1], postag[k + 2], postag[k + 3], num, ' ', end='')
                        max_np[wordnum] = 4
                        np_list[wordnum].append(str)
                        np_list[wordnum].append(postag[k + 3])
                    else:
                        print('-', postag[k],postag[k + 1], postag[k + 2], num, ' ', end = '')
                        max_np[wordnum] = max(max_np[wordnum], 3)
                else:
                    print('-', postag[k], postag[k + 1], num, ' ', end = '')
                    max_np[wordnum] = max(max_np[wordnum], 2)
            else:
                print('-', postag[k], num, ' ', end ='')
                max_np[wordnum] = max(max_np[wordnum], 1)
                np_list[wordnum].append(str)

        num = num + 1

    np_list[wordnum].append([])
    wordnum = wordnum + 1

print("\n")
print("各词汇链中最长的np长度为:", max_np)
print("最长NP存在于", max(max_np))


#找到最长np

'''
#命名实体识别
ner = nlp.ner(s)
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
    print (i, '-'.join([str(begin), token[begin-1]]), '-'.join([str(end),token[end-1]]))
'''
nlp.close()#有了它进程就不会占用空间出不来了哭
