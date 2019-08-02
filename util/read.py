#-*-coding:utf8-*-

"""
author:YJM

date:20190420

util function

"""
from __future__ import division
import os
import operator
import sys


def get_ave_score(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item)<4:
            continue
        userid,itemid,rating = item[0],item[1],float(item[2])
        if itemid not in record_dict:
            record_dict[itemid]=[0,0]
        record_dict[itemid][0] += 1
        record_dict[itemid][1] += rating
    fp.closed
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][0],3)
    return score_dict

def get_item_cate(ave_score,input_file):
    """
    :param ave_score: a dict ,key itemid value rating score
    :param input_file: item info file
    :return:a dict:key itemid value a dict,key:cate value:ratio 每个对应的类别
            a dict:key cate value [itemid1,item2,itemid3] 每个类别对应的item的倒排
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
        cate_str = item[-1]
        cate_list = cate_str.strip().split("|")
        ratio = round(1/len(cate_list),3)
        if itemid not in item_cate:
            item_cate[itemid]={}
        for fix_cate in cate_list:
            item_cate[itemid][fix_cate]=ratio
    fp.close()
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
            cate_item_sort[cate].append(zuhe[0]+"-"+str(zuhe[1]))
    return item_cate, cate_item_sort

if __name__ == '__main__':

    ave_score = get_ave_score('../data/ratings15000.csv')
    # print(len(ave_score))
    # print(ave_score['32'])
    item_cate,cate_item_sort = get_item_cate(ave_score,'../data/movies.csv')
    # print(len(item_cate))
    # print(item_cate['1'])
    # print(cate_item_sort['Children'])
    # t rain_data = get_train_data('../data/ratings.csv')
    # print train_data[:20]
    # print(len(train_data))


