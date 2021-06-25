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


#命名实体识别
ner = nlp.ner(s)
print('\n命名实体识别:')
print('|'.join([','.join(i) for i in ner]))


#句法分析
parse = nlp.parse(s)
print('\n句法分析:')
print(parse)


#依存关系分析
dependencyParse = nlp.dependency_parse(s)
print('\n依存关系分析:')
for i, begin, end in dependencyParse:
    print (i, '-'.join([str(begin), token[begin-1]]), '-'.join([str(end),token[end-1]]))


print(postag)