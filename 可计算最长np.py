#-*- coding:utf-8 -*-
from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'D:\Desktop\大二下期文件\数据新闻\实验工具\stanford-corenlp-full-2018-10-05', lang='zh')
f = open('综合实验中文.txt','r', encoding = 'utf-8')
s = f.read()
title = '巴西批准本土研发新冠疫苗开展临床试验'
sentence = " 巴西国家卫生监督局9日宣布，批准布坦坦研究所对其研发的新冠疫苗ButanVac进行临床试验。预计将有6000名18岁及以上的志愿者参与Ⅰ期和Ⅱ期临床试验。该疫苗需要接种两剂，间隔为28天。布坦坦研究所3月26日向巴西国家卫生监督局申请对ButanVac进行临床试验，4月开始该疫苗的生产工作，预计将在6月生产1800万剂。这款疫苗使用的载体病毒是鸡新城疫病毒。鸡新城疫是一种只会感染鸟类的疾病，鸡新城疫病毒可在鸡蛋胚胎中大量复制，但不会在人体中引发症状。据巴西媒体报道，生产这款疫苗的原料均可在本地获得，不依赖进口。巴西卫生部9日公布的最新数据显示，巴西较前一日新增新冠确诊病例85748例，累计确诊17122877例；新增死亡病例2723例，累计死亡479515例；累计治愈15596816例。巴西主流媒体根据各州卫生厅公布的数据联合统计得出，截至9日20时，全国已有51846929人接种第一剂新冠疫苗，占总人口的24.48%，有23418325人接种第二剂疫苗，占总人口的11.06%"
token = nlp.word_tokenize(s)
print('\n分词：')
title_lst = nlp.word_tokenize(title)
word_lst = nlp.word_tokenize(sentence)
print("  ".join(str(x) for x in title_lst))
print("  ".join(str(x) for x in word_lst))

word_set = set()
dupword_list = []
for word in token:
    if word == '，' or word == '、' or word == '。' or word == '“' or word == '”':
        continue
    word_set.add(word)
print('\n重复词汇：')
for word in word_set:
    word_count = token.count(word)
    if word_count > 1:
        dupword_list.append(word)
        print('(',word,'-频率:',word_count,')',end = '')

# 词汇链
print('\n词汇链：')
for dupword in dupword_list:
    posi = 0
    for word in token:
        if word == dupword:
            print(word,posi,'->',end='')
        posi = posi + 1
    print('')

# 词性标注
title_pos_list = nlp.pos_tag(title)
pos_list = nlp.pos_tag(sentence)
postag = nlp.pos_tag(s)

# 句法分析
parse = nlp.parse(s)

# 基于词性标注获得长NP
print('NP:')
npcnt = len(title_pos_list) - 1
npi = 0
np_lst = []
while npi <= npcnt:
    npstr = ''
    while npi <= npcnt:
        if title_pos_list[npi][1] == 'NR' or title_pos_list[npi][1] == 'NN' or title_pos_list[npi][1] == 'JJ':
            npstr = npstr + title_pos_list[npi][0]
            npi = npi + 1
        else:
            npi = npi + 1
            break
    if npstr != '':
        np_lst.append(npstr)

npcnt = len(pos_list) - 1
npi = 0
while(npi <= npcnt):
    npstr = ''
    while(npi <= npcnt):
        if pos_list[npi][1] == 'NR' or pos_list[npi][1] == 'NN' or pos_list[npi][1] == 'JJ':   #or pos_lst[npi][1] =='DEG'
            npstr = npstr + pos_list[npi][0]
            npi = npi + 1
        else:
            npi = npi + 1
            break
    if npstr != '':
        np_lst.append(npstr)

print("  ".join(np_lst))
# 最长NP
print('\n最长NP：')
setnp = set(np_lst)
dictnp = {}
for item in setnp:
    dictnp.update({item:len(item)})
dictnp = sorted(dictnp.items(), key=lambda d: d[1], reverse=True)

npi = 0
print(dictnp[npi][0], end='  ')
npmaxlist = dictnp[npi][0]
# print(npmaxlist)
while(1):
    npi = npi + 1
    if dictnp[npi][1] == dictnp[npi - 1][1]:
        print(dictnp[npi][0], end='  ')
    else:
        break

print(' ')

# 最长NP链
print('')
npchain_list = []
for dupword in dupword_list:
    chain = []
    for np in np_lst:
        for tup in np:
            if tup[0] == dupword:
                chain.append(np)
    if len(chain) > 0:
        npchain_list.append(chain)
        print('NP链 （包含词汇链',dupword,end='):')
        for np in chain:
            for tup in np:
                print(tup[0],end='')
            print('->',end='')
        print('')

