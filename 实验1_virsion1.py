# coding=utf-8
from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'D:\Desktop\大二下期文件\数据新闻\实验工具\stanford-corenlp-full-2018-10-05', lang='zh')


f = open("test.txt", encoding='utf-8')   #设置文件对象
s = f.read()     #将txt文件的所有内容读入到字符串str中
f.close()   #将文件关闭

#分词
token = nlp.word_tokenize(s)
print('\n分词:')
print(' '.join(token))

#命名实体识别
'''
ner = nlp.ner(s)
#print(ner)
print('\n命名实体识别:')
print('|'.join([','.join(i) for i in ner]))
COUNTRY = []
ORGANIZATION = []
DATE = []
for word in ner:
    if word[1] == "COUNTRY":
        COUNTRY.append(word[0])
    elif word[1] == "ORGANIZATION":
        ORGANIZATION.append(word[0])
    elif word[1] == "DATE":
        DATE.append(word[0])
print("命名实体识别结果如下：")
print("COUNTRY = :", list(set(COUNTRY)))
print("ORGANIZATION = :", list(set(ORGANIZATION)))
print("DATE = :", list(set(DATE)))
'''

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



new_wordlist = set()
print("\n词汇及其频率（只考虑频率大与1的词语）:")
#计算各个词出现频率（只考虑频率大与1的词语）
for word in wordlist:
    word_cnt = token.count(word)
    if word_cnt > 1:
        wordcount.append(word)
        new_wordlist.add(word)
        print('(', word, ' 频率:', word_cnt, ')', end = '')


#找到词汇链

print("\n得到词汇链如下：")
wordnum = 0
max_np = {}
word_list = []#记录词汇链
index = 0 #词汇链的下表
for word in new_wordlist: #遍历所有符合要求的词，寻找最长np，并记录最长np的长度
    num = 0
    max_np[wordnum] = 0
    list = []
    for k in range(len(postag) - 1):
        num_np = 0
        flag = 0
        if postag[k][0] == word:
            updata_word = postag[k][0]
            for i in range(k + 1, len(postag) - 1):
                if postag[i][1][0] == 'N':
                    updata_word = updata_word + postag[i][0] #将np连接起来
                    num_np = num_np + 1
                else:
                    break
            list.append((updata_word,num))
            max_np[wordnum] = max(max_np[wordnum], num_np)
        num = num + 1
    print(wordnum, word, ':\n', list) #输出词汇链
    word_list.append(list) #将词汇链加进对应的word_list中
    index = index + 1
    wordnum = wordnum + 1


#词汇链输出

print("\n词汇链如下：")
for i in range(len(word_list)):
    if word_list[i]:
        print("%d : "%i, word_list[i])



#最长词汇链

#找到最长np以及对应的np链
print("\n各词汇链中最长的np长度为:", max_np)
max_np_len = max_np[max(max_np, key = max_np.get)]
print("最长的np长度为", max_np_len)
print("最长的NP链为：")
for i in range(len(word_list)):
    if max_np[i] == max_np_len:
        max_np_list = word_list[i]
        print("%d : "%(i), max_np_list)


print('\n分析事件链')
event_list = []#事件链表
trigger_list = []#触发词表
event_elements_list = []#事件要素链
for list in word_list:
    the_event_list = []
    the_trigger_list = []
    the_elements_list = []
    for word in list:
        #event_word = word[0]
        elements = word[0]
        for k in range(word[1] + 1, len(postag) - 1):
            flag = 0 #是否已经遇到了N
            if postag[k][1] == 'VV':
                event_word = postag[k][0]
                trigger = postag[k][0]
                if postag[k - 1][1] == 'AD':
                    trigger = postag[k - 1][0] + postag[k][0]
                elements = elements + trigger  # 将np与动词连接起来
                for j in range(k + 1, len(postag) - 1):
                    if postag[j][1][0] == 'PU':#遇到标点符号停顿停止
                        break
                    if postag[j][1][0] == 'N':#遇到名词事件要素加上
                        flag = 1
                        elements = elements + postag[j][0]
                    elif postag[j][1] == 'VV':#遇到动词加上，并补充轻动词
                        if postag[j - 1][1] == 'AD':
                            elements = elements + postag[j - 1][0] + postag[j][0]
                        break
                break
        the_event_list.append(event_word)
        the_elements_list.append(elements)
        the_trigger_list.append(trigger)
    event_list.append(the_event_list)
    event_elements_list.append(the_elements_list)
    trigger_list.append(the_trigger_list)

#输出事件链
print("\n得到事件链、复杂触发词、事件要素如下：")
for i in range(len(event_list)):
    print("\n%d: 事件链 " % i, event_list[i])
    print("%d: 复杂触发词 " % i, trigger_list[i])
    print("%d: 事件要素" % i, event_elements_list[i])




''''
#找到不重复名词短语
verblist = set()#无序
verbcount = []
for j in postag:
    if j[1][0] == 'V':
        verblist.add(j[0])
print("\n词汇有(不包含重复部分)：\n", verblist)



new_verblist = set()
print("\n动词及其频率（只考虑频率大与1的词语）:")
#计算各个词出现频率（只考虑频率大与1的词语）
for verb in verblist:
    verb_cnt = token.count(verb)
    if verb_cnt > 1:
        verbcount.append(verb)
        new_verblist.add(verb)
        print('(', verb, ' 频率:', verb_cnt, ')', end = '')


#找到事件链
print("\n得到事件链如下：")
wordnum = 0
max_np = {}
event_list = []#记录事件链
index = 0 #事件链的下标
for verb in new_verblist: #遍历所有符合要求的词，寻找最长事件链，并记录最长事件的长度
    num = 0
    max_np[wordnum] = 0
    list = []
    for k in range(len(postag) - 1):
        num_np = 0
        flag = 0
        if postag[k][0] == verb:
            updata_word = postag[k][0]
            for i in range(k + 1, len(postag) - 1):
                if postag[i][1][0] == 'N':
                    continue
                if postag[i][1][0] == 'V':
                    updata_word = updata_word + postag[i][0] #将np连接起来
                    list.append(updata_word)
                    num_np = num_np + 1
                else:
                    list.append(updata_word)
                    break
            max_np[wordnum] = max(max_np[wordnum], num_np)
        num = num + 1
    print(wordnum, verb, ':\n', list) #输出词汇链
    word_list.append(list) #将词汇链加进对应的word_list中
    index = index + 1
    wordnum = wordnum + 1


#词汇链输出

print("\n词汇链如下：")
for i in range(len(word_list)):
    if word_list[i]:
        print("%d : "%i, word_list[i])



#最长词汇链

#找到最长np以及对应的np链
print("\n各词汇链中最长的np长度为:", max_np)
max_np_len = max_np[max(max_np, key = max_np.get)]
print("最长的np长度为", max_np_len)
print("最长的NP链为：")
for i in range(len(word_list)):
    if max_np[i] == max_np_len:
        print("%d : "%(i), word_list[i])
'''

#句法分析
'''
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
