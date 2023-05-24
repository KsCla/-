import matplotlib.pyplot as plt
root_path = "D:\\document\\gradu\\自测数据分析"
import sys
sys.path.append( root_path )
from read_file import Read
from k_points_average import *
import os
from merge import *
from sklearn.cluster import dbscan

def Preprocess(freq , resolution): #完成k点滑动平均+峰合并
    k = Calc_average_len(freq)
    freq = KPointsSmooth(freq , k)
    peak_num = 2
    freq = Merge(freq , peak_num , resolution)
    return freq

def Get_real_peak(freq): #提取高于噪声的特征峰
    level = 27.0
    temp = Get_peak(freq)
    peak = []
    for p in temp:
        if (freq[p]> max(freq)-level ):
            peak.append(p)
    return peak

def Extract(freq_list , res): #抽取一批频谱中的特征峰坐标
    idx = []
    cnt = 0
    peaks = []
    for freq in freq_list:
        cnt += 1
        data = Preprocess(freq , res)
        peak = Get_real_peak(data)
        for p in peak:
            peaks.append( [p,data[p]] )
            idx.append(cnt)
    return idx , peaks

def Show_peaks(batch_id): #展示一批频谱中的特征峰位置
    batch_size = 50
    res = 5000/600
    freq_list = []
    for cnt in range( (batch_id-1)*batch_size+1 , batch_id*batch_size+1 ):
        freq_list.append( Read(cnt) )
    
    idx , peaks = Extract(freq_list , res)

    path = "D:\\document\\gradu\\自测数据分析\\analyse\\"
    img_path = path + str(batch_id) + ".jpg"
    plt.figure()
    for p in peaks: plt.scatter(p[0] , p[1] , c = "red" , s = 2)
    plt.savefig(img_path , dpi = 300)
    plt.close()

def Work_dbscan(freq_list , res):
    idx , peaks = Extract(freq_list , res)

    h_convert = 5.0
    w_convert = 100.0
    points = []
    for p in peaks: points.append([ p[0]*res/w_convert , p[1]/h_convert ])
    #先进行横纵坐标变换

    r = 1.0
    min_pts = 25
    core_samples , cluster_ids = dbscan(points , eps=r , min_samples=min_pts)

    return idx , peaks , cluster_ids

def Show_dbscan(batch_id): #展示一批频谱的分类结果
    batch_size = 50
    res = 5000/600
    freq_list = []
    for cnt in range( (batch_id-1)*batch_size+1 , batch_id*batch_size+1 ):
        freq_list.append( Read(cnt) )
    
    idx , peaks , cluster_ids = Work_dbscan(freq_list , res)

    path = "D:\\document\\gradu\\自测数据分析\\analyse\\dbscan_"
    img_path = path + str(batch_id) + ".jpg"
    plt.figure()

    x = [p[0] for p in peaks]
    y = [p[1] for p in peaks]
    plt.scatter(x , y , c = cluster_ids , s = 2)
    plt.savefig(img_path , dpi = 300)
    plt.close()

if __name__ == "__main__":
    for batch_id in range(1,7):
        Show_dbscan(batch_id)