# 依存关系和事件链
dependencyParse = nlp.dependency_parse(s)
dependency_parse_lst = nlp.dependency_parse(sentence)
title_dependency_parse_lst = nlp.dependency_parse(title)
# print('\n依存关系分析：')
print('事件链：')
for chain in npchain_list:
    for np in chain:
        before = []
        after = []
        for tup in np:
            for i, begin, end in dependencyParse:
                if (begin - 1 == tup[1]) and (i == 'dobj' or i == 'nsubj' or i == 'dep'):
                    if tup[1] < end - 1:
                        after.append(token[end-1])
                    else:
                        before.append(token[end-1])
                elif end -1 == tup[1] and (i == 'dobj' or i == 'nsubj' or i == 'dep'):
                    if tup[1] < begin - 1:
                        after.append(token[begin-1])
                    else:
                        before.append(token[begin-1])

        if len(before) > 0:
            print(before,end='')
        for tup in np:
            print(tup[0],end='')
        if len(after) > 0:
            print(after,end='')
        print('->',end='')
    print('')

# 根据最长NP中的依存关系，分析事件链


# 根据标题依存关系，分析主要事件链
print('\n主要事件链:')
re = []
for i in title_dependency_parse_lst:
    if i[0] == 'nsubj':
        dobj_word = ''
        nn_word = ''
        assmod_word = ''
        ccomp_word = ''
        for k in title_dependency_parse_lst:
            if k[0] == 'dobj' and k[1] == i[1]:
                dobj_word = ' ' + title_lst[k[2]-1]
        for k1 in title_dependency_parse_lst:
            if k1[0] == 'compound:nn' and k1[1] == i[2]:
                nn_word = ' ' + title_lst[k1[2]-1]
        for k2 in title_dependency_parse_lst:
            if k2[0] == 'nmod:assmod' and k2[1] == i[2]:
                assmod_word = ' ' + title_lst[k2[2]-1]
        for k3 in title_dependency_parse_lst:
            if k3[0] == 'ccomp' and k3[1] == i[1]:
                ccomp_word = ' ' + title_lst[k3[2]-1]
        sstr = assmod_word + nn_word + title_lst[i[2]-1] + ' ' + title_lst[i[1]-1] + dobj_word + ccomp_word
        re.append(sstr)

re_str = ''
for n in re:
    if n == re[-1]:
        re_str = re_str + n
    else:
        re_str = re_str + n + ' --> '

print(re_str)

# 命名实体识别
ner_lst = nlp.ner(s)
print('\n要素识别：')
print('人名',end=': ')
person_lst = []
for item in ner_lst:
    if item[1] == 'PERSON':
        person_lst.append(item[0])
setp = set(person_lst)
print("、".join(str(x) for x in setp))

print('地名', end=': ')
location_lst = []
for item in ner_lst:
    if item[1] == 'CITY' or item[1] == 'COUNTRY' or item[1] == 'LOCATION' or item[1] == 'GPE':
        location_lst.append(item[0])
setl = set(location_lst)
print("、".join(str(x) for x in setl))

print('组织名', end=': ')
orgna_lst = []
for item in ner_lst:
    if item[1] == 'ORGANIZATION':
        orgna_lst.append(item[0])
seto = set(orgna_lst)
print("、".join(str(x) for x in seto))

print('时间', end=': ')
time_lst = []
for item in ner_lst:
    if item[1] == 'DATE':
        time_lst.append(item[0])
sett = set(time_lst)
print("、".join(str(x) for x in sett))
#print('|'.join([','.join(i) for i in ner]))
#for item in ner:
#    if item[1] == 'DATE':
#        print('时间:',item[0])
#for item in ner:
#    if item[1] == 'COUNTRY' or item[1] == 'STATE_OR_PROVINCE':
#        print('地名:',item[0])
#for item in ner:
#    if item[1] == 'PERSON':
#        print('人名:',item[0])
#for item in ner:
#    if item[1] == 'ORGANIZATION':
#        print('组织名:',item[0])

#根据依存关系，分析事件要素
print('\n内容事件要素:')
re = []
for i in dependency_parse_lst:
    if i[0] == 'nsubj':
        dobj_word = ''
        nn_word = ''
        assmod_word = ''
        ccomp_word = ''
        for k in dependency_parse_lst:
            if k[0] == 'dobj' and k[1] == i[1]:
                dobj_word = ' ' + word_lst[k[2]-1]
        for k1 in dependency_parse_lst:
            if k1[0] == 'compound:nn' and k1[1] == i[2]:
                nn_word = ' ' + word_lst[k1[2]-1]
        for k2 in dependency_parse_lst:
            if k2[0] == 'nmod:assmod' and k2[1] == i[2]:
                assmod_word = ' ' + word_lst[k2[2]-1]
        for k3 in dependency_parse_lst:
            if k3[0] == 'ccomp' and k3[1] == i[1]:
                ccomp_word = ' ' + word_lst[k3[2]-1]
        sstr = assmod_word + nn_word + word_lst[i[2]-1] + ' ' + word_lst[i[1]-1] + dobj_word + ccomp_word
        re.append(sstr)

re_str = ''
for n in re:
    if n == re[-1]:
        re_str = re_str + n
    else:
        re_str = re_str + n + ' --> '

print(re_str)
nlp.close()