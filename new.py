import jieba
text = "苏伊士运河恢复通航!搁浅货轮已完全恢复至正常航道 新华社快讯埃及苏伊士运河管理局29日发布公报说搁浅货轮已经完全恢复至正常航道。23日，一艘悬挂巴拿马国旗的重型货轮在苏伊士运河新航道搁浅，造成航道拥堵。25 日，苏伊士运河管理局正式宣布运河暂停航行。就在不久前,埃及总统塞西曾宣布苏伊士运河河道的疏通工作成功完成。"

cut_words = ""
all_words = ""
f = open('data.txt', 'w')

#默认是精确模式
data = jieba.cut(text)
print(u"[默认模式]: ", "/".join(data))

#返回列表
seg_list = jieba.lcut(text, cut_all=False)
print("[返回列表]: {0}".format(seg_list))
