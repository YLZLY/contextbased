#-*-coding:utf8-*-

"""
author:YJM

date:20190420

util function

"""
from __future__ import division
import os
import operator


#获取平均分的函数方法
def get_ave_score(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {} #计算评分的数据结构
    score_dict = {} #要返回的数据结构
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item)<4:#如果列数小于4就过滤掉
            continue
        userid,itemid,rating = item[0],item[1],float(item[2])
        if itemid not in record_dict:
            record_dict[itemid]=[0,0]
        record_dict[itemid][0] += 1 #有多少个人评分
        record_dict[itemid][1] += rating #总分是多少
    fp.close()
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][0],3)
    return score_dict

# 第一个返回值从item对应类别的字典 字典里面套字典，每个类别对应的分数，第二个返回值是类别对应的item的倒排表
def get_item_cate(ave_score,input_file):
    """
    :param ave_score: a dict ,key itemid value rating score
    :param input_file: item info file
    :return:a dict:key itemid value a dict,key:cate value:ratio 每个itemid对应的类别
            a dict:key cate value [itemid1,item2,itemid3] 每个类别对应的itemid的倒排表
    """
    if not os.path.exists(input_file):
        return {},{}
    linenum=0
    item_cate ={}
    record ={} #记录中间信息
    cate_item_sort ={}#存储最后的倒排
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item)<3:
            continue
        itemid = item[0]
        cate_str = item[-1]# 取出类别
        cate_list = cate_str.strip().split("|")#类别划成数组
        ratio = round(1/len(cate_list),3)#不同类别均分权重
        if itemid not in item_cate:
            item_cate[itemid]={}
        for fix_cate in cate_list:
            item_cate[itemid][fix_cate]=ratio#把权重定义给itemid的每个类别
    fp.close()
    #获得每个种类下的item的倒排
    #记录每一个种类下item的平均的评分
    for itemid in item_cate:
        for cate in item_cate[itemid]:
            if cate not in record:
                record[cate]={}
            itemid_rating_score = ave_score.get(itemid,0)
            record[cate][itemid] = itemid_rating_score
    for cate in record:
        if cate not in cate_item_sort:
            cate_item_sort[cate]=[]
        for zuhe in sorted(record[cate].items(),key=operator.itemgetter(1),reverse=True)[:100]:
            # .items()方法将字典中的无序的键值对转成了有序的元组，每一个zuhe都是一个元组
            # zuhe[0]是元组中的第一项也就是itemid，zuhe[1]是元组中第二项也就是分数
            # cate_item_sort[cate].append(zuhe[0]+"-"+str(zuhe[1]))
            cate_item_sort[cate].append(zuhe[0])
    return item_cate, cate_item_sort

if __name__ == '__main__':

    ave_score = get_ave_score('../data/ratings15000.csv')
    # print(len(ave_score))
    # print(ave_score['34'])
    item_cate,cate_item_sort = get_item_cate(ave_score,'../data/movies.csv')
    # print(len(item_cate))
    # print(item_cate['1'])
    # print(cate_item_sort['Children'])
    # t rain_data =  get_train_data('../data/ratings.csv')
    # print train_data[:20]
    # print(len(train_data))


